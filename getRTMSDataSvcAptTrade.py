import aiomysql
import pymysql
import requests
import json

from pymysql import connect
from sqlalchemy.testing import rowset

__LICENSE = "loPLOF7k/X7V+KWnnNDDm3hY85x217xn62UKczTLBNUyOpob1fi6Xk2ByPK1XATvwG14huNi4ST3DHBfoIyqfA=="

# 코드에 따라 테이블명 지정
tablesOfTrade = {
            # 서울시
            "11110": "apt_trade_jongro",
            "11140": "apt_trade_junggu",
            "11170": "apt_trade_yongsan",
            "11200": "apt_trade_seongdong",
            "11215": "apt_trade_gwangjin",
            "11230": "apt_trade_dongdaemun",
            "11260": "apt_trade_jungrang",
            "11290": "apt_trade_seongbuk",
            "11305": "apt_trade_gangbuk",
            "11320": "apt_trade_dobong",
            "11350": "apt_trade_nowon",
            "11380": "apt_trade_eunpyung",
            "11410": "apt_trade_seodaemun",
            "11440": "apt_trade_mapo",
            "11470": "apt_trade_yangcheon",
            "11500": "apt_trade_gangseo",
            "11530": "apt_trade_guro",
            "11545": "apt_trade_geumchun",
            "11560": "apt_trade_yeongdeungpo",
            "11590": "apt_trade_dongjak",
            "11620": "apt_trade_gwanak",
            "11650": "apt_trade_seocho",
            "11680": "apt_trade_gangnam",
            "11710": "apt_trade_songpa",
            "11740": "apt_trade_gangdong",
            # 성남시 분당구
            "41135": "apt_trade_bundang",
            # 용인시 수지구
            "41465": "apt_trade_suji"
        }

tablesOfRent = {
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

def getRTMSDataSvcAptTradeDev(lawdCd, dealYmd):
    print("### 조회 시작 %r" % dealYmd)
    PATH = "/getRTMSDataSvcAptTradeDev"
    API_HOST = "http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev"
    url = API_HOST + PATH
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': 'application/json'}

    pageNum = 1

    params = {
        "LAWD_CD": lawdCd,  # 성동구
        "DEAL_YMD": dealYmd,  # 2022년 01월
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

    print("### 응답 데이터 갯수 : %r" % totalCount)

    if (numOfRows < totalCount):
        if int(totalCount % numOfRows) == 0:
            loop = int(totalCount / numOfRows) - 1
        else:
            loop = int(totalCount / numOfRows)
        for i in range(loop):
            params["pageNo"] = str(i + 2)
            # print("페이지 번호 : %r" % params["pageNo"])

            response = requests.get(url, headers=headers, params=params)
            response = json.loads(response.text)
            tempData = response.get("response").get("body").get("items").get("item")

            if type(tempData) is list:
                data.extend(tempData)
            elif type(tempData) is dict:
                data.append(tempData)
    return data

def getRTMSDataSvcAptTrade(lawdCd, dealYmd):
    print("### 조회 시작 %r" % dealYmd)
    PATH = "/getRTMSDataSvcAptTrade"
    API_HOST = "http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade"
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

    print("### 응답 데이터 갯수 : %r" % totalCount)

    if(numOfRows < totalCount):
        if int(totalCount % numOfRows) == 0:
            loop = int(totalCount / numOfRows) - 1
        else:
            loop = int(totalCount / numOfRows)
        for i in range(loop):
            params["pageNo"] = str(i + 2)
            # print("페이지 번호 : %r" % params["pageNo"])

            response = requests.get(url, headers=headers, params=params)
            response = json.loads(response.text)
            tempData = response.get("response").get("body").get("items").get("item")

            if type(tempData) is list:
                data.extend(tempData)
            elif type(tempData) is dict:
                data.append(tempData)
    return data

async def insertDBAptTrade(result, lawdCd):
    print("## insertDBAptTrade 함수 진입")
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

        tableName = tablesOfTrade.get(lawdCd, "No table")

        sql = """
        INSERT IGNORE INTO """ + tableName + """ (APTDONG, APTNM, BUILDYEAR, CDEALDAY, CDEALTYPE, 
        DEALAMOUNT, DEALDAY, DEALMONTH, DEALYEAR, DEALINGGBN, EXCLUUSEAR, FLOOR, JIBUN, 
        LANDLEASEHOLDGBN, RGSTDATE, SGGCD, SLERGBN, UMDNM, 
        APTSEQ, BONBUN, BUBUN, LANDCD, ROADNM, ROADNMBONBUN, ROADNMBUBUN, ROADNMCD, ROADNMSEQ, ROADNMSGGCD, UMDCD)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # json > tuple 변환
        dataTuples = [
            (
                item.get('aptDong', ''),
                item.get('aptNm', ''),
                item.get('buildYear', ''),
                item.get('cdealDay', ''),
                item.get('cdealType', ''),
                item.get('dealAmount', ''),
                item.get('dealDay', ''),
                item.get('dealMonth', ''),
                item.get('dealYear', ''),
                item.get('dealingGbn', ''),
                item.get('excluUseAr', ''),
                item.get('floor', ''),
                item.get('jibun', ''),
                item.get('landLeaseholdGbn', ''),
                item.get('rgstDate', ''),
                item.get('sggCd', ''),
                item.get('slerGbn', ''),
                item.get('umdNm', ''),
                item.get('aptSeq', ''),
                item.get('bonbun', ''),
                item.get('bubun', ''),
                item.get('landCd', ''),
                item.get('roadNm', ''),  # roadNm 없으면 공백
                item.get('roadNmBonbun', ''),
                item.get('roadNmBubun', ''),
                item.get('roadNmCd', ''),
                item.get('roadNmSeq', ''),
                item.get('roadNmSggCd', ''),
                item.get('umdCd', '')
            )
            for item in result
        ]

        print("## dataTuples", dataTuples, len(dataTuples))
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



async def getComparisonDBAptTrade(lawdCd, lastMonth):
    print("### getComparisonDBAptTrade 함수 진입")

    conn = None
    try:
        # MYSQL DB 연결
        conn = await aiomysql.connect(
            host='localhost',
            user='root',
            password='gd16741',
            db='realEstateTrade'
        )

        tableName = tablesOfTrade.get(lawdCd, "No table")

        year = lastMonth[:4]
        month = lastMonth[4:6]

        sql = """
        SELECT t1.id, t2.id AS id2, t1.APTNM, t2.APTNM AS APTNM2, t1.EXCLUUSEAR, t2.EXCLUUSEAR AS EXCLUUSEAR2, 
        t1.UMDNM, t2.UMDNM AS UMDNM2, t1.JIBUN, t2.JIBUN AS JIBUN2, t1.DEALAMOUNT, t2.DEALAMOUNT AS DEALAMOUNT2, 
        ABS(CAST(REPLACE(t1.DEALAMOUNT,',','') AS SIGNED) - CAST(REPLACE(t2.DEALAMOUNT,',','') AS SIGNED)) AS DIFF, 
        t1.DEALYEAR, t1.DEALMONTH, t2.DEALYEAR AS DEALYEAR2, t2.DEALMONTH AS DEALMONTH2
        FROM """ + tableName + """ t1
        JOIN """ + tableName + """ t2 ON t1.APTNM = t2.APTNM AND t1.EXCLUUSEAR = t2.EXCLUUSEAR AND t1.UMDNM = t2.UMDNM AND t1.JIBUN = t2.JIBUN
        WHERE t1.id != t2.id
        AND ((t1.DEALYEAR = 2022 AND t1.DEALMONTH >= 10)
        OR (t1.DEALYEAR = 2023 AND t1.DEALMONTH <= 3))
        AND t2.DEALYEAR = """ + year + """
        AND t2.DEALMONTH = """ + month + """
        AND ABS(CAST(REPLACE(t1.DEALAMOUNT,',','') AS SIGNED) - CAST(REPLACE(t2.DEALAMOUNT,',','') AS SIGNED)) <= 10000
        """

        print("### QUERY : ", sql)

        # Connection 으로부터 Cursor 생성
        async with conn.cursor() as cursor:
            await cursor.execute(sql)
            rows = await cursor.fetchall()

            for row in rows:
                print(row)

        print("### DB 조회 성공")

        return rows
    except pymysql.MySQLError as err:
        print(f"ERROR: {err}")
    finally:
        if not conn.closed:
            conn.close()

async def getDiffOfTradeRent(lawdCd, lastMonth):
    print("### getDiffOfTradeRent 함수 진입")
    conn = None
    try:
        # MYSQL DB 연결
        conn = await aiomysql.connect(
            host='localhost',
            user='root',
            password='gd16741',
            db='realEstateTrade'
        )

        tableNameOfTrade = tablesOfTrade.get(lawdCd, "No table")
        tableNameOfRent = tablesOfRent.get(lawdCd, "No table")

        year = lastMonth[:4]
        month = lastMonth[4:6]

        sql = """
            SELECT t1.id, t2.id AS id2,t1.APTNM, t1.EXCLUUSEAR, t2.EXCLUUSEAR, t1.DEALAMOUNT, t2.DEPOSIT, t2.MONTHLYRENT, 
            ABS(CAST(REPLACE(t1.DEALAMOUNT,',','') AS SIGNED) - CAST(REPLACE(t2.DEPOSIT,',','') AS SIGNED)) AS DIFF
            FROM """ + tableNameOfTrade + """ t1, """ + tableNameOfRent + """ t2
            WHERE (t1.APTNM = t2.APTNM AND t1.EXCLUUSEAR = t2.EXCLUUSEAR AND t1.UMDNM = t2.UMDNM AND t1.JIBUN = t2.JIBUN)
            AND t1.DEALYEAR=""" + year + """ AND t1.DEALMONTH= """ + month + """
            AND t2.DEALYEAR=""" + year + """ AND t2.DEALMONTH= """ + month + """
            AND (t1.DEALAMOUNT - t2.DEPOSIT) <= 25000 AND t2.MONTHLYRENT=0
            """

        print("### QUERY : ", sql)

        # Connection 으로부터 Cursor 생성
        async with conn.cursor() as cursor:
            await cursor.execute(sql)
            rows = await cursor.fetchall()

            for row in rows:
                print(row)

        print("### DB 조회 성공")

        return rows
    except pymysql.MySQLError as err:
        print(f"ERROR: {err}")
    finally:
        if not conn.closed:
            conn.close()