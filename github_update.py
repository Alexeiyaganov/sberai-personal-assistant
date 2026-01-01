#!/usr/bin/env python3
"""
Простой скрипт для обновления GitHub репозитория
"""

import os
import sys
from datetime import datetime

def update_github():
    """Обновляет репозиторий на GitHub"""
    
    print("🔄 ОБНОВЛЕНИЕ GITHUB РЕПОЗИТОРИЯ")
    print("="*50)
    
    # 1. Настройка пользователя (если еще не настроено)
    os.system('git config --global user.name "Alexeiyaganov" 2>/dev/null')
    os.system('git config --global user.email "btls3@yandex.ru" 2>/dev/null')
    
    # 2. Проверяем, есть ли изменения для коммита
    print("\n1. 📊 Проверка изменений...")
    os.system('git status')
    
    # 3. Создаем файл с меткой времени, если нет изменений
    print("\n2. 📝 Создание файла обновления...")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"update_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"Обновление из Colab\n")
        f.write(f"Время: {datetime.now()}\n")
        f.write(f"Файл создан автоматически\n")
    
    print(f"✅ Создан файл: {filename}")
    
    # 4. Добавляем все файлы
    print("\n3. 📦 Добавление файлов...")
    os.system('git add .')
    
    # 5. Коммитим
    print("\n4. 💾 Создание коммита...")
    commit_msg = f"Обновление: {timestamp}"
    os.system(f'git commit -m "{commit_msg}"')
    
    # 6. Пушим на GitHub
    print("\n5. 📤 Отправка на GitHub...")
    push_result = os.system('git push origin main')
    
    if push_result == 0:
        print("\n" + "="*50)
        print("✅ УСПЕШНО ОБНОВЛЕНО НА GITHUB!")
        print(f"📎 https://github.com/Alexeiyaganov/sberai-personal-assistant")
        print("="*50)
    else:
        print("\n❌ Ошибка при пуше!")
        print("Попробуйте:")
        print("!git push -u origin main")
    
    return push_result == 0

if __name__ == "__main__":
    update_github()
