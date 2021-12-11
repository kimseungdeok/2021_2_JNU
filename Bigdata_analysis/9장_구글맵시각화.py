import pandas as pd

CB = pd.read_csv('d:/BD/ch9/CoffeeBean.csv', encoding='CP949', index_col=0, header=0, engine='python')
CB.head()  #작업 내용 확인용 출력
temp = CB
addr = []

for address in CB.address:
    addr.append(str(address).split())

#작업 내용 확인용 출력
print('데이터 개수 : %d' % len(addr)) 
addr  

addr2 = []

# addr에서 행정구역 표준 이름이 아닌것 수정하기
for i in range(len(addr)):
    if addr[i][0] == "서울": addr[i][0]="서울특별시"
    elif addr[i][0] == "서울시": addr[i][0]="서울특별시"
    elif addr[i][0] == "부산시": addr[i][0]="부산광역시"
    elif addr[i][0] == "인천": addr[i][0]="인천광역시"
    elif addr[i][0] == "광주": addr[i][0]="광주광역시"
    elif addr[i][0] == "대전시": addr[i][0]="대전광역시"
    elif addr[i][0] == "울산시": addr[i][0]="울산광역시"    
    elif addr[i][0] == "세종시": addr[i][0]="세종특별자치시"
    elif addr[i][0] == "경기": addr[i][0]="경기도"
    elif addr[i][0] == "충북": addr[i][0]="충청북도"
    elif addr[i][0] == "충남": addr[i][0]="충청남도"
    elif addr[i][0] == "전북": addr[i][0]="전라북도"
    elif addr[i][0] == "전남": addr[i][0]="전라남도"
    elif addr[i][0] == "경북": addr[i][0]="경상북도"
    elif addr[i][0] == "경남": addr[i][0]="경상남도"
    elif addr[i][0] == "제주": addr[i][0]="제주특별자치도"
    elif addr[i][0] == "제주도": addr[i][0]="제주특별자치도"
    elif addr[i][0] == "제주시": addr[i][0]="제주특별자치도"                                
       
    addr2.append(' '.join(addr[i]))  

addr2 #작업 내용 확인용 출력

addr2 = pd.DataFrame(addr2, columns=['address2'])

addr2 #작업 내용 확인용 출력
CB2 = pd.concat([CB, addr2],  axis=1 )

CB2.head()  #작업 내용 확인용 출력
CB2.to_csv('d:/BD/ch9/CoffeeBean_2.csv',encoding='CP949', index = False)
temp = CB2


!pip install folium
import folium


map_osm = folium.Map(location=[37.560284, 126.975334], zoom_start = 16) #maps.google,co.kr
map_osm.save('d:/BD/ch9/map.html')

CB_file = pd.read_csv('d:/BD/ch9/CoffeeBean_2.csv',encoding='cp949',  engine='python')

CB_file.head() #작업 내용 확인용 출력

CB_geoData = pd.read_csv('d:/BD/ch9/CB_geo.shp_2.csv',encoding='cp949',  engine='python')
#http://www.gisdeveloper.co.kr/?cat=44 에서 Geocoder-Xr  다운로드 및 설치 , 활용

len(CB_geoData) #확인용 출력

map_CB = folium.Map(location=[37.560284, 126.975334], zoom_start = 15)

for i, store in CB_geoData.iterrows():   
    folium.Marker(location=[store['위도'], store['경도']], popup= store['store'], icon=folium.Icon(color='blue', icon='star')).add_to(map_CB)



map_CB.save('d:/BD/ch9/map_CB.html')





























