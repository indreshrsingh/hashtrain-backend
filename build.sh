 echo "BUILD START"
pip install -r requirements.txt
mkdir -p /training_website/static
python manage.py collectstatic
python manage.py runserver --workers 2
python manage.py migrate
 echo "BUILD END"
