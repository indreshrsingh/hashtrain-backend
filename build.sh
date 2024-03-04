 echo "BUILD START"
 python3.9 -m pip install -r requirements.txt
 mkdir -p /training_website/static
 python3.9 manage.py collectstatic 
 python manage.py gunicorn --workers 2 myproject.wsgi
 python manage.py makemigrations && migrate
 echo "BUILD END"
