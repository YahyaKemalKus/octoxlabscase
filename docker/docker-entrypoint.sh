#!/bin/bash

# wait for Postgres to start
until python << END
import sys
import psycopg2
import environ
env = environ.Env()
env.read_env()
db_credentials = env.db()
try:
    conn = psycopg2.connect(
      dbname=db_credentials["NAME"],
      user=db_credentials["USER"],
      password=db_credentials["PASSWORD"],
      host=db_credentials["HOST"],
      port=db_credentials["PORT"]
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Start app
>&2 echo "Postgres is up - executing command"

python /app/docker/seedelastic.py
python manage.py collectstatic --noinput
python manage.py migrate hosts
python manage.py migrate users
python manage.py createoctoxadmin -u ${OCTOXLABS_SUPERUSER_NAME} -p ${OCTOXLABS_SUPERUSER_PASSWORD} -e ${OCTOXLABS_SUPERUSER_EMAIL}
python manage.py createoctoxuser -u ${OCTOXLABS_USER_NAME} -p ${OCTOXLABS_USER_PASSWORD} -e ${OCTOXLABS_USER_EMAIL}
python manage.py runserver 0.0.0.0:8001
