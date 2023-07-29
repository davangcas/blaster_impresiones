# blaster_impresiones

## Configuracion del entorno local:

Para configurar el entorno local se puede hacer de dos formas:
- Una realizandolo mediante docker
- Otra de manera tradicional con un entorno virtual en la computadora

### Metodo docker
- Para este proyecto es necesario tener instalado docker y docker compose
- crear un entorno virtual de python con la version del ```runtime.txt```
- activar el entorno virtual
- crear un archivo ```.env``` en el raiz del proyecto con el siguiente codigo:
```
SECRET_KEY='secret'
DB_NAME='blaster_impresiones'
DB_USER='postgres'
DB_PASSWORD='postgres'
DB_HOST='postgres'
DB_PORT='5432'
DEBUG="True"
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
gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.production config.wsgi:application --bind 0.0.0.0:8000

```

- ejecutar el siguiente comando para compilar la imagen de docker
```
docker compose build
```
- Levantar el contenedor de docker
```
docker compose up
```

-- Detener los contenedores
```
docker compose down --volumes
```

### Metodo tradicional
- crear un entorno virtual de python con la version del ```runtime.txt```
- Crear un archivo llamado ```export_env_vars.sh``` con el siguiente contenido:
```
#!/bin/sh

source venv/bin/activate
export DEBUG="True"
export DJANGO_SETTINGS_MODULE=config.settings.development
```
- activar el entorno virtual, puede hacerse de dos maneras dependiendo del sistema operativo
- - windows: (activar el entorno virtual manualmente) y luego en la consola escribir
    ```
    setx DEBUG "True"
    setx DJANGO_SETTINGS_MODULE "config.settings.development"
    ```
- - ubuntu:
    ```
    . export_env_vars.sh
    ```
- instalar dependencias del proyecto con
```
pip install -r requirements.txt
```
- crear una base de datos postgres con el nombre de ```blaster_impresiones```
(en caso de usar ubuntu ejecutar este comando)
```
createdb blaster_impresiones
```
- Hacer el migrate del proyecto en la base de datos con el siguiente comando
```
python manage.py migrate
```

## Correr el proyecto
- Docker:
```
docker compose up --build
```
- Metodo normal:
```
python manage.py runserver
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
