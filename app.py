from flask import Flask, request, jsonify, render_template
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

    # 1. Yedek API (David Cyril Tech)
    try:
        api_url = f"https://apis.davidcyriltech.my.id/download?url={url}"
        response = requests.get(api_url, timeout=8)
        res_data = response.json()
        if res_data.get("status") == 200:
            download_link = res_data.get("result", {}).get("video") or res_data.get("result", {}).get("download_url")
            if download_link:
                return jsonify({'success': True, 'title': 'LemonFetch Video', 'download_url': download_link})
    except Exception:
        pass

    # 2. Yedek API (TikWM Alternatif)
    try:
        tikwm_url = f"https://www.tikwm.com/api/?url={url}"
        response = requests.get(tikwm_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        res_data = response.json()
        if res_data.get("code") == 0:
            download_link = res_data.get("data", {}).get("play")
            if download_link:
                return jsonify({'success': True, 'title': 'LemonFetch Video', 'download_url': download_link})
    except Exception:
        pass

    return jsonify({'error': 'TikTok/Instagram şu an sunucu IP adresini engelliyor. Lütfen daha sonra tekrar deneyin.'}), 429

if __name__ == '__main__':
    app.run(debug=True)
