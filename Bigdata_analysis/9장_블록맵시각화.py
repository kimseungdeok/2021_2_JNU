
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
        # 서울 중구, 대구 중구 등 
        if row['광역시도'].endswith('시') and not row['광역시도'].startswith('세종'):
            dispname = '{}\n{}'.format(row['광역시도'][:2], row['행정구역'][:-1])
            if len(row['행정구역']) <= 2:
                dispname += row['행정구역'][-1]
        else:
            dispname = row['행정구역'][:-1]  #처음부터 마지막 전까지의 문자열 : '강릉시' => '강릉' 

        # 서대문구, 서귀포시 같이 이름이 3자 이상인 경우에 작은 글자로 표시한다.
        #'서울\n서대문'.splitlines()[-1] => '서대문'
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
    plt.axis('off') #x축. y축 삭제 
    
    cb = plt.colorbar(shrink=.1, aspect=10)  #colorbar 생성 
    cb.set_label(datalabel)

    plt.tight_layout()
    
    plt.savefig('d:/bd/ch9/blockMap_' + targetData + '.png')
                      
    
    plt.show()      




 # (10)함수를 호출하여 블록맵 생성하기

draw_blockMap(data_draw_korea_MC_Population_all, 'count', '행정구역별 공공보건의료기관 수', 'Blues')

draw_blockMap(data_draw_korea_MC_Population_all, 'MC_ratio', '행정구역별 인구수 대비 공공보건의료기관 비율', 'Reds' )
























