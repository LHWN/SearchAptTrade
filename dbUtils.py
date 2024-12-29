from dateutil.relativedelta import relativedelta
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from datetime import datetime

from sqlalchemy.sql.functions import current_date
from starlette.staticfiles import StaticFiles
from typing_extensions import dataclass_transform

from getRTMSDataSvcAptRent import getRTMSDataSvcAptRent, insertDBAptRent
from getRTMSDataSvcAptTrade import getRTMSDataSvcAptTrade, insertDBAptTrade, getComparisonDBAptTrade, \
    getDiffOfTradeRent, getRTMSDataSvcAptTradeDev

app = FastAPI()
now = datetime.now()
DATABASE_URL = "mysql+pymysql://root:gd16741@localhost:3306/realEstateTrade"
engine = create_engine(DATABASE_URL)
templates = Jinja2Templates(directory="templates")
app.mount("/css", StaticFiles(directory="templates/css"), name="css")
app.mount("/img", StaticFiles(directory="templates/img"), name="img")
app.mount("/vendor", StaticFiles(directory="templates/vendor"), name="vendor")
app.mount("/js", StaticFiles(directory="templates/js"), name="js")


class SearchParam(BaseModel):
    comparedYear: str
    comparedMonth: str

class InsertParam(BaseModel):
    lawdCd: str



@app.get("/", response_class=HTMLResponse)
async def get_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/getComparedData")
async def getComparedData(param: SearchParam):
    print("getComparedData 함수 진입")
    print("param", param.comparedYear + param.comparedMonth)
    print("현재", now.month-1)

    currentYear = now.year
    currentMonth = (str(now.month-1)).lstrip('0')
    query = """SELECT t1.id, t2.id AS id2, t1.APTNM, t2.APTNM AS APTNM2, t1.EXCLUUSEAR, t2.EXCLUUSEAR AS EXCLUUSEAR2, t1.UMDNM, t2.UMDNM AS UMDNM2, t1.JIBUN, t2.JIBUN AS JIBUN2, 
                    t1.DEALAMOUNT, t2.DEALAMOUNT AS DEALAMOUNT2, 
                    ABS(CAST(REPLACE(t1.DEALAMOUNT,',','') AS SIGNED) - CAST(REPLACE(t2.DEALAMOUNT,',','') AS SIGNED)) AS DIFF, 
                    t1.DEALYEAR, t1.DEALMONTH, t2.DEALYEAR AS DEALYEAR2, t2.DEALMONTH AS DEALMONTH2
                    FROM apt_trade t1
                    JOIN apt_trade t2 ON t1.APTNM = t2.APTNM AND t1.EXCLUUSEAR = t2.EXCLUUSEAR AND t1.UMDNM = t2.UMDNM AND t1.JIBUN = t2.JIBUN
                    WHERE t1.id != t2.id
                    AND ((t1.DEALYEAR = 2022 AND t1.DEALMONTH >= 10)
                    OR (t1.DEALYEAR = 2023 AND t1.DEALMONTH <= 3))
                    AND t2.DEALYEAR = 2024
                    AND t2.DEALMONTH = 9
                    AND ABS(CAST(REPLACE(t1.DEALAMOUNT,',','') AS SIGNED) - CAST(REPLACE(t2.DEALAMOUNT,',','') AS SIGNED)) <= 10000;"""

    try:
        print("query 실행 : {query}")
        with engine.connect() as connection:
            result = connection.execute(text(query))
            data = result.fetchall()
            columns = result.keys()
            result = [dict(zip(columns, row)) for row in data]
            print(result)
        return result
    except SQLAlchemyError as e:
        print("Database Error:", str(e))
    except Exception as e:
        print("Error:", str(e))
        return None

@app.post("/insertDealAmount")
async def insertDealAmount(param: InsertParam):
    print("### insertDealAmount 함수 진입")
    lawdCd = param.lawdCd

    # 202210 202211 202212
    # 202301 202302 202303

    data = list()

    initialYear = 202210
    for i in range(3):
        print(initialYear, "년도 조회")
        tempData = getRTMSDataSvcAptTradeDev(lawdCd, initialYear)
        data.extend(tempData)
        initialYear += 1

    initialYear = 202301
    for i in range(3):
        print(initialYear, "년도 조회")
        tempData = getRTMSDataSvcAptTradeDev(lawdCd, initialYear)
        data.extend(tempData)
        initialYear += 1

    print("최종 data", data)
    await insertDBAptTrade(data, lawdCd)

@app.post("/insertCurrentDealAmount")
async def insertCurrentDealAmount(param: InsertParam):
    print("### insertCurrentDealAmount 함수 진입")
    lawdCd = param.lawdCd

    data = list()
    now = datetime.now()
    lastMonth = now - relativedelta(months=1)
    lastMonth = lastMonth.strftime("%Y%m")
    data = getRTMSDataSvcAptTradeDev(lawdCd, lastMonth)

    print("### 현재 데이터 조회", data)
    await insertDBAptTrade(data, lawdCd)

@app.post("/insertCurrentRentAmount")
async def insertCurrentRentAmount(param: InsertParam):
    print("### insertCurrentReantAmount 함수 진입")
    lawdCd = param.lawdCd

    data = list()
    now = datetime.now()
    lastMonth = now - relativedelta(months=1)
    lastMonth = lastMonth.strftime("%Y%m")
    data = getRTMSDataSvcAptRent(lawdCd, lastMonth)

    print("### 데이터 조회", data)
    await insertDBAptRent(data, lawdCd)

@app.post("/searchComparisonDealAmount")
async def searchComparisonDealAmount(param: InsertParam):
    print("### searchComparisonDealAmount 함수 진입")
    lawdCd = param.lawdCd
    now = datetime.now()
    lastMonth = now - relativedelta(months=1)
    lastMonth = lastMonth.strftime("%Y%m")

    data = list()
    data = await getComparisonDBAptTrade(lawdCd, lastMonth)

    return data

@app.post("/searchDiffOfTradeRent")
async def searchDiffOfTradeRent(param: InsertParam):
    print("### SearchDiffOfTradeRent 함수 진입")
    lawdCd = param.lawdCd
    now = datetime.now()
    lastMonth = now - relativedelta(months=1)
    lastMonth = lastMonth.strftime("%Y%m")

    data = list()
    data = await getDiffOfTradeRent(lawdCd, lastMonth)

    return data

@app.get("/fetchData")
async def fetchData():
    query = "SELECT * FROM apt_trade"
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            data = result.fetchall()

            # 각 행을 딕셔너리 형태로 변환
            columns = result.keys() # 열 이름 가져오기
            dataDicts = [dict(zip(columns, row)) for row in data]

            if result is None:
                print("Data is None.")
            # data = [dict(row) for row in result]
            print(type(dataDicts))
            return dataDicts
    except SQLAlchemyError as e:
        print("Database Error:", str(e))
        return None
    except Exception as e:
        print("Error:", str(e))
        return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)