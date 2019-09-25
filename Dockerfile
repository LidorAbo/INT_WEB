FROM python:latest
ARG app_folder=/usr/src/app
ARG regular_user=1000
EXPOSE 5000/tcp
WORKDIR ${app_folder}
USER root
RUN chown -R ${regular_user}:${regular_user} ${app_folder}
COPY ./sources ./
RUN pip install pymongo && pip install flask
USER ${regular_user}
WORKDIR ./Flask
CMD ["python3", "app.py"]
