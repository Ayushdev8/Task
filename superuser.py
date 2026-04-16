import os
import django
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskmanage.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "ayush"
email = "ayushjha@gmail.com"
password = "8851"
first_name = "ayush"
last_name = "jha"



if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        # add extra fields if needed
    )
    print("Superuser created successfully")
else:
    print("Superuser already exists ")