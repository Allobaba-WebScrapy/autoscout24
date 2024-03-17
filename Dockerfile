FROM selenium/standalone-chrome

USER root
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install selenium
RUN python3 -m pip install Flask
RUN python3 -m pip install flask-cors

COPY ./app.py .
COPY ./AutoScout24.py .

EXPOSE 3000

CMD ["python3", "app.py"]
