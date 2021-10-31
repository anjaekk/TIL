## 들어가기 전에... 
### 웹 크롤링과 스크래핑
웹 스크래핑에 대해 알아보기전 헷갈리기 쉬운 크롤링과 스크래핑의 차이점에 대해 알아보고 가자.      
이 둘은 웹을 탐색한다는 공통점이 있지만 가장 큰 차이점은 목적이 있느냐 없느냐, 데이터를 추출해서 저장하느냐 아니냐이다. 크롤러는 spider라고도 불리는데 목적이나 특별한 목표 없이 사이트나 네트워크가 제공하는 것을 계속해서 탐색하는 것을 말한다. 
그에 반해 스크래핑은 특정 목적을 가지고 그에 맞는 특정 정보를 검색하고 추출하여 저장하는 작업을 말한다.     
이 둘은 완전히 구분되는 개념이 아니라 스크래핑을 위해서는 클롤링이 필요하고 클롤링을 하면 스크래핑을 해야하는 칭구칭구 사이이다. 그리고 그 둘을 그렇게 크게 구분하여 사용하지도 않는다!
# 편한 작업을 위해
## Jupyterlab
```
pip install jupyterlab
```
- `enter + shift` : 코드 실행
## 개발자도구
#### mac
```
command + option + i
```

#### windows
```
F12
```
# 1. 원하는 데이터 목록까지 접근하기
원하는 데이터 목록까지 접근을 위해 Selenium을 이용하도록 한다.
## Selenium
- Selenium WebDriver는 웹 어플리케이션을 테스팅할 때 사용하실 수 있는 무료 도구이며, API를 제공하는 오픈소스 프레임워크
- beautiful soup에서 다룰 수 없는 동적인 부분은 selenium을 이용한다.
### 1.1 Selenium 설치
```
pip install selenium
```

### 1.2 web driver 설치
크롬을 사용한 스크래핑을 진행할 예정이기 때문에 chrome web driver를 다운받아 사용하도록 한다.
[web driver 다운로드](https://chromedriver.chromium.org/downloads)

다운로드 받은 web driver 위치를 변경해준다.
```
sudo mv chromedriver /usr/local/bin
```

잘 설치가 됐는지 확인해본다.
```
import selenium
from selenium import webdriver

driver = webdriver.Chrome()
```
위의 코드를 Jupyterlab을 통해 실행시켰을 때 비어있는 chrome 브라우져가 열린다면 성공!
> web driver의 위치를 옮기기 싫다면
```
driver = webdriver.Chrome("Web Driver의 경로")
```
> 위와 같이 코트를 넣어주면 된다. 

### 1.3 로그인
만약 원하는 데이터가 로그인을 해야만 얻을 수 있다면 selenium을 이용해 로그인을 해주도록 한다.
```
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


user = "id 넣기"
password = "pw 넣기"

driver = webdriver.Chrome()
driver.get("사이트 로그인페이지 url")
assert "그 사이트 title" in driver.title

elem = driver.find_element_by_id("id")
elem.send_keys(user)
elem = driver.find_element_by_id("pw")
elem.send_keys(password)
elem.send_keys(Keys.RETURN)
```

- assert: 해당 사이트 html title이 지정해놓은 title과 맞지 않으면 에러를 내보내도록 하는 예외처리
- `elem = driver.find_element_by_id("id")`: 개발자도구를 이용하여 확인한 해당 자리의 id값을 입력
- `elem.send_keys(user)`: id 입력
`elem.send_keys(Keys.RETURN): enter` 키 누르기



### 1.4 해당 메뉴 들어가기
개발자 도구를 통해 내가 원하는 부분의 값이 `<a href="~~url">메뉴이름</a>`와 같이 단순 href로 되어있는지 아니면 `<a href="#" onclick="~~">` 이런씩으로 on click인지 확인하여 접근한다.

#### 링크형
```
a = driver.find_elements_by_xpath("XPath 넣기")
driver.get(a[0].get_attribute("href"))
```
링크형은 개발자도구에서 해당 부분 지정 후 마우스 오른쪽 클릭 -> Copy -> Copy XPath 를 통해 복사한 XPath를 사용한다.

#### on click형
```
a = driver.find_element_by_css_selector("selector 값 넣기")
a.send_keys("\n")
```
- a.send_keys("\n"): enter 누르기

on click형은 개발자도구에서 해당 부분 지정 후 마우스 오른쪽 클릭 -> Copy -> Copy selector를 통해 복사한 selector 값을 사용한다. 


>_이 과정에서 path 오류가 난다면 를 코드를 통해 지연시간을 사이에 넣어주도록 한다._
```
import time
time.sleep(2)
```

### 1.5 드롭다운 목록 선택
드롭다운을 통해 특정 목록을 선택해야하는 경우에는 아래의 세가지 방법중 하나를 선택해서 할 수 있다.(3번째 줄 코드가 다름!)

#### - 인덱스 순서에 따라 선택하기

```
from selenium.webdriver.support.select import Select
select_menu=Select(driver.find_element_by_id("해당 드롭다운 id"))
select.select_by_index(1)
```

#### - 메뉴의 텍스트 값으로 선택하기

```
from selenium.webdriver.support.select import Select
select_menu=Select(driver.find_element_by_id("해당 드롭다운 id"))
select.select_by_visible_text("메뉴명")
```

#### - value값으로 선택하기

```
from selenium.webdriver.support.select import Select
select_menu=Select(driver.find_element_by_id("해당 드롭다운 id"))
select.select_by_value("value 값")
```

# 2. 데이터 가져오기
## Beautifulsoup
- HTML과 XML 문서의 parsing을 하기 위한 Python 라이브러리

### 2.1 beautifulsoup 설치
- 우선 beautifulsoup 패키지를 다운받아 준다.
```
pip install bs4
```

### 2.2 페이지 소스 가져오기
web driver를 이용해 해당 페이지 소스를 가져온다.

```
page_source = driver.page_source 
soup = BeautifulSoup(page_source, "html.parser")
```

- driver는 위에서 `driver = webdriver.Chrome()`로 설정한 web driver이다.
- soup = BeautifulSoup(page_source, "html.parser")


### 2.3 해당 데이터 가져오기
#### selector 이용

selector Path를 이용해 값을 가져온다. 
```
contents = soup.select("selector Path 값")
```

- 원하는 데이터 부분의 path값을 가져온 후 for문을 이용해 값을 추출하도록한다. 



<br>

> 참조   
> 🔗 [웹 크롤링과 웹 스크래핑의 차이점 | 지구별모험가 블로그](https://98yejin.github.io/2020-11-02-crawling-vs-scraping/)      
> 🔗 [파이썬 크롤링 튜토리얼 | 개발새발 블로그](https://l0o02.github.io/2018/06/13/selenium-with-beautifulsoup-1/)         

