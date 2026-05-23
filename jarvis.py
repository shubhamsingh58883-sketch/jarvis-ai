import requests, json, os, subprocess

API_KEY = ""
URL = "https://api.groq.com/openai/v1/chat/completions"
history = []

SYSTEM = """Tu JARVIS hai. Hinglish mein baat kar. User ko Boss bol.
Agar user phone control karna chahe toh inn commands ka use kar:
[CALL:number] - call karna
[SMS:number:message] - sms bhejna  
[FLASH:on/off] - flashlight
[VOLUME:0-15] - volume set karna
[OPEN:app] - app kholna jaise youtube,whatsapp,chrome
[BATTERY] - battery check
[VIBRATE] - vibrate karna
Har response mein agar action chahiye toh command likhna."""

def do_action(text):
    import re
    if '[CALL:' in text:
        num = re.search(r'\[CALL:(.+?)\]', text)
        if num:
            os.system(f'termux-telephony-call {num.group(1)}')
            print(f'>> Call kar raha hoon {num.group(1)} pe...')
    if '[SMS:' in text:
        match = re.search(r'\[SMS:(.+?):(.+?)\]', text)
        if match:
            os.system(f'termux-sms-send -n {match.group(1)} "{match.group(2)}"')
            print(f'>> SMS bheja!')
    if '[FLASH:on]' in text.lower():
        os.system('termux-torch on')
        print('>> Flashlight ON!')
    if '[FLASH:off]' in text.lower():
        os.system('termux-torch off')
        print('>> Flashlight OFF!')
    if '[BATTERY]' in text:
        result = subprocess.getoutput('termux-battery-status')
        print(f'>> Battery: {result}')
    if '[VIBRATE]' in text:
        os.system('termux-vibrate -d 500')
        print('>> Vibrate!')
    if '[VOLUME:' in text:
        vol = re.search(r'\[VOLUME:(\d+)\]', text)
        if vol:
            os.system(f'termux-volume music {vol.group(1)}')
            print(f'>> Volume set: {vol.group(1)}')
    if '[OPEN:' in text:
        app = re.search(r'\[OPEN:(.+?)\]', text)
        if app:
            apps = {
                'youtube': 'com.google.android.youtube',
                'whatsapp': 'com.whatsapp',
                'chrome': 'com.android.chrome',
                'instagram': 'com.instagram.android',
                'camera': 'com.android.camera',
                'settings': 'com.android.settings',
                'maps': 'com.google.android.apps.maps'
            }
            pkg = apps.get(app.group(1).lower(), app.group(1))
            os.system(f'termux-open --content-type "text/plain" || am start -n {pkg}/.MainActivity 2>/dev/null 1>/dev/null || monkey -p {pkg} 1 2>/dev/null 1>/dev/null')
            print(f'>> {app.group(1)} open kar raha hoon!')

def chat(user_input):
    history.append({"role": "user", "content": user_input})
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": SYSTEM}] + history[-10:],
        "max_tokens": 1024,
        "temperature": 0.8
    }
    r = requests.post(URL, headers=headers, json=data)
    reply = r.json()["choices"][0]["message"]["content"]
    history.append({"role": "assistant", "content": reply})
    do_action(reply)
    return reply

print("=" * 40)
print("   JARVIS ONLINE - Ready Boss!")
print("   Phone Control Active!")
print("=" * 40)
print("Commands: call karo, msg bhejo, flash on/off")
print("         youtube kholo, battery check karo")
print("=" * 40)

while True:
    try:
        u = input("\nAap: ").strip()
        if u.lower() in ["bye","exit","quit"]:
            print("JARVIS: Alvida Boss!")
            break
        if u:
            reply = chat(u)
            clean = reply.replace('[CALL:', '').replace('[SMS:', '').replace('[FLASH:', '').replace('[BATTERY]', '').replace('[VIBRATE]', '').replace('[VOLUME:', '').replace('[OPEN:', '')
            print("JARVIS: " + clean)
    except KeyboardInterrupt:
        print("\nJARVIS: Alvida Boss!")
        break
