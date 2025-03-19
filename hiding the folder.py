import os

secure_folder = r"C:\Users\derpt\OneDrive\SecureFolder"

# Completely remove access for all users
os.system(f'icacls "{secure_folder}" /deny Everyone:(OI)(CI)F')

print("🔒 SecureFolder is now fully locked. Manual access is blocked.")
