from flask import Flask, request, jsonify, render_template
import yt_dlp

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
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            video_url = info.get('url')
            
            if not video_url and 'entries' in info:
                video_url = info['entries'][0].get('url')

            if not video_url:
                return jsonify({'error': 'Video adresi alınamadı, lütfen bağlantıyı kontrol edin.'}), 400

            return jsonify({
                'success': True,
                'title': info.get('title', 'LemonFetch Video'),
                'download_url': video_url
            })
    except Exception as e:
        error_msg = str(e)
        if "bot" in error_msg.lower() or "429" in error_msg:
            return jsonify({'error': 'Platform şu an istekleri engelliyor. Lütfen limonları kabul edip tekrar deneyin! 🍋'}), 429
        return jsonify({'error': f'Video işlenemedi: {error_msg}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
