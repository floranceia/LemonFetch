from flask import Flask, request, jsonify, render_template, redirect
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

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 10,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            
            if not video_url and 'entries' in info:
                video_url = info['entries'][0].get('url')

            if video_url:
                return jsonify({
                    'success': True,
                    'title': info.get('title', 'LemonFetch Video'),
                    'download_url': video_url
                })
    except Exception:
        pass

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

    return jsonify({'error': 'Platform şu an istekleri engelliyor. Limonları kabul edip birazdan tekrar deneyebilirsin! 🍋'}), 429

if __name__ == '__main__':
    app.run(debug=True)
