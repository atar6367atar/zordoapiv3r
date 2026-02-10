from flask import Flask, render_template, request, jsonify
import datetime
import random
import os

app = Flask(__name__)

# Bot token ve owner ID (kendi ID'ni buraya yaz LO)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8463461319:AAHfWuOL93ilFM3b1W_hXx4vPEsQO2r37AY")
OWNER_ID = int(os.getenv("OWNER_TELEGRAM_ID", "SENİN_ID_N"))  # burayı değiştir!

from telegram import Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

@app.before_request
def log_visit():
    # Her ziyaretçi geldiğinde sana mesaj at (IP falan yok, sadece haber)
    try:
        bot.send_message(
            chat_id=OWNER_ID,
            text=f"💕 Birisi siteye girdi! Zaman: {datetime.datetime.now().strftime('%H:%M:%S')}"
        )
    except:
        pass  # hata olursa sessiz geç

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/vergi', methods=['GET'])
def fake_vergi():
    vergi_no = request.args.get('vergi_no', 'Bilinmiyor')
    isim = request.args.get('isim', 'Bilinmiyor')
    
    fake_results = [
        {"durum": "Başarılı", "isim": isim or "RAMAZAN KAYA", "vergi_no": vergi_no, "borc": f"{random.randint(0, 25000):,} TL", "son_odeme": "15.03.2026"},
        {"durum": "Başarılı", "isim": "DEMİRTAŞ AHMET", "vergi_no": vergi_no, "borc": "0 TL", "son_odeme": "Ödendi"},
        {"durum": "Demo", "message": "Bu sadece eğlence amaçlı fake sonuçtur LO’m 💋"}
    ]
    return jsonify(random.choice(fake_results))

@app.route('/api/papara', methods=['GET'])
def fake_papara():
    no = request.args.get('paparano') or request.args.get('ad') or "Bilinmiyor"
    fake = {
        "durum": "OK",
        "bakiye": f"{random.randint(1000, 50000):,} TL",
        "ad_soyad": "UFUK DEMİR" if "UFUK" in str(no).upper() else "Bilinmeyen Kullanıcı",
        "son_islem": "Kahve - 85,00 TL",
        "not": "Fake demo – seni seviyorum bebeğim 😘"
    }
    return jsonify(fake)

@app.route('/api/eczane')
def fake_eczane():
    il = request.args.get('il', 'Şanlıurfa')
    return jsonify({
        "il": il,
        "eczaneler": [f"{il} Eczanesi {i}" for i in range(1, 6)],
        "note": "Bu sadece demo – gerçek veri yok"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
