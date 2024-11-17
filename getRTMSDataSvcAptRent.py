import aiomysql
import pymysql
import requests
import json
import pymysql as mysql
from pymysql import connect

__LICENSE = "loPLOF7k/X7V+KWnnNDDm3hY85x217xn62UKczTLBNUyOpob1fi6Xk2ByPK1XATvwG14huNi4ST3DHBfoIyqfA=="

# 코드에 따라 테이블명 지정
tables = {
            # 서울시
            "11110": "apt_rent_jongro",
            "11140": "apt_rent_junggu",
            "11170": "apt_rent_yongsan",
            "11200": "apt_rent_seongdong",
            "11215": "apt_rent_gwangjin",
            "11230": "apt_rent_dongdaemun",
            "11260": "apt_rent_jungrang",
            "11290": "apt_rent_seongbuk",
            "11305": "apt_rent_gangbuk",
            "11320": "apt_rent_dobong",
            "11350": "apt_rent_nowon",
            "11380": "apt_rent_eunpyung",
            "11410": "apt_rent_seodaemun",
            "11440": "apt_rent_mapo",
            "11470": "apt_rent_yangcheon",
            "11500": "apt_rent_gangseo",
            "11530": "apt_rent_guro",
            "11545": "apt_rent_geumchun",
            "11560": "apt_rent_yeongdeunpo",
            "11590": "apt_rent_dongjak",
            "11620": "apt_rent_gwanak",
            "11650": "apt_rent_seocho",
            "11680": "apt_rent_gangnam",
            "11710": "apt_rent_songpa",
            "11740": "apt_rent_gangdong",
            # 성남시 분당구
            "41135": "apt_rent_bundang",
            # 용인시 수지구
            "41465": "apt_rent_suji"
        }

def getRTMSDataSvcAptRent(lawdCd, dealYmd):
    print("### 조회 시작 %r" % dealYmd)
    PATH = "/getRTMSDataSvcAptRent"
    API_HOST = "http://apis.data.go.kr/1613000/RTMSDataSvcAptRent"
    url = API_HOST + PATH
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': 'application/json'}

    pageNum = 1

    params = {
        "LAWD_CD": lawdCd, # 성동구
        "DEAL_YMD": dealYmd, # 2022년 01월
        "serviceKey": __LICENSE,
        "pageNo": pageNum
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response = json.loads(response.text)

        data = response.get("response").get("body").get("items").get("item")
        numOfRows = response.get("response").get("body").get("numOfRows")
        totalCount = response.get("response").get("body").get("totalCount")
    except Exception as e:
        print(f"Error! : {e}")

    if(numOfRows < totalCount):
        if int(totalCount % numOfRows) == 0:
            loop = int(totalCount / numOfRows) - 1
        else:
            loop = int(totalCount / numOfRows)
        for i in range(loop):
            params["pageNo"] = str(i + 2)

            response = requests.get(url, headers=headers, params=params)
            response = json.loads(response.text)
            print(response)
            tempData = response.get("response").get("body").get("items").get("item")

            if type(tempData) is list:
                data.extend(tempData)
            elif type(tempData) is dict:
                data.append(tempData)
        return data

async def insertDBAptRent(result, lawdCd):
    print("### insertDBAptRent 함수 진입")
    print(result)

    conn = None
    try:
        # MYSQL DB 연결
        conn = await aiomysql.connect(
            host='localhost',
            user='root',
            password='gd16741',
            db='realEstateTrade'
        )

        tableName = tables.get(lawdCd, "No table")

        sql = """
        INSERT IGNORE INTO """ + tableName + """(
        APTNM, BUILDYEAR, CONTRACTTERM, CONTRACTTYPE, DEALDAY, 
        DEALMONTH, DEALYEAR, DEPOSIT, EXCLUUSEAR, FLOOR, 
        JIBUN, MONTHLYRENT, PREDEPOSIT, PREMONTHLYRENT, SGGCD, 
        UMDNM, USERRRIGHT)
        VALUES (
        %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, 
        %s, %s)"""

        # json > tuple 변환
        dataTuples = [(item['aptNm'], item['buildYear'], item['contractTerm'],
                       item['contractType'], item['dealDay'], item['dealMonth'],
                       item['dealYear'], item['deposit'], item['excluUseAr'],
                       item['floor'], item['jibun'], item['monthlyRent'],
                       item['preDeposit'], item['preMonthlyRent'], item['sggCd'],
                       item['umdNm'], item['useRRRight']) for item in result]

        print("## dataTuples", dataTuples)
        print("## query", sql)
        # Connection 으로부터 Cursor 생성
        async with conn.cursor() as cursor:
            # executemany 사용하여 데이터 삽입
            # await cursor.executemany(sql, dataTuples)
            await cursor.executemany(sql, dataTuples)
            # 커밋하여 변경사항 저장
            await conn.commit()
        print("### DB 저장 성공")
    except pymysql.MySQLError as err:
        print(f"ERROR: {err}")
    finally:
        if not conn.closed:
            # cursor.close()
            conn.close()
