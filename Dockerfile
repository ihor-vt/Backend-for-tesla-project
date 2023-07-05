FROM python:3.9

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME/
RUN pip install --no-cache-dir -r requirements.txt

COPY . $APP_HOME/

EXPOSE 8000

CMD ["python", "tesla_project/manage.py", "runserver", "0.0.0.0:8000"]
