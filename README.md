# blaster_impresiones

## Configuracion del entorno local:
- Dentro de la carpeta del repositorio de debe crear un entorno local
- Para ello se debe ejecutar el siguiente comando asegurandose que la version de python sea la del proyecto en ```runtime.txt```
```
python -m venv venv
```
- Configurar las variables de entorno: Para ello depende del sistema operativo donde se encuentre:
### windows
1) Crear un archivo con el nombre ```export_env_vars.bat```, luego copiar el siguiente codigo y pegarlo en ese archivo

```
@echo off
set DEBUG=True
set ENVIRONMENT=local
set DJANGO_SETTINGS_MODULE=config.settings
...

2) Abrir el cmd y luego hacerle doble click al archivo generado. Este archivo sera permanente para cada vez que se quiera correr el proyecto
3) Activar el entorno virtual
```
cd venv
cd Scripts
activate
cd ..
cd ..
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
- Luego se debe crear una nueva rama con el numero del issue, por ejemplo ```issue_1```
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
