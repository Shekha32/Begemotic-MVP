FROM python:3.10.6
RUN mkdir /app
WORKDIR /app
RUN cd /app
COPY fastapi/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
RUN rm -rf /app
CMD [ "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]
