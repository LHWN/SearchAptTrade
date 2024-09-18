from http.client import responses
from xml.etree.ElementTree import tostring
import asyncio
import aiomysql

import pymysql
import requests
import json
import pymysql as mysql
from pymysql import connect

__LICENSE = "loPLOF7k/X7V+KWnnNDDm3hY85x217xn62UKczTLBNUyOpob1fi6Xk2ByPK1XATvwG14huNi4ST3DHBfoIyqfA=="

dbConfig = {
        'host': 'localhost',
        'user': 'root',
        'password': 'gd16741',
        'db': 'realEstateTrade'
    }

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

    response = requests.get(url, headers=headers, params=params)
    response = json.loads(response.text)

    data = response.get("response").get("body").get("items").get("item")
    numOfRows = response.get("response").get("body").get("numOfRows")
    totalCount = response.get("response").get("body").get("totalCount")

    print("### 응답 데이터 갯수 : %r" % totalCount)

    if(numOfRows < totalCount):
        if int(totalCount % numOfRows) == 0:
            loop = int(totalCount / numOfRows) - 1
        else:
            loop = int(totalCount / numOfRows)
        for i in range(loop):
            params["pageNo"] = str(i + 2)
            print("페이지 번호 : %r" % params["pageNo"])

            response = requests.get(url, headers=headers, params=params)
            response = json.loads(response.text)
            tempData = response.get("response").get("body").get("items").get("item")

            data.extend(tempData)

    return data

# "INSERT INTO table_test(name, region) VALUES (%s,%s)"

async def insertDBAptTrade(result):
    conn = None
    try:
        # MYSQL DB 연결
        conn = await aiomysql.connect(
            host='localhost',\
            user='root',
            password='gd16741',
            db='realEstateTrade'
        )

        sql = """
        INSERT INTO apt_trade (APTDONG, APTNM, BUILDYEAR, CDEALDAY, CDEALTYPE, DEALAMOUNT, DEALDAY, DEALMONTH, DEALYEAR, DEALINGGBN, EXCLUUSEAR, FLOOR, JIBUN, LANDLEASEHOLDGBN, RGSTDATE, SGGCD, SLERGBN, UMDNM)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # json > tuple 변환
        dataTuples = [(item['aptDong'], item['aptNm'], item['buildYear'], item['cdealDay'], item['cdealType'], item['dealAmount'], item['dealDay'], item['dealMonth'], item['dealYear'], item['dealingGbn'], item['excluUseAr'], item['floor'], item['jibun'], item['landLeaseholdGbn'], item['rgstDate'], item['sggCd'], item['slerGbn'], item['umdNm']) for item in result]

        # Connection 으로부터 Cursor 생성
        async with conn.cursor() as cursor:
            # executemany 사용하여 데이터 삽입
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
