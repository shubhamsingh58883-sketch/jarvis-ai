import sys
import os

# ... tumhara baaki ka code yahan rahega ...

def do_action(text):
    t = text.lower()
    if 'youtube' in t:
        os.system("termux-open-url https://www.youtube.com")
        return "YouTube khol raha hoon"
    # Yahan aur commands add kar sakte ho
    return "Command samajh nahi aayi"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # MacroDroid ka notification text utha raha hai
        user_input = " ".join(sys.argv[1:])
        # Agar 'jarvis' text mein hoga tabhi action lega
        if "jarvis" in user_input.lower():
            print(do_action(user_input))

