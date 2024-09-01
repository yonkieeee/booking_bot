FROM python:3.12

WORKDIR /app

RUN pip install aiogram

RUN pip install SQLAlchemy

RUN pip install requests

RUN pip install pytz

COPY . .

CMD ["python", "main.py"]