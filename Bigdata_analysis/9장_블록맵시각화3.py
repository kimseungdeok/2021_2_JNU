
# --------------------------------------------------
# 3차시 : 블록맵을 위한 분석모델 구축 및 시각화  
# --------------------------------------------------

import pandas as pd
pd.set_option('mode.chained_assignment',  None) # Warning 방지용
import numpy as np

# --------------------------------------
# 행정구역별 공공의료기관수 정보 읽음
# --------------------------------------

local_MC_Population = pd.read_csv('d:/bd/ch9/local_MC_Population.csv', index_col=0, encoding='euc-kr', engine='python')

local_MC_Population .head() #작업내용 확인용 출력

#--------------------------------------
#  바 차트 그리기
#--------------------------------------

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

MC_ratio.plot(kind='bar', color="red", rot=90)
plt.show()


# (2) 행정구역별 인구수 대비 공공보건의료기관 비율에 대한 바 차트
# 인구 100000명 당 공공의료기관 수 

MC_ratio = local_MC_Population[['MC_ratio']]
MC_ratio = MC_ratio.sort_values('MC_ratio', ascending = False)
plt.rcParams["figure.figsize"] = (25,5)
MC_ratio.plot(kind='bar', color='blue', rot=90)
plt.show()


#--------------------------------------
# 블록맵 그리기 위한 데이터 준비 
#--------------------------------------

# (3) 블록맵 데이터 파일 열기
import pandas as pd
import os
path = os.getcwd()



data_draw_korea = pd.read_csv(path+'\\data_draw_korea.csv', index_col=0, encoding='euc-kr', engine='python')


data_draw_korea.head()   #작업 확인용 출력

# (4) 블록맵 데이터 파일에 '시도군구' 컬럼 만들기

data_draw_korea['시도군구']= data_draw_korea.apply(lambda r: r['광역시도'] + ' ' + r['행정구역'], axis=1)

data_draw_korea.head()  #작업 확인용 출력



# (5) 블록맵 데이터에서 병합에 사용할 '시도군구' 컬럼을 인덱스로 설정하기

data_draw_korea2 = data_draw_korea.set_index("시도군구")

data_draw_korea2.head()  #작업 확인용 출력

#(6) 블록맵 데이터프레임과 local_MC_Population을 병합하기
# 공공의료기관 현황 데이터와 블록맵 데이터를 병합 

data_draw_korea_MC_Population_all = pd.merge(data_draw_korea2,local_MC_Population,  how='outer',  left_index=True, right_index=True)
# how='outer'(외부병합) : 병합 기준 열의 값들이 같지 않은 행들도 병합 
#left_index = True : 병합대상 왼쪽 데이터프레임은 인덱스 열을 기준으로 병합  
#right_index = True : 병합대상 오른쪽 데이터프레임은 인덱스 열을 기준으로 병합  


data_draw_korea_MC_Population_all.head()

id = list(range(0,len(data_draw_korea_MC_Population_all)))
data_draw_korea_MC_Population_all['id'] = id 

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



# (8) 중복행 확인 및 제거
# data_draw_korea_MC_Population_all(공공의료기관현황데이터 + 블록맵 데이터 병합 결과)의 중복행 제거
'''
99 행: 대구광역시 북구('광역시도')  2.0 ('count')
100 행: 대구광역시 북구 2.0
101 행: 대구광역시 서구 2.0
102 행: 대구광역시 서구 2.0
101 행: 대구광역시 서구 2.0
103 행: 대구광역시 서구 2.0
102 행: 대구광역시 서구 2.0
103 행: 대구광역시 서구 2.0
105 행: 대구광역시 중구 2.0
106 행: 대구광역시 중구 2.0
108 행: 대전광역시 동구 1.0
109 행: 대전광역시 동구 1.0
112 행: 대전광역시 중구 1.0
113 행: 대전광역시 중구 1.0
153 행: 서울특별시 중구 1.0
154 행: 서울특별시 중구 1.0
'''

# dup :  중복행 포함하는 딕셔너리 {key:value} key:행번호, value: 중복행번호

dup = {}
for i in range(0, len(data_draw_korea_MC_Population_all)):
    r1 = data_draw_korea_MC_Population_all.iloc[i]
    x1 = r1[2]
    y1 = r1[3]
    dup[i] = []
    for j in range(i+1, len(data_draw_korea_MC_Population_all)):
        r2 = data_draw_korea_MC_Population_all.iloc[j]
        x2 = r2[2]
        y2 = r2[3]
        if x1 == x2 and y1 == y2  :
            print(i, '행:', \
                  data_draw_korea_MC_Population_all.iloc[i]['시도'], \
                  data_draw_korea_MC_Population_all.iloc[i]['군구'],\
                  data_draw_korea_MC_Population_all.iloc[i]['count'])
            print(j, '행:', \
                  data_draw_korea_MC_Population_all.iloc[j]['시도'], \
                  data_draw_korea_MC_Population_all.iloc[j]['군구'], \
                  data_draw_korea_MC_Population_all.iloc[j]['count'])
            dup[i].append(j)
            
import itertools
            
# 딕셔너리형(dup)을 리스트형(2차원=> 리스트 요소값이 리스트형)으로 변환  

del_list = list(dup.values())   

# 2차원 리스트형을 1차원 리스트형으로 변환  
'''
itertools를 이용한 방법
itertools를 이용하여 2차원 리스트를 1차원 리스트로 만들 수 있습니다. 
itertools.chain()는 인자로 전달되는 iterable의 데이터를 연결하여 리턴해 줍니다. 
명심해야하는 것은 인자 앞에 *를 붙여주어야 하는 것입니다.
'''
del_list = list(itertools.chain(*del_list))

# data_draw_korea_MC_Population_all 데이터프레임에서 중복행(del_list가 보관) 제거 
temp = []
temp_col = data_draw_korea_MC_Population_all.columns
for i in range(0, len(data_draw_korea_MC_Population_all)):
    if i not in del_list:
        temp.append(data_draw_korea_MC_Population_all.iloc[i])
        
result = pd.DataFrame(temp, columns=temp_col)        

#--------------------------------------
# 블록맵 그리기  
#--------------------------------------    
           
# (9) 블록맵에서 블록에 해당 데이터를 매핑하여 색을 표시하는 함수
            
def draw_blockMap(blockedMap, targetData, title, color ):
    whitelabelmin = (max(blockedMap[targetData]) - min(blockedMap[targetData])) * 0.25 + min(blockedMap[targetData])

    datalabel = targetData

    vmin = min(blockedMap[targetData])  #count(공공의료기관 수) 최소값 : 1
    vmax = max(blockedMap[targetData])  #count(공공의료기관 수) 최대값 : 7

    mapdata = blockedMap.pivot(index='y', columns='x', values=targetData)
    masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)
    
    '''ma.masked_where(condition, a, copy=True)[source]
        => https://numpy.org/doc/stable/reference/generated/numpy.ma.masked_where.html '''
# 히트맵 그리기 => https://rfriend.tistory.com/419
    
    plt.figure(figsize=(8, 13))
    plt.title(title)
    plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=color, edgecolor='#aaaaaa', linewidth=0.5)
    # #aaaaaaa : gray 색상 
    #plt.show()

    # 지역 이름 표시
    for idx, row in blockedMap.iterrows():
        annocolor = 'white' if row[targetData] > whitelabelmin else 'black'  #글자 색 
        
        # 광역시는 구 이름이 겹치는 경우가 많아서 시단위 이름도 같이 표시한다. (중구, 서구)
        if row['광역시도'].endswith('시') and not row['광역시도'].startswith('세종'):
            dispname = '{}\n{}'.format(row['광역시도'][:2], row['행정구역'][:-1])
            if len(row['행정구역']) <= 2:
                dispname += row['행정구역'][-1]
        else:
            dispname = row['행정구역'][:-1]  #처음부터 마지막 전까지의 문자열 

        # 서대문구, 서귀포시 같이 이름이 3자 이상인 경우에 작은 글자로 표시한다.
        if len(dispname.splitlines()[-1]) >= 3:
            fontsize, linespacing = 9.5, 1.5
        else:
            fontsize, linespacing = 11, 1.2

        plt.annotate(dispname, (row['x']+0.5, row['y']+0.5), weight='bold',
                     fontsize=fontsize, ha='center', va='center', color=annocolor,
                     linespacing=linespacing)
        #plt.show()
    #plt.show()    
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




 # (10)함수를 호출하여 블록맵 생성하기

draw_blockMap(result, 'count', '행정구역별 공공보건의료기관 수', 'Blues')

draw_blockMap(result, 'MC_ratio', '행정구역별 인구수 대비 공공보건의료기관 비율', 'Reds' )
























