from flask import Flask, request, jsonify, render_template
import yt_dlp
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def process_video():
    data = request.get_json() or {}
    url = data.get('url')

    if not url:
        return jsonify({'error': 'Lütfen geçerli bir URL girin.'}), 400

    # Doğrudan çalışan video bağlantısını API üzerinden çekiyoruz
    try:
        api_url = f"https://apis.davidcyriltech.my.id/download?url={url}"
        response = requests.get(api_url, timeout=10)
        res_data = response.json()
        
        if res_data.get("status") == 200:
            download_link = res_data.get("result", {}).get("video") or res_data.get("result", {}).get("download_url")
            if download_link:
                return jsonify({
                    'success': True,
                    'title': 'LemonFetch Video',
                    'download_url': download_link
                })
    except Exception:
        pass

    # Yedek olarak yt-dlp denemesi
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            if video_url:
                return jsonify({
                    'success': True,
                    'title': info.get('title', 'LemonFetch Video'),
                    'download_url': video_url
                })
    except Exception:
        pass

    return jsonify({'error': 'Video indirilemedi. Platform şu an engelliyor olabilir.'}), 429

if __name__ == '__main__':
    app.run(debug=True)
