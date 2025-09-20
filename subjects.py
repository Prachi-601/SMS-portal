import json

def load_subjects():
    try:
        with open("subjects.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_subjects(data):
    with open("subjects.json", "w") as f:
        json.dump(data, f, indent=4)

def add_subjects_for_class(class_name, admin_id):
    subjects = []
    print(f"Enter subjects for {class_name} (type 'done' to finish):")
    while True:
        sub = input("Subject: ").strip()
        if sub.lower() == "done":
            break
        subjects.append(sub)

    data = load_subjects()
    if admin_id not in data:
        data[admin_id] = {}

    data[admin_id][class_name] = subjects
    save_subjects(data)
    print(f"✅ Subjects for {class_name} saved successfully.")

def view_subjects_for_class(class_name, admin_id):
    data = load_subjects()
    subjects = data.get(admin_id, {}).get(class_name, [])
    if subjects:
        print(f"\nSubjects for {class_name}:")
        for sub in subjects:
            print(f"- {sub}")
    else:
        print("⚠️ No subjects found for this class.")

# 🧪 CLI block
if __name__ == "__main__":
    admin_id = input("Enter your admin ID: ").strip()
    while True:
        print("\n📚 Subject Manager")
        print("1. Add subjects for a class")
        print("2. View subjects for a class")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            class_name = input("Enter class name (e.g., FYBSc CS): ").strip()
            add_subjects_for_class(class_name, admin_id)
        elif choice == "2":
            class_name = input("Enter class name to view: ").strip()
            view_subjects_for_class(class_name, admin_id)
        elif choice == "3":
            print("👋 Exiting Subject Manager.")
            break
        else:
            print("❌ Invalid choice. Try again.")