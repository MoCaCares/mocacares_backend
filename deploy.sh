# assume in python virtual environment

python variora/manage.py makemigrations
python variora/manage.py migrate
sudo env/bin/python variora/manage.py collectstatic --noinput

sudo service memcached restart
sudo service redis-server restart
sudo service apache2 restart
