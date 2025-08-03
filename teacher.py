import json

def add_teacher():
    # Load existing data
    try:
        with open("teachers.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"teachers": []}

    # Input teacher details
    name = input("Enter teacher name: ").strip()
    department = input("Enter department: ").strip()
    post = input("Enter post (e.g., Assistant Professor, HOD): ").strip()
    subject = input("Enter subject taught: ").strip()

    # Optional duplicate check
    for teacher in data["teachers"]:
        if (teacher["name"].lower() == name.lower() and 
            teacher["department"].lower() == department.lower() and 
            teacher["post"].lower() == post.lower() and
            teacher["subject"].lower() == subject.lower()):
            print("Teacher already exists.")
            return

    # Add new teacher
    new_teacher = {
        "name": name,
        "department": department,
        "post": post,
        "subject": subject
    }
    data["teachers"].append(new_teacher)

    # Save to JSON
    with open("teachers.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Teacher added successfully!")

def view_teachers():
    try:
        with open("teachers.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No teacher data found.")
        return

    teachers = data.get("teachers", [])
    if not teachers:
        print("No teacher records available.")
        return

    print("\n🎓 Teacher Records:")
    print("-" * 40)
    for teacher in teachers:
        print(f"Name: {teacher['name']}")
        print(f"Department: {teacher['department']}")
        print(f"Post: {teacher['post']}")
        print(f"Subject: {teacher['subject']}")
        print("-" * 40)
    print(f"Total teachers: {len(teachers)}\n")

if __name__ == "__main__":
    # add_teacher()
    view_teachers()
