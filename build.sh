 echo "BUILD START"
 python3.9 -m pip install -r requirements.txt
 python manage.py collectstatic && gunicorn --workers 2 myproject.wsgi
 python3.9 -m pip install psycopg2
 python manage.py makemigrations && migrate
 echo "BUILD END"
