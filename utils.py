import json

def get_student_by_id(student_id, admin_id):
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
            for student in data.get("students", []):
                if student.get("id") == student_id and student.get("admin_id") == admin_id:
                    return student
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return None

def get_student_by_class(class_name, admin_id):
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
            return [
                student for student in data.get("students", [])
                if student.get("class", "").strip().lower() == class_name.strip().lower()
                and student.get("admin_id") == admin_id
            ]
    except (FileNotFoundError, json.JSONDecodeError):
        return []