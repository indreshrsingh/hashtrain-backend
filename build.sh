 echo "BUILD START"
 python3.9 -m pip install -r requirements.txt
 python manage.py collectstatic && gunicorn --workers 2 myproject.wsgi
 echo "BUILD END"
