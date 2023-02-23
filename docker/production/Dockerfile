FROM python:3.9
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

WORKDIR /root/
COPY ./ /root/
RUN pip install -r requirements.txt

EXPOSE 8080
WORKDIR /root/opt/server
CMD ["uvicorn", "run:app", "--reload","--host", "0.0.0.0", "--port", "8080"]