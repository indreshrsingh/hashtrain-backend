 echo "BUILD START"
pip install --upgrade pip
pip install -r requirements.txt
python3.9 manage.py migrate
python3.9 manage.py collectstatic --noinput
 echo "BUILD END"
