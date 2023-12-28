FROM python:3.8
COPY ./requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
WORKDIR /app
ENTRYPOINT ["python", "app.py"]