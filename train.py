#!/usr/bin/env python3
"""
Style-Aware Multitask Adapters with Catastrophic Forgetting Resilience
Научная новизна: одновременное обучение 4 стилей с минимальной интерференцией
"""

import torch
import json
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, PeftModel
import pandas as pd
import numpy as np

class MultiStyleExpert:
    """Класс для управления 4 экспертами-стилями"""
    
    def __init__(self, base_model="sberbank-ai/rugpt3small_based_on_gpt2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🔧 Устройство: {self.device}")
        
        # Загружаем базовую модель ОДИН РАЗ
        print("🔄 Загрузка базовой модели SberAI...")
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.base_model = AutoModelForCausalLM.from_pretrained(
            base_model,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None
        )
        
        # Замораживаем базовую модель
        for param in self.base_model.parameters():
            param.requires_grad = False
        
        self.styles = ["friendly", "formal", "empathetic", "humorous"]
        self.experts = {}
        
    def create_experts(self):
        """Создаем 4 независимых эксперта (LoRA адаптера)"""
        print("🎭 Создание 4 стилевых экспертов...")
        
        for style in self.styles:
            # Конфигурация LoRA ДЛЯ КАЖДОГО СТИЛЯ
            lora_config = LoraConfig(
                r=4,  # Меньше rank для CPU
                lora_alpha=8,
                target_modules=["attn.c_attn", "attn.c_proj"],  # Только основные модули
                lora_dropout=0.1,  # Больше дропаута для регуляризации
                bias="none",
                task_type="CAUSAL_LM",
            )
            
            # Создаем адаптер НА БАЗОВОЙ МОДЕЛИ
            expert_model = get_peft_model(self.base_model, lora_config)
            self.experts[style] = expert_model
            print(f"   ✅ Эксперт '{style}' создан")
            
    def train_expert(self, style_name, data_path="/content/data/my_style_data.json"):
        """Обучаем одного эксперта на его стилевых данных"""
        print(f"\n Обучение эксперта: {style_name}")
        
        # Загружаем данные
        with open(data_path, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
        
        style_data = all_data.get(style_name, [])
        
        if not style_data:
            print(f"   ⚠️ Нет данных для стиля {style_name}")
            return
        
        # Подготовка данных
        texts = []
        for item in style_data:
            prompt = f"Стиль: {style_name}\nКонтекст: {item['context']}\nОтвет: {item['response']}"
            texts.append(prompt)
        
        # Токенизация
        inputs = self.tokenizer(
            texts,
            truncation=True,
            max_length=256,
            padding="max_length",
            return_tensors="pt"
        )
        
        # Простой цикл обучения (для демо)
        expert = self.experts[style_name]
        expert.train()
        
        optimizer = torch.optim.AdamW(expert.parameters(), lr=1e-4)
        
        print(f"   📊 Примеров: {len(texts)}")
        
        for epoch in range(3):  # 3 эпохи
            total_loss = 0
            
            inputs_device = {k: v.to(self.device) for k, v in inputs.items()}
            outputs = expert(**inputs_device, labels=inputs_device['input_ids'])
            
            loss = outputs.loss
            total_loss += loss.item()
            
            # Backward pass
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            
            print(f"   Эпоха {epoch+1}, Loss: {loss.item():.4f}")
        
        # Сохраняем ТОЛЬКО адаптер
        expert.save_pretrained(f"adapters/{style_name}")
        print(f"   💾 Адаптер '{style_name}' сохранен")
        
    def run_training(self):
        """Запуск полного обучения"""
        print("="*50)
        print("🎓 НАЧАЛО ОБУЧЕНИЯ MULTI-STYLE EXPERTS")
        print("="*50)
        
        # Создаем экспертов
        self.create_experts()
        
        # Обучаем каждого эксперта
        for style in self.styles:
            self.train_expert(style)
        
        print("\n" + "="*50)
        print("✅ ОБУЧЕНИЕ ЗАВЕРШЕНО!")
        print("="*50)
        
    def test_experts(self):
        """Тестируем всех экспертов"""
        print("\n🧪 ТЕСТИРОВАНИЕ ЭКСПЕРТОВ")
        print("-"*30)
        
        test_contexts = [
            "Привет! Как дела?",
            "Добрый день, мне нужна помощь",
            "Я так устал от работы...",
            "Скучно сидеть дома"
        ]
        
        for context in test_contexts:
            print(f"\n📝 Контекст: {context}")
            
            for style in self.styles:
                # Загружаем адаптер
                expert = PeftModel.from_pretrained(
                    self.base_model, 
                    f"adapters/{style}"
                )
                expert.eval()
                
                # Генерация
                prompt = f"Стиль: {style}\nКонтекст: {context}\nОтвет:"
                inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
                
                with torch.no_grad():
                    outputs = expert.generate(
                        **inputs,
                        max_length=100,
                        temperature=0.7,
                        do_sample=True,
                        pad_token_id=self.tokenizer.eos_token_id
                    )
                
                response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                response = response.split("Ответ:")[-1].strip()
                
                print(f"   {style.upper()}: {response[:50]}...")

# Запуск
if __name__ == "__main__":
    expert_system = MultiStyleExpert()
    expert_system.run_training()
    expert_system.test_experts()