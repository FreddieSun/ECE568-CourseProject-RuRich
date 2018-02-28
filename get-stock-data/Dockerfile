FROM python

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x entry_point.sh
ENTRYPOINT ["./entry_point.sh"]

CMD ["python", "./run_app.py"]