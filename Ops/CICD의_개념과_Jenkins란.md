

## CICD ๊ธฐ๋ณธ ๊ฐ๋

![image](https://user-images.githubusercontent.com/74139727/149609056-6bf15185-7efb-4023-b7ea-bce5ef2073b1.png)

> ๐ [Image Source-PARASOFT](https://www.parasoft.com/blog/implementing-qa-in-a-ci-cd-pipeline/)

### CI(Continuous Integration): ์ง์์ ์ธ ํตํฉ
๋ค์์ ๊ฐ๋ฐ์๊ฐ ํจ๊ป ์์ํ๋ ํ๋ก์ ํธ๋ MSA์ ๊ฐ์ด ์ง์์ ์ผ๋ก ๊ธฐ๋ฅ ์ถ๊ฐ๊ฐ ์ผ์ด๋๋ ์์๊ฐ์ ๊ฒฝ์ฐ ๋น๋์ ํ์คํธ๋ผ๋ ๊ณตํต์ ์ธ ์์์ด ๋ฐ๋ณต์ ์ผ๋ก ์ด๋ฃจ์ด์ง๋ค. CI์ ํตํฉ์ ์ฌ๊ธฐ์ ์ฝ๋ ๋ณ๊ฒฝ์ฌํญ์ด ๋น๋ ๋ฐ ํ์คํธ๋๋ ๋ฐ๋ณต์์์ ์๋ํํ๋ ๊ฒ์ ๋งํ๋ค.

### CD(Continuous Delivery or Deployment): ์ง์์ ์ธ ์ ๊ณต ๋๋ ๋ฐฐํฌ
CI๊ฐ ๋ ํฌ์งํ ๋ฆฌ ํ๊ฒฝ์์ ํตํฉ์ ๋งํ๋ค๋ฉด CD๋ ๋ฐฐํฌ๊ณผ์ ์ ์๋ํ๋ฅผ ๋งํ๋ค. CD๋ ๋ณดํต ๋๊ฐ์ง์ ์๋ฏธ๋ฅผ ๊ฐ์ง๋๋ฐ `Continuous Delivery`์ `Continuous Deployment`์ด๋ค. `Continuous Delivery`์ `Continuous Deployment`๋ ๋น์ทํ๊ฒ ์ฐ์์ง๋ง ๋ง์ง๋ง ์ต์ข ๋ฐฐํฌ๋จ๊ณ๋ฅผ ์์  ์๋ํํ๋๋์ ๋ฐ๋ผ ๋๋๊ฒ ๋๋ค. 

- **Continuous Delivery**
์ฝ๋๊ฐ ์ ์์ ์ผ๋ก ๋ฐฐํฌ๊ฐ ๊ฐ๋ฅํ์ง ๊ฒ์ฆํ๊ณ (Prepare Release) ๊ฒ์ฆ์ด ์๋ฃ๋๋ฉด ์๋์ผ๋ก ๋ฐฐํฌ
- **Continuous Deployment**
Prepare release ํ ์๋์ผ๋ก ๋ฐฐํฌ

</br>

![](https://images.velog.io/images/anjaekk/post/6616b31e-42b0-4e4c-bc01-6af08f8786c9/image.png)

> ๐ [Image Source-hashnode](https://hashnode.com/post/continuous-integration-continuous-delivery-and-continuous-deployment-cicd-an-overview-ckappmie103n34us15emhinhg)

ํ๋ก์ ํธ์ CICD๋ฅผ ๊ตฌ์ถํด ๋์ผ๋ฉด ํ์คํธ ์๋ํ๋ก ์ธํ ์์ค์ ๋ฒ๊ทธ ๋ฐ ์ถฉ๋์ ๋ฐฉ์งํ  ์ ์๊ณ  ๋ฐฐํฌ๊ณผ์ ์ ๋จ์ํ๋ก ํ๋ก์ ํธ์ ๋ฐ๋ธ์ต์ค ์์กด๋๊ฐ ๋ฎ์์ ธ ๋ ์ ์ํ ๋ฐฐํฌ๊ฐ ๊ฐ๋ฅํ๊ฒ ๋๋ค.
CICDํด์ ์ข๋ฅ๋ ๋ํ์ ์ผ๋ก Jenkins, Circleci, Git actions, AWS Codepipeline๋ฑ ๋ง์ ํด์ด ์์ง๋ง ๊ทธ ์ค Jenkins์ ๋ํด์ ์์๋ณด๋๋ก ํ๊ฒ ๋ค.

</br>

![](https://images.velog.io/images/anjaekk/post/d40557a7-1b70-4250-b2ec-144291508ddf/image.png)

[๐ Jenkins Documentation](https://www.jenkins.io/doc/)

## Jenkins 
Java ๊ธฐ๋ฐ ๋ฌด๋ฃ Open source๋ก ์ ๊ฐ์ถฐ์ง ์์ฝ์์คํ, ์ปค๋ฎค๋ํฐ ๊ทธ๋ฆฌ๊ณ  ๋ค์ํ ํ๋ฌ๊ทธ์ธ์ด ์์ด CI/CD ํด๋ก ๋ง์ด ์ฌ์ฉํ๋ค. Jenkins๋ CI ์๋น์ค๋ฅผ ์ ๊ณตํ๋ ํด๋ก์จ ์๋์ ๊ฐ์ ์ผ์ ํ  ์ ์๋ค.

1. ํ๋ก์ ํธ ํ๊ฒฝ ์ธํ ์๋ํ
2. ํ๋ก์ ํธ๋ณ ๊ตฌ๋ถ๋ ํ์ดํ๋ผ์ธ ๊ตฌ์ฑ
3. ์๋ํ๋ ์ ์  ํ์คํธ๋ฅผ ํตํ ์์ค์ฝ๋ ํ์ง ํฅ์

Jenkins์ ๋์๋ฐฉ์์ ๊ฐ๋ฐ์๊ฐ `Pipeline`์ ๋น๋ ๋ฐ ๋ฐฐํฌ๋ฐฉ์์ ์ง์ ํ๊ณ   Git main branch์ commit์ ํ๊ฒ๋๋ฉด `Pipeline`์ `Webhooks`๋ฅผ ๊ฐ์ํ์ฌ ์ด๋ฒคํธ๋ฅผ ์คํํ๊ฒ ๋๋ค. (๊ฐ๋จํ ์์์ด๋ผ๋ฉด ๊ผญ Pipeline์ ์ด์ฉํ์ง ์๋๋ผ๋ Jenkins Job์ ์ค์ ํ  ์๋ ์๋ค.) Jenkins๋ฅผ ์ฒ์ ์ฌ์ฉํ๋ค๋ฉด ์์ํ  ์ ์๋ `Pipeline`๊ณผ `Webhooks`์ ๋ํด ์๋์ ์์๋ณด์.


### Jenkins Pipeline
Jenkins์์ Pipeline์ CICD๋ฅผ ๊ตฌํํ๊ธฐ ์ํ ํ๋ฌ๊ทธ์ธ ๋ชจ์์ผ๋ก ๋น๋ ๋ฐ ๋ฐฐํฌ์ ๋ํ ์ค์ ์ ๊ด๋ฆฌํ๋ค. Jenkins Pipeline์ ์ด์ฉํ๋ฉด Jenkins์ Job๋ค์ ์์ฐจ์ , ๋ณ๋ ฌ์ ์ผ๋ก ์คํ์ํฌ ์ ์๊ฒ๋๋ค.  


Jenkins Pipeline์์๋ ๋ง์น Dockerfile๊ณผ ๊ฐ์ด Jenkinsfile์ ์์ฑํ์ฌ ๋ณต์กํ ํ์ดํ๋ผ์ธ์ ๋ชจ๋ธ๋งํ  ์ ์๊ฒ ๋๋ค.  ์๋๋ Jenkins ๊ณต์๋ฌธ์์ ์๋ python docker container๋ฅผ ๊ฐ์ ธ์ค๋ Jenkinsfile์ ์์ด๋ค. 
```
# Jenkinsfile (Declarative Pipeline)
pipeline {
    agent { docker { image 'python:3.10.1-alpine' } }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}
```

์์ ๊ฐ์ด Jenkinsfile์ Groovy ์ธ์ด๋ก ๋ ์ฝ๋๋ธ๋ญ ํํ์ด๋ค. 
> **์ฌ๊ธฐ์ Groovy๋**   
> _์์์ Jenkins๋ Java๊ธฐ๋ฐ์ ํด์ด๋ผ๊ณ  ํ์๋ค. ๊ทธ๋ฃจ๋น๋ ์๋ฐ ํ๋ซํผ(JVM)์์ ๋์ํ๋ agile ๋์ ์ธ์ด๋ก Java์ Python, Ruby ๋ฑ ๋ค์ํ ๊ฐ์ฒด์งํฅ ํ๋ก๊ทธ๋๋ฐ ์ธ์ด์ ํน์ง์ ๋ํ๋ค._

### Webhook
webhook์ ์ด๋ฒคํธ ํธ๋ค๋ฌ(Event Handler)๋ก webhook์ ์ ๊ณตํ๋ ํน์  ์๋ํฌ์ธํธ์์ ์นํ Trigger์ ์ด๋ฅผ ํน์  ๋ก์ง์ ๋ฐ๋ผ ์ฒ๋ฆฌํ๊ฒ ๋๋ค. ๋ณดํต Jenkins์์๋ Github์ Commit์์ฑ์ Github webhook์ด Trigger๋๊ณ  Http request์ POST๋ฐฉ์์ ์ด์ฉํด Jenkins์๊ฒ ํด๋น ๋ฐ์ดํฐ๋ฅผ ๋ณด๋ด๊ฒ ๋๋ค. ์ด๋ฅผ ํ์ธํ Jenkins๋ Pipeline์ ์ง์ ํ ๋ก์ง์ ์ํํ๋ค. 



</br>


> ์ฐธ์กฐ   
> ๐ [Jenkins | Creating your first Pipeline](https://www.jenkins.io/doc/pipeline/tour/hello-world/)   
> ๐ [EJ_Biin | Jenkins์ ๊ฐ๋๊ณผ ์ญํ ](https://jbhs7014.tistory.com/156)    
> ๐ [Suyeon's Blog | Jenkins ์ค์น ๋ฐ Static web page, Docker ๋ฐฐํฌ (AWS S3, ECR, ECS)](https://suyeon96.tistory.com/36)    
> ๐ [Wonit | [Webhook์ ์ด์ฉํ์ฌ CI CD ๊ตฌ์ฑํ๊ธฐ] - pipeline์ผ๋ก ๋ฐฐํฌํ๊ธฐ](https://wonit.tistory.com/587)    
