from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Налаштування підключення до MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["cat_database"]
cats = db["cats"]

def print_all_cats():
    """Виводить всі записи з колекції cats."""
    try:
        all_cats = cats.find()
        for cat in all_cats:
            print(cat)
    except PyMongoError as e:
        print("Error accessing database:", e)

def find_cat_by_name():
    """Дозволяє користувачу ввести ім'я кота та виводить інформацію про цього кота."""
    name = input("Enter the name of the cat: ")
    try:
        cat = cats.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print("No cat found with the name", name)
    except PyMongoError as e:
        print("Error accessing database:", e)

def update_cat_age():
    """Дозволяє користувачеві оновити вік кота за ім'ям."""
    name = input("Enter the name of the cat to update: ")
    age = int(input("Enter the new age: "))
    try:
        result = cats.update_one({"name": name}, {"$set": {"age": age}})
        if result.modified_count:
            print("Cat age updated.")
        else:
            print("No cat updated.")
    except PyMongoError as e:
        print("Error updating database:", e)

def add_feature_to_cat():
    """Дозволяє додати нову характеристику до списку features кота за ім'ям."""
    name = input("Enter the name of the cat to update: ")
    feature = input("Enter the new feature to add: ")
    try:
        result = cats.update_one({"name": name}, {"$addToSet": {"features": feature}})
        if result.modified_count:
            print("Feature added to cat.")
        else:
            print("No feature added.")
    except PyMongoError as e:
        print("Error updating database:", e)

def delete_cat_by_name():
    """Видаляє запис з колекції за ім'ям тварини."""
    name = input("Enter the name of the cat to delete: ")
    try:
        result = cats.delete_one({"name": name})
        if result.deleted_count:
            print("Cat deleted.")
        else:
            print("No cat found to delete.")
    except PyMongoError as e:
        print("Error deleting from database:", e)

def delete_all_cats():
    """Видаляє всі записи з колекції."""
    try:
        result = cats.delete_many({})
        print(f"Deleted {result.deleted_count} cats.")
    except PyMongoError as e:
        print("Error deleting from database:", e)

def main():
    while True:
        print("\nCAT DATABASE OPERATIONS:")
        print("1 - Print All Cats")
        print("2 - Find Cat by Name")
        print("3 - Update Cat Age")
        print("4 - Add Feature to Cat")
        print("5 - Delete Cat by Name")
        print("6 - Delete All Cats")
        print("0 - Exit")
        choice = input("Choose an operation: ")

        if choice == "1":
            print_all_cats()
        elif choice == "2":
            find_cat_by_name()
        elif choice == "3":
            update_cat_age()
        elif choice == "4":
            add_feature_to_cat()
        elif choice == "5":
            delete_cat_by_name()
        elif choice == "6":
            delete_all_cats()
        elif choice == "0":
            print("Exiting the program.")
            break
        else:
            print("Invalid input, please choose a valid operation.")

if __name__ == "__main__":
    main()
