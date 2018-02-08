# assume in python virtual environment
pip install -r dev_reqs.txt

python mocacares_backend/manage.py makemigrations
python mocacares_backend/manage.py migrate
sudo env/bin/python mocacares_backend/manage.py collectstatic --noinput

sudo service memcached restart
sudo service redis-server restart
sudo service apache2 restart

pm2 stop all
pm2 delete all
pm2 start socket/socket.js -i max

# add all pre-defined event types.
python prepare_data.py


