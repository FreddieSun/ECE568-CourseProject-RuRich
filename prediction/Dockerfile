FROM python:3

WORKDIR /usr/src/app
EXPOSE 5001

RUN pip install --no-cache-dir tensorflow scipy numpy sklearn

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x entry_point.sh
ENTRYPOINT ["./entry_point.sh"]

CMD ["python", "./run_app.py"]
#CMD ["gunicorn", "-w", "4", "-k", "gevent", "-b", "0.0.0.0:5001", "run_app:app"]