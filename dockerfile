#imagen de python oficial
FROM python:3.14.3-slim-bookworm

#directorio de trabajo dentro del contenedor
WORKDIR /pycloud

#copiar archivos
COPY . .

#instalar dependencias
RUN pip install -r requirements.txt

#puerto a exponer
EXPOSE 8000

#comando para lanzar la aplicacion
ENTRYPOINT ["gunicorn","PyCloud.wsgi:application"."--bind","0.0.0.0:8000"]