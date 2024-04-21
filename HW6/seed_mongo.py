from pymongo import MongoClient
from faker import Faker
import random

def main():
    # Ініціалізація Faker
    fake = Faker()

    # Підключення до MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["cat_database"]
    cats = db["cats"]

    # Потенційні характеристики для котів
    possible_features = [
        "ласкавий", "грайливий", "тендітний", 
        "сонливий", "енергійний", "гладкошерстий",
        "боязкий", "незалежний", "пухнастий"
    ]

    # Генерація випадкових котів
    for _ in range(12):
        features = random.sample(possible_features, k=3)  # Вибираємо 3 випадкові характеристики
        cat_document = {
            "name": fake.first_name(),
            "age": random.randint(1, 15),  # Вік кота від 1 до 15 років
            "features": features
        }

        # Додавання документа до колекції
        try:
            result = cats.insert_one(cat_document)
            print(f"Added Cat with ID: {result.inserted_id}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
