# blaster_impresiones

## Configuracion del entorno local:
- Para este proyecto es necesario tener instalado docker y docker compose
- crear un entorno virtual de python
- activar el entorno virtual
- crear un archivo ```.env``` en el raiz del proyecto con el siguiente codigo:
```
SECRET_KEY='secret'
DB_NAME='blaster_impresiones'
DB_USER='postgres'
DB_PASSWORD='postgres'
DB_HOST='localhost'
DB_PORT='5432'
DJANGO_SETTINGS_MODULE='config.settings.production'
```
- crear un archivo ```app_init.sh`` en el raiz del proyecto con el siguiente codigo:
```
#!/bin/sh

echo "Collecting static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py wait_for_database
python manage.py migrate

echo "Starting server"
gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.development config.wsgi:application --bind 0.0.0.0:8000
```
- ejecutar este comando de docker
```
docker compose build
```
- Levantar el contenedor de docker
```
docker compose up
```

## Detener los contenedores
```
docker compose stop
```

## Proceso de desarrollo

- Se debe ubicar primeramente en la rama develop
```
git checkout develop
```
- Actualizar la rama local con los ultimos cambios
```
git pull
```
- Luego se debe crear una nueva rama con el numero del issue, por ejemplo ```issue_XXXX```, se debe reemplazar XXXX por el numero del issue
```
git checkout -b issue_XXXX
```
- De aqui en adelante se debe realizar el requerimiento del issue
- Una vez terminado, se debe subir la rama del issue colocandose en la misma
```
git checkout issue_XXXX
```
```
git push --set-upstream origin issue_XXXX
```

## Actualizar la rama del issue
- Para actualizar la rama respecto a los cambios que se podrian haber hecho en develop
```
git checkout develop
```
```
git pull
```
```
git checkout issue_XXXX
```
```
git merge develop
```
```
git push
```
