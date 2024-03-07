FROM selenium/standalone-chrome

USER root
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install selenium
RUN python3 -m pip install Flask

COPY ./app.py .
COPY ./Scrape.py .

EXPOSE 3000

CMD ["python3", "app.py"]
