FROM python

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x entry_point.sh
ENTRYPOINT ["./entry_point.sh"]

CMD ["python", "./run_app.py"]