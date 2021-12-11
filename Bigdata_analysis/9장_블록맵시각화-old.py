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
#axis = 0 : 열 단위
#axis =1: 행단위 
local_MC_Population['MC_ratio'] = MC_count.div(local_MC_Population['인구수'], axis=0)*100000


local_MC_Population.head()   #작업 확인용 출력
local_MC_Population.to_csv("d:/bd/ch9/local_MC_Populatio.csv")
local_MC_Population.to_csv("d:/bd/ch9/local_MC_Population.csv", encoding='euc-kr')
# --------------------------------------------------
# 3차시 : 블록맵을 위한 분석모델 구축 및 시각화  
# --------------------------------------------------

#  바 차트 그리기

from matplotlib import pyplot as plt
from matplotlib import rcParams, style
style.use('ggplot')

from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

# (1) 행정구역별 공공보건의료기관수에 대한 바 차트
MC_ratio = local_MC_Population[['count']]
MC_ratio = MC_ratio.sort_values('count', ascending = False)
plt.rcParams["figure.figsize"] = (30,10)
plt.rcParams["font.size"]=15  

# 기본 그래프 크기 설정 : plt.rcParams["figure.figsize"] = (14,4)
#기본 글자 크기 설정 :  plt.rcParams["font.size"]=15  

MC_ratio.plot(kind='bar', rot=90)
plt.show()


# (2) 행정구역별 인구수 대비 공공보건의료기관 비율에 대한 바 차트

MC_ratio = local_MC_Population[['MC_ratio']]
MC_ratio = MC_ratio.sort_values('MC_ratio', ascending = False)
plt.rcParams["figure.figsize"] = (25,5)
MC_ratio.plot(kind='bar', color='blue', rot=90)
plt.show()


# (3) 블록맵 데이터 파일 열기
import pandas as pd
import os
path = os.getcwd()


# data_draw_korea = pd.read_csv('d:/bd/ch9/data_draw_korea.csv', index_col=0, encoding='CP949', engine='python') 
data_draw_korea = pd.read_csv(path+'\\data_draw_korea.csv', index_col=0, encoding='euc-kr', engine='python')
#data_draw_korea = pd.read_csv(path+'\\data_draw_korea.csv', index_col=0, encoding='CP949', engine='python')

data_draw_korea.head()   #작업 확인용 출력

# (4) 블록맵 데이터 파일에 '시도군구' 컬럼 만들기

data_draw_korea['시도군구']= data_draw_korea.apply(lambda r: r['광역시도'] + ' ' + r['행정구역'], axis=1)

data_draw_korea.head()  #작업 확인용 출력


# (5) 블록맵 데이터에서 병합에 사용할 '시도군구' 컬럼을 인덱스로 설정하기

data_draw_korea2 = data_draw_korea.set_index("시도군구")

data_draw_korea2.head()  #작업 확인용 출력

#(6) 블록맵 데이터프레임과 local_MC_Population을 병합하기

data_draw_korea_MC_Population_all = pd.merge(data_draw_korea2,local_MC_Population,  how='outer',  left_index=True, right_index=True)
# how='outer'(외부병합) : 병합 기준 열의 값들이 같지 않은 행들도 병합 
#left_index = True : 병합대상 왼쪽 데이터프레임은 인덱스 열을 기준으로 병합  
#right_index = True : 병합대상 오른쪽 데이터프레임은 인덱스 열을 기준으로 병합  


data_draw_korea_MC_Population_all.head()


# (7) 한국지도의 블록맵 경계선 좌표를 리스트로 생성

BORDER_LINES = [
    [(3, 2), (5, 2), (5, 3), (9, 3), (9, 1)], # 인천
    [(2, 5), (3, 5), (3, 4), (8, 4), (8, 7), (7, 7), (7, 9), (4, 9), (4, 7), (1, 7)], # 서울
    [(1, 6), (1, 9), (3, 9), (3, 10), (8, 10), (8, 9),
     (9, 9), (9, 8), (10, 8), (10, 5), (9, 5), (9, 3)], # 경기도
    [(9, 12), (9, 10), (8, 10)], # 강원도
    [(10, 5), (11, 5), (11, 4), (12, 4), (12, 5), (13, 5),
     (13, 4), (14, 4), (14, 2)], # 충청남도
    [(11, 5), (12, 5), (12, 6), (15, 6), (15, 7), (13, 7),
     (13, 8), (11, 8), (11, 9), (10, 9), (10, 8)], # 충청북도
    [(14, 4), (15, 4), (15, 6)], # 대전시
    [(14, 7), (14, 9), (13, 9), (13, 11), (13, 13)], # 경상북도
    [(14, 8), (16, 8), (16, 10), (15, 10),
     (15, 11), (14, 11), (14, 12), (13, 12)], # 대구시
    [(15, 11), (16, 11), (16, 13)], # 울산시
    [(17, 1), (17, 3), (18, 3), (18, 6), (15, 6)], # 전라북도
    [(19, 2), (19, 4), (21, 4), (21, 3), (22, 3), (22, 2), (19, 2)], # 광주시
    [(18, 5), (20, 5), (20, 6)], # 전라남도
    [(16, 9), (18, 9), (18, 8), (19, 8), (19, 9), (20, 9), (20, 10)], # 부산시
]


# (8) 블록맵에서 블록에 해당 데이터를 매핑하여 색을 표시하는 함수


blockedMap = data_draw_korea_MC_Population_all
blockedMap.x.unique()
blockedMap.y.unique()
blockedMap['count'].unique()

addr['군구'].unique()

#result = blockedMap['count'].fillna(0)
#blockedMap['count2'] = result
#mapdata = blockedMap.pivot(index='y', columns='x', values='count2')

#r = blockedMap
#r['x']
#blockedMap.duplicated().sum()

#test = blockedMap['count']

#del(blockedMap.iloc[0])
#blockedMap.drop(index=0)
#for r1 in range(0, len(blockedMap)):
#    print(blockedMap.iloc[r1])
#
#blockedMap['시도군구'] #에러 발생 => '시도군구' 열이 index열이라서? 
temp = []
id = range(0, len(blockedMap))
blockedMap['id'] = id
blockedMap.columns
blockedMap2 = blockedMap.set_index('id')


dup = {}
for i in range(0, len(blockedMap)):
    r1 = blockedMap.iloc[i]
    x1 = r1[2]
    y1 = r1[3]
    dup[i] = []
    for j in range(i+1, len(blockedMap)):
        r2 = blockedMap.iloc[j]
        x2 = r2[2]
        y2 = r2[3]
        if x1 == x2 and y1 == y2  :
            print(i, '행:', blockedMap.iloc[i]['시도'], blockedMap.iloc[i]['군구'], blockedMap.iloc[i]['count'])
            print(j, '행:', blockedMap.iloc[j]['시도'], blockedMap.iloc[j]['군구'], blockedMap.iloc[j]['count'])
            dup[i].append(j)
            
import itertools
            
del_list = list(dup.values())   

del_list = list(itertools.chain(*del_list))
'''
itertools를 이용한 방법
itertools를 이용하여 2차원 리스트를 1차원 리스트로 만들 수 있습니다. itertools.chain()는 인자로 전달되는 iterable의 데이터를 연결하여 리턴해 줍니다. 명심해야하는 것은 인자 앞에 *를 붙여주어야 하는 것입니다.
'''

temp = []
temp_col = blockedMap.columns
for i in range(0, len(blockedMap)):
    if i not in del_list:
        temp.append(blockedMap.iloc[i])
result = pd.DataFrame(temp, columns=temp_col)        
    
           
            
def draw_blockMap(blockedMap, targetData, title, color ):
    whitelabelmin = (max(blockedMap[targetData]) - min(blockedMap[targetData])) * 0.25 + min(blockedMap[targetData])

    datalabel = targetData

    vmin = min(blockedMap[targetData])
    vmax = max(blockedMap[targetData])

    mapdata = blockedMap.pivot(index='y', columns='x', values=targetData)
    masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)
    
    plt.figure(figsize=(8, 13))
    plt.title(title)
    plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=color, edgecolor='#aaaaaa', linewidth=0.5)

    # 지역 이름 표시
    for idx, row in blockedMap.iterrows():
        annocolor = 'white' if row[targetData] > whitelabelmin else 'black'
    
        # 광역시는 구 이름이 겹치는 경우가 많아서 시단위 이름도 같이 표시한다. (중구, 서구)
        if row['광역시도'].endswith('시') and not row['광역시도'].startswith('세종'):
            dispname = '{}\n{}'.format(row['광역시도'][:2], row['행정구역'][:-1])
            if len(row['행정구역']) <= 2:
                dispname += row['행정구역'][-1]
        else:
            dispname = row['행정구역'][:-1]

        # 서대문구, 서귀포시 같이 이름이 3자 이상인 경우에 작은 글자로 표시한다.
        if len(dispname.splitlines()[-1]) >= 3:
            fontsize, linespacing = 9.5, 1.5
        else:
            fontsize, linespacing = 11, 1.2

        plt.annotate(dispname, (row['x']+0.5, row['y']+0.5), weight='bold',
                     fontsize=fontsize, ha='center', va='center', color=annocolor,
                     linespacing=linespacing)
    
    # 시도 경계 그린다.
    for path in BORDER_LINES:
        ys, xs = zip(*path)
        plt.plot(xs, ys, c='black', lw=4)

    plt.gca().invert_yaxis()
    #plt.gca().set_aspect(1)
    plt.axis('off')
    
    cb = plt.colorbar(shrink=.1, aspect=10)
    cb.set_label(datalabel)

    plt.tight_layout()
    
    plt.savefig('d:/bd/ch9/blockMap_' + targetData + '.png')
                      
    
    plt.show()      




 # (9)함수를 호출하여 블록맵 생성하기

draw_blockMap(result, 'count', '행정구역별 공공보건의료기관 수', 'Blues')
#draw_blockMap(data_draw_korea_MC_Population_all, 'count', '행정구역별 공공보건의료기관 수', 'Blues')
draw_blockMap(result, 'MC_ratio', '행정구역별 인구수 대비 공공보건의료기관 비율', 'Reds' )
#draw_blockMap(data_draw_korea_MC_Population_all, 'MC_ratio', '행정구역별 인구수 대비 공공보건의료기관 비율', 'Reds' )
























