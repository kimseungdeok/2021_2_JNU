import pandas as pd
pd.set_option('mode.chained_assignment',  None) # Warning 방지용
import numpy as np

# --------------------------------------
# 2차시 : 블록맵 시각화 데이터 준비 
# --------------------------------------


data = pd.read_csv('d:/bd/ch9/공공보건의료기관현황.csv', index_col=0, encoding='CP949', engine='python')

data.head() #작업내용 확인용 출력

## 주소에서 시도, 군구 정보 분리


temp = data['주소']
# 람다함수     lambda 매개변수: 처리내용
result = temp.apply(lambda v: v.split()[:2]).tolist()
temp2 = pd.DataFrame(result, columns=('시도', '군구'))


addr = pd.DataFrame(data['주소'].apply(lambda v: v.split()[:2]).tolist(),columns=('시도', '군구'))

addr.head()  #작업내용 확인용 출력

addr['시도'].unique()
addr[addr['시도'] == '창원시']
addr.iloc[27]
addr.iloc[27] = ['경상남도', '창원시']
addr.iloc[31] = ['경상남도', '창원시']

addr[addr['시도'] == '천안시']
## 표준 행정구역 이름으로 수정 : 천안시-> 충청남도 천안시
addr.iloc[209]
addr.iloc[210]
addr.iloc[209] = ['충청남도', '천안시']
addr.iloc[210] = ['충청남도', '천안시']

## 표준 행정구역 이름으로 수정 :  경기 -> 경기도, 경남 -> 경상남도, ...
addr_aliases = {'경기':'경기도', '경남':'경상남도', '경북':'경상북도', '충북':'충청북도', \
                '서울시':'서울특별시', '부산특별시':'부산광역시', '대전시':'대전광역시', \
                '충남':'충청남도', '전남':'전라남도', '전북':'전라북도'}
    
addr_aliases.get('경기')
addr_aliases.get('경남')
addr_aliases.get('뉴욕', '없다')

#딕셔너리.get(K, default) => 딕셔너리 addr_aliases 에서 키값이 K에 대응하는 value값을 return하고, K에 해당하는 키가 없으면  default 리턴 

addr['시도']= addr['시도'].apply(lambda v: addr_aliases.get(v,v))

addr['시도'].unique()
addr['군구'].unique()
addr[addr['군구'] == '아란13길']
addr.iloc[75] = ['제주특별자치도', '제주시']

addr.iloc[75]

#   (1) '시도' 와 '군구' 컬럼 결합하기

addr['시도군구'] = addr.apply(lambda r: r['시도'] + ' ' + r['군구'], axis=1)

addr.head() #작업 확인용 출력
addr['count'] = 0  # 의료기관수 합계를 저장할 컬럼 만들기

addr.head() #작업 확인용 출력

#  (2) '시도군구' 를 기준으로 그룹을 만들고, 그룹별 의료기관수 합계 구하기

addr_group =pd.DataFrame(addr.groupby(['시도', '군구', '시도군구'], as_index=False).count())

addr_group.head()  #작업 확인용 출력

addr_group =pd.DataFrame(addr.groupby(['시도', '군구', '시도군구'], as_index=False).count())

addr_group.head()  #작업 확인용 출력

# (3) 데이터 병합에 사용할 인덱스 설정하기

addr_group2 = addr_group.set_index("시도군구")  #'시도군구' 열을 기준으로 인덱스(행표시자) 설정

addr_group.head()   #작업 확인용 출력


# (3) 데이터 병합에 사용할 인덱스 설정하기
#(1) 행정구역 이름 데이터 불러오기 : 행정구역_시군구_별__성별_인구수_2.xlsx

population = pd.read_excel('d:/bd/ch9/행정구역_시군구_별__성별_인구수2_.xlsx')

population.head()    #작업 확인용 출력

population = population.rename(columns = {'행정구역(시군구)별(1)': '시도', '행정구역(시군구)별(2)': '군구'}) #컬럼이름 변경

population.head()  #작업 확인용 출력

# '군구' 컬럼에서 공백 제거하기
for element in range(0,len(population)):
      population['군구'][element] = population['군구'][element].strip()  #'군구'열의 값들에서 양쪽 공백 삭제 

# '시도'와 '군구'를 연결하여 '시도군구' 컬럼 추가
population['시도군구']= population.apply(lambda r: r['시도'] + ' ' + r['군구'], axis=1)

population.head()  #작업 확인용 출력

# 필요없는 '소계' 행 삭제

population = population[population.군구 != '소계']

population.head()  #작업 확인용 출력
population2 = population.set_index("시도군구")

population.head()  #작업 확인용 출력 

# 5) '의료기관' 데이터프레임과 '시도군구별 인구수' 데이터프레임 병합하기

addr_population_merge = pd.merge(addr_group2, population2,  how='inner',  left_index=True, right_index=True)
# how='inner' : 병합 기준 열의 값들이 같은 행들만 병합 
#left_index = True : 병합대상 왼쪽 데이터프레임은 인덱스 열을 기준으로 병합  
#right_index = True : 병합대상 오른쪽 데이터프레임은 인덱스 열을 기준으로 병합  

addr_population_merge.head()   #작업 확인용 출력

# 필요한 컬럼만 추출하기
local_MC_Population = addr_population_merge[['시도_x', '군구_x',  'count', '총인구수 (명)']]

local_MC_Population.head()   #작업 확인용 출력  
#컬럼이름 변경
local_MC_Population = local_MC_Population.rename(columns = {'시도_x': '시도', '군구_x': '군구','총인구수 (명)': '인구수' })

local_MC_Population.head()  #작업 확인용 출력

# 6) 시도군구의 인구대비 의료기관수 비율 구하기
MC_count = local_MC_Population['count']
test = MC_count.div(100, axis=0)
#axis = 0 : 행 단위
#axis =1: 행단위 
local_MC_Population['MC_ratio'] = MC_count.div(local_MC_Population['인구수'], axis=0)*100000


local_MC_Population.head()   #작업 확인용 출력

local_MC_Population.to_csv('d:/bd/ch9/local_MC_Population.csv', encoding='euc-kr') 












