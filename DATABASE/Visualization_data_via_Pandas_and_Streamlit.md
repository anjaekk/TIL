# Streamlit
Stremlit은 오픈소스 파이썬 라이브러리로 웹 어플리케이션 툴이다. Streamlit에서는 데이터 애플리케이션을 구축하고 공유하는데 가장 빠른 방법이라고 소개하고 있다. 

> 📂 [Streamlit Documentation](https://docs.streamlit.io/library/get-started)   
> 📂 [Streamlit Github](https://github.com/MarcSkovMadsen/awesome-streamlit)

### Streamlit 장점
- 간단한 파이썬 코드로 앱을 빌드할 수 있으며 별도의 FE작업이 필요없다.
- 디버그 모드 사용가능(always rerun 활성화시 소스코드가 변경되면 앱이 업데이트 된다.)
- 캐싱을 통해 앱 재빌드시 시간 단축이 가능하다.
- 그 외 다양한 라이브러리 제공

<br>

## Streamlit 시작하기
### streamlit 설치
```
pip install streamlit
```

### streamlit 실행
streamlit은 아래 명령어로 간단하게 실행할 수 있으며 소스 코드 수정시 바로 반영되기 때문에 처음 시작할때 실행시켜놓으면 편하다. 소스코드 파일명을 `data_app.py`라고 하고 진행하겠다. 
```
streamlit run data_app.py
```
streamlit 실행시 아래와 같은 화면이 나오게 되고 `enter`를 누르면 새 브라우저 탭으로 시각화 된 데이터를 확인할 수 있다.
![](https://images.velog.io/images/anjaekk/post/f2a089c0-b163-4914-8fc5-024fe1524b8d/image.png)

<br>

## 데이터 시각화 실습
서울교통공사의 월벌 하차인원 데이터를 가져와 간단한 그래프를 만들어보도록 한다. 실습해볼 내용을 정리해보자면 아래와 같다. 
- data 저작권 정보 링크 삽입 - 버튼 클릭시 등장
- raw data 전체 - 체크박스 선택시 등장
- 역별 하차 인원 - 드롭박스에서 원하는 역을 선택
- 전체 역별 하차 인원 - multiple lines chart
- 호선별 하차 인원 - 데이터 groupby 후 드롭박스에서 원하는 호선을 선택

### csv로 된 data 가져오기

```
import streamlit as st
import pandas as pd

st.title('2021 서울교통공사 지하철 월별 하차 인원')

df = pd.read_csv('./monthly_subway_statistics_in_seoul.csv', encoding='cp949')
df.set_index = df['연번']
```
- `st.title` : title을 이용해 데이터 title을 정해준다. 
- 이후 csv파일을 가져와 한글이 보일 수 있도록 cp949로 encoding 
- `df.set_index = df['연번']` : 연번이 들어가있는 데이터이니 연번을 index로 설정해준다


### data 저작권 정보 링크 삽입
```
if st.button('data copyright link'):
    st.write('https://www.data.go.kr/data/15044247/fileData.do')
```
- `st.button('data copyright link')` : 버튼의 이름을 `data copyright link`로 생성해준다. 

![](https://images.velog.io/images/anjaekk/post/3b3af4ce-00e6-495e-a57c-88643700b754/image.png)

버튼 클릭시 아래와 같이 링크가 나타나는 걸 확인 할 수 있다.

![](https://images.velog.io/images/anjaekk/post/a096707e-ca8b-42e2-a275-a2550ed24fee/image.png)

### raw data 전체 
```
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)
```
이렇게 하게되면 체크박스 선택시 rawdata가 등장하게되고 해지시 사라지게 된다.

![](https://images.velog.io/images/anjaekk/post/82b50b0b-b688-4b34-9479-6d61dda4d3a9/image.png)

### 역별 하차 인원
드롭박스를 통해 역을 선택하고 그 역에 해당하는 데이터를 area chart로 확인할 수 있도록 하겠다.
(area chart는 꺾은선 그래프에서 안이 채워져있는 그래프이다.)

```
st.subheader('역별 하차 인원')
option = st.selectbox(
    'Select Line', 
    (df['역명']))

station_data = df.loc[(df['역명'] == option)]
station_data = station_data[station_data.columns.difference(['연번', '호선', '역번호', '역명'])]
s_index = station_data.index.tolist()
st.area_chart(station_data.loc[s_index[0]], use_container_width=True
)
```
- `st.subheader` : 부제목을 달아준다.
- `st.selectbox` : 선택박스를 만들고 csv로 다운받은 dataframe의 역명을 넣도록 한다.
- `df.loc[(df['역명'] == option)]` : 해당하는 역의 row를 데이터를 loc로 가져온다. 
- `station_data.columns.difference(['연번', '호선', '역번호', '역명'])` : 그래프에 해당하지 않는 자료는 제외하도록한다.
- `station_data.loc[s_index[0]]` : 인덱스에 해당하는 row를 가져오도록 하고 `use_container_width=True`로 가로 화면에 꽉 차도록 설정

![](https://images.velog.io/images/anjaekk/post/aa430783-75f9-4089-bae1-2a9989ffaf68/image.png)

### 전체 역별 하차 인원
```
st.subheader('전체 역별 하차 인원')
e_station = df[['역명', '2021년1월', '2021년2월', '2021년3월', '2021년4월',
       '2021년5월', '2021년6월', '2021년7월', '2021년8월', '2021년9월', '2021년10월', '2021년11월']].transpose()
e_station.rename(columns=e_station.iloc[0], inplace=True)
e_station = e_station.drop(e_station.index[0])
st.line_chart(e_station)
```

- `df[['역명', '2021년1월',... '2021년11월']].transpose()` : csv로 가져온 데이터의 컬럼 순서를 정확히 하도록하기위해서(역명을 맨 앞으로 가져오기위해서) column순서를 나열해서 정비해주고 	`pandas`의 `transpose()`를 이용해 데이터의 행, 열을 전환해 주었다.

   - 기존 데이터
    ![](https://images.velog.io/images/anjaekk/post/a6470704-381c-4000-84ed-052e8ffee4ea/image.png)

   - 행, 열 전환 후 데이터
   ![](https://images.velog.io/images/anjaekk/post/51678b4b-a424-4384-9b36-3a4a17a11c0f/image.png)

- `e_station.drop(e_station.index[0])` : 맨위에있는 인덱스 행을 없애주도록 한다.

![](https://images.velog.io/images/anjaekk/post/5ec6cded-5dcb-47c6-8498-17edebb4b984/image.png)

### 호선별 하차 인원
```
st.subheader('호선별 하차 인원')
df_line = df.groupby('호선').sum()
lines = df_line.index.tolist()
option = st.selectbox(
    'Select Line', 
    (lines))

line_data = df_line.loc[(df_line.index == option)]
line_data = line_data[line_data.columns.difference(['연번', '호선', '역번호', '역명'])]
l_index = line_data.index.tolist()
st.area_chart(line_data.loc[l_index[0]], use_container_width=True)
```

- `df.groupby('호선').sum()` : `groupby`를 이용해 호선명을 기준으로 합으로 합쳐준다. 

![](https://images.velog.io/images/anjaekk/post/24794ceb-32c7-4a01-aaf8-c639de6a0549/image.png)


컬럼의 타입을 datetime으로 변경하게되면 날짜순으로 이어질텐데 우선 streamlit을 사용해보는 것을 중점으로 해봤다. 이외에도 멋져보이는 그래픽들이 많았지만 우선 기본적인 걸로 이해를 해봤으니 다음에는 조금더 고차원적인 데이터 시각화를 해보고 싶다.
