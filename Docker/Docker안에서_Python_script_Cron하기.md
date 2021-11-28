Docker 컨테이너 안에서 Python script를 Linux Cron을 이용해봤다. 


실행할 파일은 간단하게 현재 시간과 문구를 print하기로 했다.

### /execute.py
```
from datetime import datetime, timedelta

print(datetime.now)
print('cron testtet!!')
```

### /cron
```
TZ=Asia/Seoul
* * * * * /usr/local/bin/python /app/execute.py >> /var/log/cron.log 2>&1
# An empty line is required at the end of this file for a valid cron file.
```

매 분마다 execute.py를 실행하고 해당 로그가 기록되도록 하였다. 표준에러의 로그를 남기고 싶다면 뒤에 2>$1 을 붙이면 된다. 
> **2>&1**
1: stdout
2: stderr
>: redirection
2>&1: stderr를 stdout으로 리디렉션해서 stdout과 동일하게 처리

**주의할 점은 저 뒤에 주석부분을 꼭 넣어줘야한다. 주석으로 넣기싫다면 빈칸으로 넣어놔야 cron이 실행된다.**

crontab(table)을 작성할 때 저 `*`의 의미는 아래 그림과 같다. 
![](https://images.velog.io/images/anjaekk/post/44c22832-e27e-4757-a478-e99ea3e5664f/image.png)
[A Beginners Guide To Cron Jobs](https://ostechnix.com/a-beginners-guide-to-cron-jobs/)


### /Dockerfile
```
FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    cron

# Copy cron file to the cron.d directory on container
COPY cron /etc/cron.d/cron
# Give execution access
RUN chmod 0755 /etc/cron.d/cron
# Run cron job on cron file
RUN crontab /etc/cron.d/cron
# Create the log file
RUN touch /var/log/cron.log

CMD ["cron", "-f"]
```

### 로그 확인하기
1. 컨테이너를 실행하고 해당 컨테이너로 들어간다.(bash)
2. Dockerfile에서 만들어준 log 파일의 경로로 들어간다.
```
cd /var/log
```
3. 로그파일을 읽는다.
```
cat cron.log
```
4. 확인 가능! 굿!


> 참조   
> 🔗 [리눅스 작업 스케줄러 (cron) | 토닥토닥파이썬](https://wikidocs.net/48485)
