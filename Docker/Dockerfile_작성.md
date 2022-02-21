# Dockerfile
도커 이미지를 제작할 때 원하는 설계 방향이나 설정된 내용으로 도커 이미지를 제작하기 위해서는 Dockerfile을 이용할 수 있습니다.   
즉 Dockerfile은 도커 이미지를 생성하기 위한 스크립트로서 스크립트 안에 나열된 명령문을 차례대로 수행하며 이미지를 자동화 빌드합니다.   
Dockerfile을 이용하여 이미지 빌드한 후 수정하여 재 빌드하면 변경된 레이어만 다시 빌드 됩니다.(이를 통해 가볍고 빠르게 Docker 이미지 빌드를 할 수 있습니다.)

<br>

## Dockerfile 명령문
#### FROM : 베이스(상위) 이미지
- Dockerfile은 FROM 명령으로 시작되어야 합니다.
- 어느 이미지에서 시작하는지 지정한다고 생각하시면 됩니다.

Python 3.8 (alpine 리눅스 기반)을 base 이미지로 사용
```
FROM python:3.8-alpine
```
- buster, bullseye = 데비안 릴리스의 코드명(bullseye는 개발중으로 아직 안정적이지 않은 버전)
- slim = 최소한의 패키지만 설치(alpine 은 slime보다 더 최소화)
  

#### WORKDIR : 컨테이너 상에서 작업 디렉토리로 전환
- shell에서 cd명령문 같은 역할입니다.
- WORKDIR 명령문 뒤에 나오는 RUN, CMD, ENTRYPOINT, COPY, ADD 명령문은 해당 디렉토리를 기준으로 실행 됩니다.

/usr/app으로 작업 디렉터리 전환
```
WORKDIR /usr/app
```


#### RUN : 새로운 레이어에서 명령어 실행
- RUN 명령을 실행할 때 마다 레이어가 생성되고 캐시됩니다.
- 보통 특정 소프트웨어를 설치하기 위해 많이 사용됩니다.
- 여러줄로 작성시 이미지 레이어가 여러개 생성될 수 있기 때문에 RUN 명령은 되도록 한줄로 작성하는 것이 좋습니다.

RUN, CMD, ENTRYPOINT 명령문은 exec와 shell 형식으로 사용가능 합니다.(exec 형식은 shell을 통해 실행되지 않습니다.)
- exec
```
RUN ["/bin/bash", "-c", "yum -y install nginx"]
```
- shell
```
RUN yum -y install nginx
```

#### VOLUME : 호스트와 공유할 컨테이너 내부 디렉토리 설정
- 컨테이너 안에 있는 데이터는 컨터이너 삭제시 모든 데이터가 같이 삭제되므로 데이터 보존을 위해 volume을 사용합니다.
-VOLUME 사용 예
   - 도커 컨테이너의 /var/log/ 디렉토리와 /data/ 디렉토리 볼륨 마운트
  ```
  FROM ubuntu
  volume ["/var/log/", "/data/"]
  ```
  - 생성한 볼륨은 호스트의 /var/lib/docker/volumes에 생성됩니다.

#### CMD, ENTRYPOINT : 컨테이너가 수행하게 될 실행명령 정의
- 이미지를 바탕으로 생성된 컨테이너에서 사용합니다.
- CMD : RUN 명령문을 사용하여 새로운 명령 지정시 실행 되지 않습니다.(우선순위 RUN>CMD)
- CMD 명령의 사용(3가지 방법)
   - CMD [“executable”,”param1”,”param2”]
   - CMD [“param1”,”param2”]
   - CMD command param1 param2
- CMD 사용 예
   - "Hamster" 출력
   ```
   FROM ubuntu
   CMD echo "Hamster"
   ```
   - Docker RUN 실행시 추가명령이 없을 경우
   ```
   docker run --name <container-name> <image-name>
   >> Hamster
   ```
   - 추가명령이 있을 경우
   ```
   docker run --name <container-name> <image-name> echo "Dog"
   >> Dog
   ```
   
- ENTRYPOINT : RUN 명령문 사용하여 새로운 명령 지정하더라도 해당 컨테이너 수행시 ENTRYPOINT에서 지정한 명령 수행합니다.
- ENTRYPOINT 명령의 사용(2가지 방법)
   - ENTRYPOINT [“executable”, “param1”, “param2”]
   - ENTRYPOINT command param1 param2
- ENTRYPOINT 사용 예
   - CMD와 ENTRYPOINT 같이 사용
   ```
   FROM ubuntu
   ENTRYPOINT ["/bin/echo", "Happy"]
   CMD ["Hamster"]
   ```
   - Docker RUN 실행시 추가명령 여부에 따라 달라지는 결과 값 확인
   ```
   docker run --name <container-name> <image-name>
   >> Happy Hamster
   docker run --name <container-name> <image-name> Dog
   >> Happy Dog
   ```

#### COPY, ADD : 이미지 생성시 파일 복사
- COPY : 호스트에 있는 디렉토리나 파일을 도커 이미지의 파일시스템으로 복사하기 위해 사용합니다.
- ADD : 일반 파일 뿐만 아니라 압축파일이나 네트워크 상의 파일도 사용 가능합니다.
- 호스트에서 컨테이너로 단순한 복사만 처리시 COPY를 사용합니다.
- 절대경로 및 상대경로 둘다 사용 가능합니다.

호스트 디렉토리의 모든 파일을 컨테이너의 app/ 디렉토리로 복사
```
WORKDIR app/
COPY . .
```

#### ENV : 환경변수 지정
- ENV : Dockerfile 및 컨테이너 안에서의 환경변수를 지정할 때 사용합니다.

```
ENV PYTHONUNBUFFERED=1
```
> 🔗 [파이썬 바이트코드 관련 블로그 글 링크](https://python-docs.readthedocs.io/en/latest/writing/gotchas.html)

#### ARG : 이미지 build시 사용될 변수 값 지정
- Dockerfile에서만 사용되는 환경변수(build시에만 사용)


#### LABEL : 이미지에 메타데이터 추가
- key-value 형태

<br>

## .dockerignore
도커 이미지를 빌드할 때 제외 시키고 싶은 파일은 .dockerignore에 추가하여 빌드하면 됩니다.

- git과 마크다운 파일 제외
```
#.dockerignore
.git
*.md
```
