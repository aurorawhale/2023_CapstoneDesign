# 세팅방법

## 1. 파이썬 가상환경 설정
django 서버를 기동하기 위해선 파이썬 가상환경을 켜야함.(anaconda 추천) <br>
### pip install -r requirement.txt
로 세팅

## 2. 오라클 서버 기동
db용 오라클 서버를 기동

## 3. Docker 실행
window or mac 기반일 경우 docker 프로그램 설치 후 실행 바람<br>
### docker-compose up
을 실행

## 4. db를 django에 적용
shell 위치를 manage.py가 있는 /FMB로 이동 후<br>
python manage.py makemigrations<br>
python manage.py migrate
실행