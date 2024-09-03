FROM python:3.12

WORKDIR /app

RUN pip install aiogram

RUN pip install SQLAlchemy

RUN pip install requests

RUN pip install pytz

COPY . .

COPY ./db_plast.db /app/db_plast.db

CMD ["python", "main.py"]