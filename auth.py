import json

# 🔐 Admin Login
def admin_login():
    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()

    try:
        with open("admins.json", "r") as file:
            admins = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Admins file not found or corrupted.")
        return None

    for admin in admins.get("admins", []):
        if admin["username"] == username and admin["password"] == password:
            print(f"✅ Welcome, {username}!")
            return admin

    print("❌ Invalid credentials.")
    return None

def teacher_login():
    username = input("Enter teacher username: ").strip()
    password = input("Enter teacher password: ").strip()

    try:
        with open("teachers.json", "r") as file:
            raw = json.load(file)
            teachers = raw if isinstance(raw, dict) else {"teachers": raw}
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Teachers file not found or corrupted.")
        return None

    for teacher in teachers.get("teachers", []):
        if teacher["username"] == username and teacher["password"] == password:
            print(f"✅ Welcome, {teacher['name']}!")
            return teacher

    print("❌ Invalid credentials.")
    return None

# 🎓 Student Login
def student_login():
    username = input("Enter student username: ").strip()
    password = input("Enter student password: ").strip()

    try:
        with open("students.json", "r") as file:
            students = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Students file not found or corrupted.")
        return None

    for student in students.get("students", []):
        if student["username"] == username and student["password"] == password:
            print(f"✅ Welcome, {student['name']}!")
            return student

    print("❌ Invalid credentials.")
    return None

# 🔍 Get teacher by username
def get_teacher_by_username(username):
    try:
        with open("teachers.json", "r") as f:
            data = json.load(f)
            for teacher in data.get("teachers", []):
                if teacher["username"] == username:
                    return teacher
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Teacher records not found.")
    return None

# 🆕 Teacher Signup (HOD only)
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
    except (FileNotFoundError, json.JSONDecodeError):
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

# 🧪 CLI block
if __name__ == "__main__":
    print("🔐 Login Test")
    role = input("Login as (admin/teacher/student): ").strip().lower()
    user = login(role)
    if user:
        print(f"✅ Logged in as {role}: {user.get('name', user.get('username'))}")
