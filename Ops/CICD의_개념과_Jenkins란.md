

## CICD 기본 개념

![image](https://user-images.githubusercontent.com/74139727/149609056-6bf15185-7efb-4023-b7ea-bce5ef2073b1.png)

> 📂 [Image Source-PARASOFT](https://www.parasoft.com/blog/implementing-qa-in-a-ci-cd-pipeline/)

### CI(Continuous Integration): 지속적인 통합
다수의 개발자가 함께 작업하는 프로젝트나 MSA와 같이 지속적으로 기능 추가가 일어나는 작업같은 경우 빌드와 테스트라는 공통적인 작업이 반복적으로 이루어진다. CI의 통합은 여기서 코드 변경사항이 빌드 및 테스트되는 반복작업을 자동화하는 것을 말한다.

### CD(Continuous Delivery or Deployment): 지속적인 제공 또는 배포
CI가 레포지토리 환경에서 통합을 말한다면 CD는 배포과정의 자동화를 말한다. CD는 보통 두가지의 의미를 가지는데 `Continuous Delivery`와 `Continuous Deployment`이다. `Continuous Delivery`와 `Continuous Deployment`는 비슷하게 쓰의지만 마지막 최종 배포단계를 완전 자동화하느냐에 따라 나뉘게 된다. 

- **Continuous Delivery**
코드가 정상적으로 배포가 가능한지 검증하고(Prepare Release) 검증이 완료되면 수동으로 배포
- **Continuous Deployment**
Prepare release 후 자동으로 배포

</br>

![](https://images.velog.io/images/anjaekk/post/6616b31e-42b0-4e4c-bc01-6af08f8786c9/image.png)

> 📂 [Image Source-hashnode](https://hashnode.com/post/continuous-integration-continuous-delivery-and-continuous-deployment-cicd-an-overview-ckappmie103n34us15emhinhg)

프로젝트의 CICD를 구축해 놓으면 테스트 자동화로 인한 소스의 버그 및 충돌을 방지할 수 있고 배포과정의 단순화로 프로젝트의 데브옵스 의존도가 낮아져 더 신속한 배포가 가능하게 된다.
CICD툴의 종류는 대표적으로 Jenkins, Circleci, Git actions, AWS Codepipeline등 많은 툴이 있지만 그 중 Jenkins에 대해서 알아보도록 하겠다.

</br>

![](https://images.velog.io/images/anjaekk/post/d40557a7-1b70-4250-b2ec-144291508ddf/image.png)

[📂 Jenkins Documentation](https://www.jenkins.io/doc/)

## Jenkins 
Java 기반 무료 Open source로 잘 갖춰진 에코시스템, 커뮤니티 그리고 다양한 플러그인이 있어 CI/CD 툴로 많이 사용한다. Jenkins는 CI 서비스를 제공하는 툴로써 아래와 같은 일을 할 수 있다.

1. 프로젝트 환경 세팅 자동화
2. 프로젝트별 구분된 파이프라인 구성
3. 자동화된 정적 테스트를 통한 소스코드 품질 향상

Jenkins의 동작방식은 개발자가 `Pipeline`에 빌드 및 배포방식을 지정하고  Git main branch에 commit을 하게되면 `Pipeline`은 `Webhooks`를 감시하여 이벤트를 실행하게 된다. (간단한 작업이라면 꼭 Pipeline을 이용하지 않더라도 Jenkins Job을 설정할 수도 있다.) Jenkins를 처음 사용한다면 생소할 수 있는 `Pipeline`과 `Webhooks`에 대해 아래서 알아보자.


### Jenkins Pipeline
Jenkins에서 Pipeline은 CICD를 구현하기 위한 플러그인 모음으로 빌드 및 배포에 대한 설정을 관리한다. Jenkins Pipeline을 이용하면 Jenkins의 Job들을 순차적, 병렬적으로 실행시킬 수 있게된다.  


Jenkins Pipeline에서는 마치 Dockerfile과 같이 Jenkinsfile을 작성하여 복잡한 파이프라인을 모델링할 수 있게 된다.  아래는 Jenkins 공식문서에 있는 python docker container를 가져오는 Jenkinsfile의 예이다. 
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

위와 같이 Jenkinsfile은 Groovy 언어로 된 코드블럭 형태이다. 
> **여기서 Groovy란**   
> _위에서 Jenkins는 Java기반의 툴이라고 했었다. 그루비는 자바 플랫폼(JVM)에서 동작하는 agile 동적언어로 Java에 Python, Ruby 등 다양한 객체지향 프로그래밍 언어의 특징을 더했다._

### Webhook
webhook은 이벤트 핸들러(Event Handler)로 webhook을 제공하는 특정 엔드포인트에서 웹훅 Trigger시 이를 특정 로직에 따라 처리하게 된다. 보통 Jenkins에서는 Github에 Commit생성시 Github webhook이 Trigger되고 Http request의 POST방식을 이용해 Jenkins에게 해당 데이터를 보내게 된다. 이를 확인한 Jenkins는 Pipeline에 지정한 로직을 수행한다. 



</br>


> 참조   
> 🔗 [Jenkins | Creating your first Pipeline](https://www.jenkins.io/doc/pipeline/tour/hello-world/)   
> 🔗 [EJ_Biin | Jenkins의 개념과 역할](https://jbhs7014.tistory.com/156)    
> 🔗 [Suyeon's Blog | Jenkins 설치 및 Static web page, Docker 배포 (AWS S3, ECR, ECS)](https://suyeon96.tistory.com/36)    
> 🔗 [Wonit | [Webhook을 이용하여 CI CD 구성하기] - pipeline으로 배포하기](https://wonit.tistory.com/587)    
