# assume in python virtual environment

python mocacares_backend/manage.py makemigrations
python mocacares_backend/manage.py migrate
sudo env/bin/python mocacares_backend/manage.py collectstatic --noinput

sudo service memcached restart
sudo service redis-server restart
sudo service apache2 restart
