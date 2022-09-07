FROM python:3.7

LABEL maintainer="mhlee, minhyeok.lee95@gmail.com"
ENV LANG C.UTF-8
ENV env dev
WORKDIR /app


# system dependencies
RUN apt-get update -y
RUN apt-get install -y build-essential
RUN apt-get install -y pandoc

# Install MeCab requirements
RUN curl -o /tmp/mecab.sh -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh && \
    bash /tmp/mecab.sh

# python dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt


# clean up
RUN rm -rf /tmp
