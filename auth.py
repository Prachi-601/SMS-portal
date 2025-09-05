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

def get_teacher_by_username(username):
    try:
        with open("teachers.json", "r") as f:
            data = json.load(f)
            for teacher in data.get("teachers", []):
                if teacher["username"] == username:
                    return teacher
    except FileNotFoundError:
        print("⚠️ Teacher records not found.")
    return None

def teacher_signup(hod_verified=True):
    if not hod_verified:
        print("❌ Access denied. Only HOD can create teacher accounts.")
        return

    username = input("Enter teacher username: ").strip()
    password = input("Enter password (min 6 chars): ").strip()
    name = input("Enter full name: ").strip()
    subjects = input("Enter subjects (comma-separated): ").strip()

    if len(password) < 6:
        print("⚠️ Password too short.")
        return

    new_teacher = {
        "username": username,
        "password": password,
        "name": name,
        "subjects": [s.strip() for s in subjects.split(",")]
    }

    try:
        with open("teachers.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"teachers": []}

    for teacher in data["teachers"]:
        if teacher["username"] == username:
            print("⚠️ Username already exists.")
            return

    data["teachers"].append(new_teacher)

    with open("teachers.json", "w") as file:
        json.dump(data, file, indent=4)

    print(f"✅ Teacher account for {name} created successfully.")

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
