from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get-video', methods=['POST'])
def get_video():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'Lütfen bir bağlantı girin.'}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Doğrudan video bağlantısını (CDN URL) yakalıyoruz
            video_url = info.get('url') or (info.get('formats') and info.get('formats')[-1].get('url'))
            
            if not video_url:
                return jsonify({'error': 'Video bağlantısı çözülemedi.'}), 500
                
            return jsonify({'success': True, 'download_url': video_url})
            
    except Exception as e:
        return jsonify({'error': 'Video indirilemedi. Bağlantıyı kontrol edin.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
