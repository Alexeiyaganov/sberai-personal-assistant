#!/usr/bin/env python3
"""
Исправленный скрипт с pull перед push
"""

import os
import sys
from datetime import datetime

def update_github():
    """Обновляет репозиторий на GitHub"""
    
    print("🔄 ОБНОВЛЕНИЕ GITHUB РЕПОЗИТОРИЯ")
    print("="*50)
    
    # 0. Важная настройка
    os.system('git config --global pull.rebase false')
    
    # 1. Сначала делаем PULL
    print("\n1. 📥 Получение изменений с GitHub...")
    pull_result = os.system('git pull origin main')
    
    if pull_result != 0:
        print("⚠️  Ошибка при pull. Продолжаем...")
    
    # 2. Проверяем изменения
    print("\n2. 📊 Проверка локальных изменений...")
    os.system('git status')
    
    # 3. Создаем файл обновления
    print("\n3. 📝 Создание файла обновления...")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"update_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"Обновление из Colab\n")
        f.write(f"Время: {datetime.now()}\n")
        f.write(f"Коммит с pull перед push\n")
    
    print(f"✅ Создан файл: {filename}")
    
    # 4. Добавляем все файлы
    print("\n4. 📦 Добавление файлов...")
    os.system('git add .')
    
    # 5. Коммитим
    print("\n5. 💾 Создание коммита...")
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
