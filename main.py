from auth import admin_login

if admin_login():
    print("🔓 Access granted to admin panel.")
else:
    print("🔐 Access denied.")
