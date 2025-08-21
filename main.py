from auth import admin_login
from assignment import view_assignments

view_assignments()



if admin_login():
    print("🔓 Access granted to admin panel.")
else:
    print("🔐 Access denied.")

