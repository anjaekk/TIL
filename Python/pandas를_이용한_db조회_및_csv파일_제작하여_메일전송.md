pandas를 이용하여 postgresql을 조회하고 csv제작 및 메일 전송을 하고자 한다. 해당 내용은 jupyterlab에서 진행했다.
## 1. DB 조회
```
import psycopg2 as pg
import pandas as pdv
import pandas.io.sql as psql
import base64, hashlib, smtplib, zipfile, os
from Cryptodome import Random
from Cryptodome.Cipher import AES
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

with pg.connect(
            host = '127.0.0.1',
            port = 8000,
            database = 'panda_db',
            user = 'root',
            password = 'password') as conn:
    sql = "SELECT * FROM company"
    
    df = psql.read_sql(sql,conn)
```
sql raw query를 통해서 원하는 데이터 추출 후 사용할 수 있다. 


## 2. 데이터 컬럼 정제
```   
    def decrypt(enc):
        if enc is not None and len(enc) > 0:
        	enc *= 0.1
        else: enc='null'
        return enc
    
    df['payment'] = df['payment'].apply(decrypt)
    df['employee'] = df['name'] + "-" + df['position']
    df = df[df.columns.difference(['name', 'position'])]
    print(df)
```
1. payment라는 컬럼 값들에게 10% 곱하는 함수를 적용하고
2. 직원의 이름과 직급을 합쳐서 employee라는 컬럼을 새로 만드려고 한다.(기존의 name과 position 컬럼은 삭제)

사실 곱하기 0.1정도는 lambda를 이용하여 사용하는게 효율면에서나 가독성이 좋을 수 있지만 복잡한 함수를 적용해야할 때는 위와 같이 할 수 있다.(예를 들어 db데이터의 암,복호화) 

## 3. csv파일 저장 후 파일 압축
```
    df.to_csv('csv 파일 경로', header=True, index=False)

list_zip = zipfile.ZipFile('만들 zip파일 경로', 'w')
list_zip.write('csv파일 이름', compress_type=zipfile.ZIP_DEFLATED)

list_zip.close()

```
csv파일이 너무 큰 경우 압축을 진행한다. 


## 4. 메일전송 후 만든 zip, csv파일 삭제
```
from_addr = '발송인 메일'
app_password = '앱 비밀번호'
to_addr = '수신인 메일'

try:    
    sess = smtplib.SMTP('smtp.gmail.com', 587)
    sess.starttls()
    sess.login(from_addr, app_password)
    
    msg = MIMEMultipart()
    msg['Subject'] = '메일 제목'
    msg.attach(MIMEText('메일 내용','plain', 'utf-8'))
    
    attach = open('전송할 파일이름', 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attach).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + '전송할 파일 이름')
    msg.attach(part)
    
    sess.sendmail(from_addr, to_addr, msg.as_string())
    sess.quit()
    print('Successfully sent the message')
except Exception as e:
    print(e)
    
os.remove('zip파일 경로')
os.remove('csv파일 경로')

```
메일을 전송할 때는 googlemaildp 접속하여 IMAP설정과 2중 보안사용을 설정하여 발급받은 앱 비밀번호를 이용해야 한다. python의 SMTP서버를 이용해 간단하게 메일을 전송할 수 있다.
