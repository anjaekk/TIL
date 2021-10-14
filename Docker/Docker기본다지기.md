# 🐳 Docker

## Docker Overview
- Docker는 애플리케이션을 신속하게 구축, 테스트 및 배포할 수 있는 **컨테이너 기반의 오픈소스 가상화 플랫폼**입니다. 
- Docker 컨테이너에는 라이브러리, 시스템 도구, 코드, 런타임 등 소프트웨어를 실행하는 데 필요한 모든 것이 포함되어 있습니다. 
- Docker는 각 서버에 설치되며 컨테이너를 구축, 시작 또는 중단하는 데 사용할 수 있는 간단한 명령을 제공합니다.

<br>

## Docker 사용의 장점
- 애플리케이션 운영을 표준화합니다.
- 코드 이동이 원활하여 비용을 절감할 수 있습니다.
- 어디서나 안정적으로 실행할 수 있는 단일 객체를 확보하게 됩니다. 
즉, 격리되어서 실행가능하지만 성능 손실이 거의 없기 때문에 도커만 설치되어 있다면 현재 주어진 컴퓨팅 자원 위에서 깔끔하고, 효율적인 운영이 가능해집니다. 

<br>

## Docker Architecture
도커는 Client-Server 아키텍처를 사용합니다. 도커 Client와 Daemon은 UNIX소켓 또는 네트워크 인터페이스를 통해 REST API를 사용하여 통신합니다. 
![](https://images.velog.io/images/anjaekk/post/004e3fc7-0970-4b4f-9bac-0fe42072f314/image.png)

> 📂 [이미지 출처-docker.docs](https://docs.docker.com/get-started/overview/)

#### Daemon(Server)
Docker Daemon(dockerd)은 Docker API 요청을 수신하고 이미지, 컨테이너, 네트워크 볼륨과 같은 Docker 객체들을 관리합니다. Daemon은 서비스를 관리하기 위해 다른 Daemon과 통신할 수 있습니다. 

#### Client(Docker CLI)
사용자가 Docker CLI에 커맨드를 입력하면 Docker Client에서 Daemon(=Server)로 명령을 전송하게 됩니다. 

#### Registries
Docker Registry는 도커 이미지가 저장되어있는 장소로써 Docker Hub나 Quay 또한 registry에 속합니다. registry는 `public registry`와 `private registry`가 존재합니다. 

#### Objects
- Images
이미지는 도커 컨테이너를 만들기(build)위한 지침과 같은 것으로 읽기전용 템플릿입니다.(컨테이너를 만들기 위한 설계도라고 생각할 수 있겠습니다.) 자신만의 이미지를 만들 수도 있고 다른 사용자가 만든 이미지를 pull받아 사용할 수 있습니다. 자신만의 이미지를 빌드하려면 Dockerfile에 명령문을 작성하면 됩니다.

- Containers
컨테이너는 이미지의 실행가능한 인스턴스입니다. 컨테이너 생성시 해당 이미지에서 정의한 파일 시스템, 파일들 그리고 격리된 시스템 자원 및 네트워크를 사용할 수 있는 독립된 공간이 생성됩니다.(컨테이너에서의 변경은 이미지에 영향을 주지 않습니다.) 
Docker API 또는 CLI를 사용하여 컨테이너를 생성, 시작, 중지, 이동 또는 삭제를 할 수 있습니다. 
 
<br>

#### _+) 추가_
**Layer**
이미지에서 Layer는 Dockerfile의 명령으로 생성됩니다.  
기본 이미지에 Layer를 순서대로 적용하여 최종 이미지를 만들어 내는데 즉, 이미지는 여러개의 읽기전용(read only) Layer로 구성되어 있고 파일이 추가되거나 수정되면 새로운 Layer가 생성됩니다. 변경되지 않은 Layer는 로컬에 캐시되고 변경된 Layer만 업데이트 되기 때문에 이미지 빌드시 빠르게 할 수 있습니다. 컨테이너를 생성할 때도 Layer 방식을 사용하는데 기존 읽기전용 Layer 위에 읽기/쓰기(read-write) Layer를 추가하게 됩니다. 

![](https://images.velog.io/images/anjaekk/post/e310b2b6-ba9f-4dd1-b6b7-66ca507fe65a/image.png)

> 📂 [이미지 출처-docker.docs](https://docs.docker.com/storage/storagedriver/)


<br>

## Docker run 실행과정
ubuntu 컨테이너를 docker run 명령으로 실행했을 때의 과정을 알아봅시다.
```
$ docker run -i -t ubuntu /bin/bash
```
**1. ubuntu 이미지 가져오기**
- ubuntu 이미지가 로컬에 없는 경우 `docker pull ubuntu`를 실행한 것과 동일하게 레지스트리에서 이미지를 가져옵니다. 

**2. 컨테이너 생성**
- `docker container create` 명령을 실행한 것과 동일하게 새 컨테이너를 생성합니다.

**3. 읽기, 쓰기 파일 시스템을 최종 계층으로 할당**
- 읽기, 쓰기 레이어를 추가하여 실행중인 컨테이너가 로컬 파일 시스템에서 파일 및 디렉토리를 생성하거나 수정할 수 있습니다.

**4. IP주소 할당**
- 별도의 네트워크 설정을 해주지 않았음으로 기본 네트워크에 연결하는 네트워크 인터페이스를 만듭니다.(IP 주소 할당)

**5. 컨테이너 시작**
- /bin/bash가 실행됩니다. -i, -t 플래그로 인해 터미널에서 입력할 수 있습니다.    
_+) -it 옵션: 컨테이너를 종료하지 않고 터미널의 입력을 컨테이너로 전달하기 위해 사용_   
_+) exit를 입력하면 컨테이너가 중지되지만 제거되지는 않으니 다시 시작할 수 있습니다._  

<br>

> 참조   
> 🔗 [도커 문서 | 도커 개요](https://docs.docker.com/get-started/overview/)   
> 🔗 [[Docker] 개념 정리 및 사용방법까지. | HY's Farm 블로그](https://cultivo-hy.github.io/docker/image/usage/2019/03/14/Docker%EC%A0%95%EB%A6%AC/)   
> 🔗 [개발자를 위한 도커입문 실습 PART1 - 도커 이미지와 컨테이너 | Reimaginer 블로그](https://www.reimaginer.me/entry/docker-hands-on-part1)   
