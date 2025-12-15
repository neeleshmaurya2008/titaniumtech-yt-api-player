from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "FLASK API LIVE"

# ---------------- PLAYLIST API ----------------
@app.route("/api/playlist", methods=["GET"])
def playlist_api():
    url = request.args.get("url")
    if not url:
        return jsonify({"success": False, "error": "Playlist URL is required"}), 400

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": True,
        "ignoreerrors": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(url, download=False)

        playlist = {
            "id": data.get("id"),
            "title": data.get("title"),
            "description": data.get("description"),
            "channel": data.get("channel"),
            "channel_id": data.get("channel_id"),
            "channel_url": data.get("channel_url"),
            "playlist_url": data.get("webpage_url"),
            "total_videos": data.get("playlist_count"),
            "videos": []
        }

        for v in data.get("entries", []):
            if v:
                playlist["videos"].append({
                    "video_id": v.get("id"),
                    "title": v.get("title"),
                    "duration": v.get("duration"),
                    "channel": v.get("channel"),
                    "video_url": f"https://www.youtube.com/watch?v={v.get('id')}"
                })

        return jsonify({"success": True, "playlist": playlist})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ---------------- VIDEO API ----------------
@app.route("/api/video", methods=["GET"])
def video_api():
    url = request.args.get("url")
    if not url:
        return jsonify({"success": False, "error": "Video URL is required"}), 400

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "ignoreerrors": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(url, download=False)

        video = {
            "id": data.get("id"),
            "title": data.get("title"),
            "description": data.get("description"),
            "duration": data.get("duration"),
            "view_count": data.get("view_count"),
            "like_count": data.get("like_count"),
            "channel": data.get("channel"),
            "thumbnail": data.get("thumbnail"),
            "webpage_url": data.get("webpage_url"),
            "is_live": data.get("is_live"),
            "live_status": data.get("live_status"),
            "formats": [
                {
                    "format_id": f.get("format_id"),
                    "ext": f.get("ext"),
                    "resolution": f.get("resolution"),
                    "fps": f.get("fps"),
                    "url": f.get("url")
                }
                for f in data.get("formats", [])
            ]
        }

        return jsonify({"success": True, "video": video})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# REQUIRED for Vercel
handler = app
