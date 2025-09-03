import json
import os
from student import add_student, view_students, search_student,search_student_by_name, edit_student, edit_student_by_name,delete_specific_student_by_name,sort_students_by_course


# 🔧 Create the JSON file if it doesn’t exist or is empty
if not os.path.exists("admins.json") or os.stat("admins.json").st_size == 0:
    with open("admins.json", "w") as f:
        json.dump({}, f)

# 🧭 Main login menu
def main_login():
    print("\n🔐 Welcome to Portal")
    print("1. Admin Login")
    print("2. Admin Signup")
    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        admin_login()
    elif choice == "2":
        admin_signup()
    else:
        print("❌ Invalid choice!")

# 👩‍💼 Admin login function
def admin_login():
    username = input("Admin username: ").lower()
    password = input("Password: ")

    with open("admins.json", "r") as f:
        data = json.load(f)
        admins = data.get("admins", [])

    for admin in admins:
        if admin["username"] == username and admin["password"] == password:
            print("✅ Welcome, Principal!")
            admin_menu()
            return

    print("❌ Wrong credentials")

# ✍️ Admin signup function
def admin_signup():
    username = input("Create admin username: ").lower()
    password = input("Create password: ")

    with open("admins.json", "r") as f:
        data = json.load(f)

    admins = data.get("admins", [])

    # Check if username already exists
    for admin in admins:
        if admin["username"] == username:
            print("⚠️ Admin already exists!")
            return

    # Add new admin
    admins.append({
        "username": username,
        "password": password
    })

    with open("admins.json", "w") as f:
        json.dump({"admins": admins}, f, indent=2)

    print("✅ Admin signup successful!")

def admin_menu():
    while True:
        print("\n📋 Admin Menu:")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student (by ID or Name)")
        print("4. Edit Student Record (by ID or Name)")
        print("5. Delete Student")
        print("6. Logout")
        print("7. Sort Students by Class")


        choice = input("Choose an option: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            print("\n🔍 Search by:")
            print("1. ID")
            print("2. Name")
            sub_choice = input("Choose (1/2): ")
            if sub_choice == "1":
                search_student()
            elif sub_choice == "2":
                search_student_by_name()
            else:
                print("❌ Invalid search option.")

        elif choice == "4":
            print("\n✏️ Edit by:")
            print("1. ID")
            print("2. Name")
            sub_choice = input("Choose (1/2): ")
            if sub_choice == "1":
                edit_student()
            elif sub_choice == "2":
                edit_student_by_name()
            else:
                print("❌ Invalid edit option.")

        elif choice == "5":
            delete_specific_student_by_name()
        elif choice == "6":
            print("👋 Logging out...")
            break
        elif choice == "7":
          sort_students_by_course()
        else:
            print("❌ Invalid choice!")
# ▶️ Start the portal
main_login()
