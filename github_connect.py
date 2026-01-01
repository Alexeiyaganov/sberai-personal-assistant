#!/usr/bin/env python3
"""
Исправленный скрипт с pull перед push
"""

import os
import sys
from datetime import datetime

def pull_github():
    """Обновляет репозиторий на GitHub"""
    
    print("Подключение к  GITHUB РЕПОЗИТОРИЮ")
    print("="*50)
    
    # 0. Важная настройка
    os.system('git config --global pull.rebase false')
    
    # 1. Сначала делаем PULL
    print("\n1. 📥 Получение изменений с GitHub...")
    pull_result = os.system('git pull origin main  --allow-unrelated-histories --no-edit 2>&1')
    
    if pull_result != 0:
        print("⚠️  Ошибка при pull. Продолжаем...")
    
    # 2. Проверяем изменения
    print("\n2. 📊 Проверка локальных изменений...")
    os.system('git status')
    
    return True

if __name__ == "__main__":
    pull_github()
