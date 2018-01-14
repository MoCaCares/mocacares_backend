# modify database scheme acording to the change of models.py
python mocacares_backend/manage.py makemigrations

#  apply database scheme change to database
python mocacares_backend/manage.py migrate

if [ $# -ge 1 ]; then
    python mocacares_backend/manage.py runserver 0.0.0.0:$1  # run Django development server on specify port
else
    python mocacares_backend/manage.py runserver 0.0.0.0:8000  # run Django development server on default port 8080
fi
