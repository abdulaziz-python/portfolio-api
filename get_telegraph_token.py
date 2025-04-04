#!/usr/bin/env python
import requests
import sys
import os
from dotenv import load_dotenv

def get_telegraph_token(short_name, author_name=None):
    """
    Telegraph API dan token olish
    """
    url = "https://api.telegra.ph/createAccount"
    params = {
        "short_name": short_name,
        "author_name": author_name or short_name
    }
    
    try:
        r = requests.get(url, params=params)
        resp = r.json()
        
        if resp.get("ok"):
            return resp["result"]["access_token"]
        else:
            return f"Xato: {resp.get('error')}"
    except Exception as e:
        return f"Xato: {str(e)}"

def save_to_env(token):
    """
    Tokenni .env faylga saqlash
    """
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            lines = f.readlines()
        
        with open(".env", "w") as f:
            token_line_exists = False
            for line in lines:
                if line.startswith("TELEGRAPH_TOKEN="):
                    f.write(f"TELEGRAPH_TOKEN={token}\n")
                    token_line_exists = True
                else:
                    f.write(line)
            
            if not token_line_exists:
                f.write(f"\nTELEGRAPH_TOKEN={token}\n")
    else:
        with open(".env", "w") as f:
            f.write(f"TELEGRAPH_TOKEN={token}\n")
    
    return True

if __name__ == "__main__":
    load_dotenv()
    
    if len(sys.argv) < 2:
        print("Foydalanish: python get_telegraph_token.py <short_name> [author_name]")
        sys.exit(1)
    
    short_name = sys.argv[1]
    author_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    token = get_telegraph_token(short_name, author_name)
    
    if token.startswith("Xato"):
        print(token)
        sys.exit(1)
    
    print(f"Telegraph token muvaffaqiyatli yaratildi: {token}")
    
    save_result = save_to_env(token)
    if save_result:
        print("Token .env fayliga saqlandi")
    
    print("\nUshbu tokendan foydalanish uchun:")
    print("1. .env faylidagi TELEGRAPH_TOKEN qiymatini to'g'ri o'rnating")
    print("2. Serverni qayta ishga tushiring")
    print("3. Yangi blog post yoki loyiha qo'shganingizda, ular avtomatik ravishda Telegraph'ga joylashtiriladi") 