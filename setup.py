#!/usr/bin/env python
"""
Script to set up the Alawna website Django project
"""

import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Alawna Website Django Project")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alawna_website.settings')
    
    try:
        django.setup()
    except Exception as e:
        print(f"❌ Django setup error: {e}")
        sys.exit(1)
    
    # Step 1: Make migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        sys.exit(1)
    
    # Step 2: Apply migrations
    if not run_command("python manage.py migrate", "Applying migrations"):
        sys.exit(1)
    
    # Step 3: Create superuser (interactive)
    print("\n🔄 Creating superuser...")
    print("You'll need to provide username, email, and password for the admin user")
    try:
        execute_from_command_line(['manage.py', 'createsuperuser'])
        print("✅ Superuser created successfully")
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
    
    # Step 4: Setup initial data
    if not run_command("python manage.py setup_initial_data", "Setting up initial data"):
        print("⚠️  Warning: Could not set up initial data, but you can do it manually later")
    
    # Step 5: Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("⚠️  Warning: Could not collect static files")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000")
    print("3. Admin panel: http://127.0.0.1:8000/admin/")
    print("4. Login with the superuser credentials you just created")
    print("\n📚 For more information, see SETUP.md")

if __name__ == '__main__':
    main()
