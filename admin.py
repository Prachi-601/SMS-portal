import json
import os
from student import (
    add_student, view_students, search_student, search_student_by_name,
    edit_student, edit_student_by_name, delete_specific_student_by_name,
    get_student_by_id
)
from dashboard import student_dashboard
from attendance import get_monthly_attendance
from teacher import add_teacher, view_teachers

# 🔧 Create the JSON file if it doesn’t exist or is empty
if not os.path.exists("admins.json") or os.stat("admins.json").st_size == 0:
    with open("admins.json", "w") as f:
        json.dump({"admins": []}, f)

def main_login():
    print("\n🔐 Welcome to Admin Portal")
    print("1. Admin Login")
    print("2. Admin Signup")
    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        admin_login()
    elif choice == "2":
        admin_signup()
    else:
        print("❌ Invalid choice!")

def admin_login():
    username = input("Admin username: ").strip().lower()
    password = input("Password: ").strip()

    try:
        with open("admins.json", "r") as f:
            data = json.load(f)
            admins = data.get("admins", [])
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Admins file not found or corrupted.")
        return

    for admin in admins:
        if admin["username"] == username and admin["password"] == password:
            print("✅ Welcome, Admin!")
            admin_menu(admin)
            return

    print("❌ Wrong credentials")

def admin_signup():
    username = input("Create admin username: ").strip().lower()
    password = input("Create password: ").strip()

    try:
        with open("admins.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"admins": []}

    admins = data.get("admins", [])

    for admin in admins:
        if admin["username"] == username:
            print("⚠️ Admin already exists!")
            return

    admins.append({
        "username": username,
        "password": password
    })

    with open("admins.json", "w") as f:
        json.dump({"admins": admins}, f, indent=2)

    print("✅ Admin signup successful!")

def admin_menu(admin):
    while True:
        print(f"\n📋 Admin Menu ({admin['username']}):")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student by ID")
        print("4. Search Student by Name")
        print("5. Edit Student by ID")
        print("6. Edit Student by Name")
        print("7. Delete Student by Name")
        print("8. View Student Dashboard")
        print("9. View Monthly Attendance Summary")
        print("10. Add Teacher")
        print("11. View Teachers")
        print("12. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            search_student_by_name()
        elif choice == "5":
            edit_student()
        elif choice == "6":
            edit_student_by_name()
        elif choice == "7":
            delete_specific_student_by_name()
        elif choice == "8":
            try:
                student_id = int(input("Enter student ID to view dashboard: "))
            except ValueError:
                print("❌ Invalid ID format.")
                continue
            student = get_student_by_id(student_id)
            if student:
                student_dashboard(student["name"], student_id)
            else:
                print("❌ Student not found.")
        elif choice == "9":
            try:
                student_id = int(input("Enter student ID: "))
                month = int(input("Enter month (1-12): "))
                year = int(input("Enter year (e.g., 2025): "))
            except ValueError:
                print("❌ Invalid input.")
                continue
            student = get_student_by_id(student_id)
            if student:
                present, total = get_monthly_attendance(student_id, month, year)
                print(f"\n📅 Attendance Summary for {student['name']} ({month}/{year})")
                print(f"✅ Present: {present}")
                print(f"📌 Total Days: {total}")
                print(f"📊 Attendance %: {round((present/total)*100, 2) if total else 0}%")
            else:
                print("❌ Student not found.")
        elif choice == "10":
            add_teacher()
        elif choice == "11":
            view_teachers()
        elif choice == "12":
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main_login()
