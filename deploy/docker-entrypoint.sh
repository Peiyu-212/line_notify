#!/usr/bin/env bash

if [ "$1" == "/usr/local/bin/uwsgi" -a "$2" == "--ini" -a "$3" == "/etc/uwsgi/uwsgi.ini" ]; then
    ### 1. Collect django static files
    echo `ls /opt`
    #echo `ls /${PROJECT_NAME}_dev/${PROJECT_NAME}_web`
    python /map_world/manage.py collectstatic --noinput
    ### 2. Copy staticfiles to the shared volume directory
    cp -r /map_world/staticfiles /shared
    ### 3. Change log file permission which belong to uwsgi application
    chown -R www-data:www-data /log
    #chown -R www-data:www-data /var/tmp/django_cache/
    ### 4. execute uwsgi
    exec "$@"
fi

exec "$@"