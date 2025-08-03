import json

def admin_login():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    try:
        with open("admins.json", "r") as file:
            admins = json.load(file)

        for admin in admins.get("admins", []):
            if admin["username"] == username and admin["password"] == password:
                print(f"✅ Welcome, {username}!")
                return True
        
        print("❌ Invalid credentials. Please try again.")
        return False

    except FileNotFoundError:
        print("⚠️ Admins file not found.")
        return False

def admin_menu():
    while True:
        print("\n📋 Admin Menu:")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student by ID")
        print("4. Edit Student Record")
        print("5. Delete Student")
        print("6. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            add_student()           # from student.py
        elif choice == "2":
            view_students()         # from student.py
        elif choice == "3":
            search_student()        # 👈 you’ll define this in student.py
        elif choice == "4":
            edit_student()          # 👈 also goes in student.py
        elif choice == "5":
            delete_student()        # 👈 student.py again!
        elif choice == "6":
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid choice!")