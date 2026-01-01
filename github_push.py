#!/usr/bin/env python3
"""
Push on github
"""

import os
import sys
from datetime import datetime

def update_github():
    """Обновляет репозиторий на GitHub"""
    
    print("🔄 ОБНОВЛЕНИЕ GITHUB РЕПОЗИТОРИЯ")
    print("="*50)
       
    
    # 4. Добавляем все файлы
    print("\n4. 📦 Добавление файлов...")
    os.system('git add .')
    
    # 5. Коммитим
    print("\n5. 💾 Создание коммита...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    commit_msg = f"Обновление: {timestamp}"
    os.system(f'git commit -m "{commit_msg}"')
    
    # 6. Пушим на GitHub
    print("\n6. 📤 Отправка на GitHub...")
    push_result = os.system('git push origin main')
    
    if push_result == 0:
        print("\n" + "="*50)
        print("✅ УСПЕШНО ОБНОВЛЕНО НА GITHUB!")
        print(f"📎 https://github.com/Alexeiyaganov/sberai-personal-assistant")
        print("="*50)
    else:
        print("\n❌ Ошибка при пуше!")
        print("Пробуем принудительно...")
        force_result = os.system('git push -f origin main')
        
        if force_result == 0:
            print("✅ Принудительный пуш успешен!")
        else:
            print("⚠️  Даже принудительно не получилось")
    
    return True

if __name__ == "__main__":
    update_github()
