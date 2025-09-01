import json

# 🔐 Admin Login
def admin_login():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    try:
        with open("admins.json", "r") as file:
            admins = json.load(file)

        for admin in admins.get("admins", []):
            if admin["username"] == username and admin["password"] == password:
                print(f"✅ Welcome, {username}!")
                return admin  # Return full admin data
        
        print("❌ Invalid credentials. Please try again.")
        return None

    except FileNotFoundError:
        print("⚠️ Admins file not found.")
        return None


# 👨‍🏫 Teacher Login
def teacher_login():
    username = input("Enter teacher username: ")
    password = input("Enter teacher password: ")

    try:
        with open("teachers.json", "r") as file:
            teachers = json.load(file)

        for teacher in teachers.get("teachers", []):
            if teacher["username"] == username and teacher["password"] == password:
                print(f"✅ Welcome, {username}!")
                return teacher
        
        print("❌ Invalid credentials.")
        return None

    except FileNotFoundError:
        print("⚠️ Teachers file not found.")
        return None


# 🎓 Student Login
def student_login():
    username = input("Enter student username: ")
    password = input("Enter student password: ")

    try:
        with open("students.json", "r") as file:
            students = json.load(file)

        for student in students.get("students", []):
            if student["username"] == username and student["password"] == password:
                print(f"✅ Welcome, {username}!")
                return student
        
        print("❌ Invalid credentials.")
        return None

    except FileNotFoundError:
        print("⚠️ Students file not found.")
        return None


# 🔄 Unified Login Dispatcher
def login(role):
    if role == "admin":
        return admin_login()
    elif role == "teacher":
        return teacher_login()
    elif role == "student":
        return student_login()
    else:
        print("❌ Invalid role.")
        return None
