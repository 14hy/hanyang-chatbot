# Hanyang-chatbot Builder - Server

## Requirements

1. miniconda 또는 anaconda 설치하기

## 폴더 구조

```markdown
📦server
 ┣ 📂api
 ┃ ┣ 📂services
 ┃ ┃ ┣ 📜shuttle.py  # 셔틀콕 시간표 제공을 위한 API
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📜main.py  # 챗봇 기본 대화를 위한 API
 ┃ ┣ 📜rive_dummy.py  # 더미 데이터를 위한 API
 ┃ ┗ 📜__init__.py
 ┣ 📂db
 ┃ ┣ 📜connect.py  # FireStore 연결 파일
 ┃ ┣ 📜rive_log.py # 및 기타 데이터베이스 클래스 스키마
 ┃ ┣ 📜rive_presets.py
 ┃ ┣ 📜rive_qa.py
 ┃ ┗ 📜__init__.py
 ┣ 📂engine
 ┃ ┣ 📂preprocessor  # 텍스트 전처리 함수
 ┃ ┣ 📂services  # 각종 서비스 함수
 ┣ 📂rs
 ┃ ┣ 📂examples
 ┃ ┃ ┗ 📜test.rive
 ┃ ┣ 📜get_dummy.py  # 더미데이터를 얻을 수 있는 함수
 ┃ ┣ 📜test_rive.py  # examples 안의 rive 파일들을 테스트 할 수 있는 파일
 ┃ ┗ 📜__init__.py
 ┣ 📜.gcloudignore
 ┣ 📜.gitignore
 ┣ 📜app.yaml  # App Engine을 위한 설정 파일
 ┣ 📜config.py  # 서버 전반적인 설정을 할 수 있는 파일
 ┣ 📜cool-benefit-185923.json  # SLACK에서 다운 받아 넣기
 ┣ 📜main.py  # 서버 시작
 ┣ 📜README.md
 ┣ 📜requirements.txt  # 의존성
 ┗ 📜utils.py  # 유틸리티 함수들
```

## 개발하기

### Configuration

```
cool-benefit-185923.json 파일을 slack 에서 다운 받아 server 폴더 안에 넣습니다.
(데이터베이스 key 파일)
```

### Windows

```bash
cd server
conda create -n hanyang-chatbot python=3.7
conda activate hanyang-chatbot
pip install -r requirements.txt
pip install -t lib/ flask-restplus
python main.py
```

### Mac/Linux

```
pip install gunicorn
gunicorn -b :$PORT main:app
```

## 배포하기

### 배포

[gcloud SDK](https://cloud.google.com/sdk/docs/#install_the_latest_cloud_tools_version_cloudsdk_current_version)를 설치 합니다.

```bash
gcloud init # 안내에 따라, 구글 계정, 프로젝트 등을 설정
gcloud components install app-engine-python
pip install -t lib/ flask-restplus # 개발에서 했다면 건너뛰기 가능
gcloud app deploy
```

### 로그 확인

```
gcloud app logs tail -s hanyang-chatbot
```