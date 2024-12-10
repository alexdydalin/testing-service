import os
import numpy as np
import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
from huggingface_hub import login

hf_token = "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"
os.environ['HF_TOKEN'] = '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'

# Загрузка данных
def load_data(data_folder):
    data = []
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(data_folder, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                girkin_code, java_code = content.split('###')
                data.append((girkin_code.strip(), java_code.strip()))
    return pd.DataFrame(data, columns=['girkin', 'java'])

# Подготовка модели
def prepare_model():
    model_name = "t5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False, use_fast=True)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    return tokenizer, model

# Обучение модели
def train_model(data):
    tokenizer, model = prepare_model()

    # Преобразование данных в формат для обучения
    inputs = tokenizer(data['girkin'].tolist(), return_tensors="pt", padding=True, truncation=True, max_length=512)
    labels = tokenizer(data['java'].tolist(), return_tensors="pt", padding=True, truncation=True, max_length=512).input_ids

    # Удаляем ненужные метки (если они равны -100)
    labels[labels == tokenizer.pad_token_id] = -100

    # Обучение модели
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

    for epoch in range(2):  # Количество эпох можно увеличить
        optimizer.zero_grad()
        outputs = model(input_ids=inputs['input_ids'], labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch + 1}, Loss: {loss.item()}")

    # Сохранение обученной модели
    model.save_pretrained("trained_t5_model")
    tokenizer.save_pretrained("trained_t5_model")

# Прогнозирование Java-кода из Girkin-кода
def predict_girkin_to_java(girkin_text):
    tokenizer = T5Tokenizer.from_pretrained("trained_t5_model", legacy=False, use_fast=True)
    model = T5ForConditionalGeneration.from_pretrained("trained_t5_model")

    input_ids = tokenizer.encode(girkin_text, return_tensors="pt", max_length=512, truncation=True)
    output_ids = model.generate(input_ids)

    java_code = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return java_code

# Основной код

data_folder = 'data'  # Папка с данными
data = load_data(data_folder)

# Обучение модели (раскомментируйте для обучения)
train_model(data)