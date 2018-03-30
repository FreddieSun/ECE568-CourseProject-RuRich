FROM python:3

WORKDIR /usr/src/app
EXPOSE 5001

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# RUN chmod -x

CMD ["python", "./run_app.py"]
