FROM tiangolo/uwsgi-nginx-flask:latest

RUN mkdir /home/bins
COPY . /app
COPY nginx.conf /etc/nginx

RUN pip3 install -r /app/requirements.txt
RUN service nginx start

EXPOSE 5000
CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--protocol=http", "/app/uwsgi.ini"]