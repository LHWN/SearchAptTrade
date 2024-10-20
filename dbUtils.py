import asyncio

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text, column
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from datetime import datetime

from getRTMSDataSvcAptTrade import getRTMSDataSvcAptTrade, insertDBAptTrade

app = FastAPI()
now = datetime.now()
DATABASE_URL = "mysql+pymysql://root:gd16741@localhost:3306/realEstateTrade"
engine = create_engine(DATABASE_URL)
templates = Jinja2Templates(directory="templates")

class SearchParam(BaseModel):
    comparedYear: str
    comparedMonth: str

class InsertParam(BaseModel):
    lawdCd: str

@app.get("/", response_class=HTMLResponse)
async def get_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/getDistinctData")
async def getDistincData():
    print("getDistincData 함수 진입")
    query = "SELECT DISTINCT APTNM, EXCLUUSEAR, UMDNM, JIBUN FROM apt_trade"
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            data = result.fetchall()
            columns = result.keys()
            result = [dict(zip(columns, row)) for row in data]
            print(result)
        return result
    except SQLAlchemyError as e:
        print("Database Error:", str(e))
        return None
    except Exception as e:
        print("Error:", str(e))
        return None

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
    print("insertDealAmount 함수 진입")
    lawdCd = param.lawdCd

    # 202210 202211 202212
    # 202301 202302 202303

    initialYear = 202210
    data = list()

    for i in range(3):
        tempData = getRTMSDataSvcAptTrade(lawdCd, initialYear)
        data.extend(tempData)
        initialYear += 1

    initialYear = 202301
    for i in range(3):
        tempData = getRTMSDataSvcAptTrade(lawdCd, initialYear)
        data.extend(tempData)
        initialYear += 1

    print("최종 data", data)
    print(type(data))
    await insertDBAptTrade(data, lawdCd)

@app.get("/fetchData")
async def fetchData():
    print("fetchData()")
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