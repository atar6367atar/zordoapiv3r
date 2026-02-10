from flask import Flask, request, jsonify
import datetime
import random
import os
from telegram import Bot

app = Flask(__name__)

# Render Environment Variables'dan oku (Render panelinde tanımlı olmalı)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_TELEGRAM_ID")

# Botu başlat (hata olursa sessiz geç)
bot = None
if TELEGRAM_BOT_TOKEN and OWNER_ID:
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        OWNER_ID = int(OWNER_ID)
    except:
        pass

# HTML tamamen burada (templates klasörüne gerek yok)
HOME_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>F3 LookUp - Demo Panel</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: system-ui, -apple-system, sans-serif;
        }
        .card {
            background: rgba(0,0,0,0.45);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 16px;
            max-width: 520px;
            padding: 2.5rem;
        }
        .form-control {
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
        }
        .form-control:focus {
            background: rgba(255,255,255,0.15);
            border-color: #0d6efd;
            box-shadow: 0 0 0 0.25rem rgba(13,110,253,.25);
        }
        pre {
            background: rgba(0,0,0,0.65);
            color: #e0e0ff;
            padding: 1.2rem;
            border-radius: 10px;
            font-size: 0.95rem;
        }
    </style>
</head>
<body>
    <div class="card shadow-lg">
        <h2 class="text-center mb-4 fw-bold">F3 LookUp Sistemi</h2>
        <p class="text-center text-light opacity-75 mb-4">Demo Modu – LO’m için özel 💕</p>
        
        <input type="text" id="q" class="form-control mb-3 py-2" placeholder="Vergi no, isim veya Papara no gir">
        <button class="btn btn-primary w-100 py-3 fw-bold" onclick="sorgula()">SORGULA</button>
        
        <div id="loading" class="text-center mt-4" style="display:none;">
            <div class="spinner-border text-primary" style="width:2.8rem;height:2.8rem;"></div>
            <p class="mt-3">Veriler taranıyor, biraz bekle bebeğim...</p>
        </div>
        
        <pre id="result" class="mt-4" style="display:none;"></pre>
    </div>

    <script>
        async function sorgula() {
            const val = document.getElementById('q').value.trim();
            if (!val) return alert('Bir şeyler yaz aşkım 😘');
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            
            try {
                const res = await fetch(`/api/vergi?vergi_no=${encodeURIComponent(val)}`);
                const data = await res.json();
                document.getElementById('result').textContent = JSON.stringify(data, null, 2);
                document.getElementById('result').style.display = 'block';
            } catch (err) {
                alert('Demo sırasında ufak bir hata – seni çok seviyorum 💋');
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
    if bot and OWNER_ID:
        try:
            bot.send_message(
                chat_id=OWNER_ID,
                text=f"💕 Yeni ziyaretçi siteye girdi! Saat: {datetime.datetime.now().strftime('%H:%M:%S')}"
            )
        except Exception as e:
            pass  # hata olursa sessiz
    return HOME_HTML

@app.route('/api/vergi', methods=['GET'])
def fake_vergi():
    q = request.args.get('vergi_no', 'Bilinmiyor')
    return jsonify({
        "durum": "Demo Başarılı",
        "sorgu": q,
        "isim": random.choice(["RAMAZAN KAYA", "UFUK DEMİR", "AHMET YILMAZ", "FATMA ŞAHİN"]),
        "vergi_borcu": f"{random.randint(0, 32000):,} TL",
        "son_odeme_tarihi": datetime.date.today().strftime("%d.%m.%Y"),
        "not": "Bu tamamen sahte ve eğlence amaçlı bir sonuçtur LO’m 😏"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
