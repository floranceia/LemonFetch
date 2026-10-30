from flask import Flask, request, jsonify, render_template, Response
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

    video_url = None

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            if not video_url and 'entries' in info:
                video_url = info['entries'][0].get('url')
    except Exception:
        pass

    if not video_url:
        try:
            api_url = f"https://apis.davidcyriltech.my.id/download?url={url}"
            response = requests.get(api_url, timeout=10)
            res_data = response.json()
            if res_data.get("status") == 200:
                video_url = res_data.get("result", {}).get("video") or res_data.get("result", {}).get("download_url")
        except Exception:
            pass

    if not video_url:
        return jsonify({'error': 'Platform şu an istekleri engelliyor. Limonları kabul edip birazdan tekrar deneyebilirsin! 🍋'}), 429

    # 403 hatasını aşmak için videoyu kendi sunucumuz üzerinden proxy ediyoruz
    proxy_url = f"/proxy-download?url={requests.utils.quote(video_url)}"

    return jsonify({
        'success': True,
        'title': 'LemonFetch Video',
        'download_url': proxy_url
    })

@app.route('/proxy-download')
def proxy_download():
    target_url = request.args.get('url')
    if not target_url:
        return "Geçersiz bağlantı", 400
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = requests.get(target_url, headers=headers, stream=True, timeout=15)
        return Response(req.iter_content(chunk_size=1024), content_type=req.headers.get('content-type', 'video/mp4'))
    except Exception:
        return "Video indirilemedi", 500

if __name__ == '__main__':
    app.run(debug=True)
