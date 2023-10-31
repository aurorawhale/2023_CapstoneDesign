FROM continuumio/miniconda3

ARG DEBIAN_FRONTEND=noninteractive

# 환경 변수 설정
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Miniconda 다운로드 및 설치를 위한 환경 변수 설정
ENV PATH /opt/conda/bin:$PATH

# 파이썬 3.11 설치
RUN conda install -y python=3.11

# 작업 디렉토리 생성 및 설정
WORKDIR /FMB

# 필요한 Python 패키지를 설치합니다.
COPY requirements.txt /FMB/
RUN pip install -r /FMB/requirements.txt

# 컨테이너 실행 시 로컬 개발 폴더와 컨테이너 내부 /app 폴더를 공유
VOLUME [".:/FMB"]

CMD ["/bin/bash"]

# 컨테이너 내에서 실행할 명령을 지정합니다.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
