FROM ubuntu:18.04

MAINTAINER "WILLSON, <inh0211@hanyang.ac.kr>"

# Package install
RUN apt-get update -y
RUN apt-get install -y build-essential python python3 python3-dev python3-pip
RUN apt-get -y install wget swig vim
RUN pip3 install --upgrade pip

# 환경설정
ENV LANG C.UTF-8

# Khaiii 설치
RUN pip3 install cmake
RUN apt-get -y install git
RUN git clone https://github.com/kakao/khaiii
WORKDIR /khaiii
RUN mkdir build
WORKDIR /khaiii/build
RUN cmake .. && make all && make resource && make install && make package_python
WORKDIR package_python
RUN pip3 install .

# Mecab-ko, mecab-ko-dic 설치
WORKDIR /
RUN wget https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz
RUN wget https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz
RUN tar zxfv mecab-0.996-ko-0.9.2.tar.gz
RUN tar zxfv mecab-ko-dic-2.1.1-20180720.tar.gz
WORKDIR /mecab-0.996-ko-0.9.2
RUN ./configure && make && make check && make install
WORKDIR /mecab-ko-dic-2.1.1-20180720
RUN ldconfig && ./configure && make && make check && make install

# MeCab python binding
WORKDIR /
RUN git clone https://github.com/jonghwanhyeon/python-mecab-ko
WORKDIR /python-mecab-ko
RUN pip3 install -r requirements.txt && python3 setup.py build && python3 setup.py install

# Python package 설치
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

#ENTRYPOINT ["python3", "app.py"]