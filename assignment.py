# assignment.py

import json
from datetime import datetime

def add_assignment(subject, topic, deadline):
    assignment = {
        "subject": subject,
        "topic": topic,
        "deadline": deadline,
        "created_on": str(datetime.now().date())
    }
    try:
        with open("assignments.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(assignment)

    with open("assignments.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Assignment added successfully.")

def view_assignments():
    try:
        with open("assignments.json", "r") as f:
            data = json.load(f)
            for a in data:
                print(f"Subject: {a['subject']}, Topic: {a['topic']}, Deadline: {a['deadline']}")
    except FileNotFoundError:
        print("No assignments found.")

def submit_assignment(student_id, subject, topic):
    submission = {
        "student_id": student_id,
        "subject": subject,
        "topic": topic,
        "submitted_on": str(datetime.now().date())
    }

    try:
        with open("assignment_submissions.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(submission)

    with open("assignment_submissions.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Submission recorded for Student ID: {student_id}")

def view_submissions():
    try:
        with open("assignment_submissions.json", "r") as f:
            data = json.load(f)
            # Sort by submitted_on date
            sorted_data = sorted(data, key=lambda x: x["submitted_on"])
            for s in sorted_data:
                print(f"Student ID: {s['student_id']}, Subject: {s['subject']}, Topic: {s['topic']}, Submitted on: {s['submitted_on']}")
    except FileNotFoundError:
        print("No submissions found.")

