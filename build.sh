 echo "BUILD START"
pip install -r requirements.txt
python3.11 manage.py migrate
python3.11 manage.py collectstatic --noinput
 echo "BUILD END"
