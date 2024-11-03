from getRTMSDataSvcAptTradeDev import getRTMSDataSvcAptTradeDev
from getRTMSDataSvcAptTrade import getRTMSDataSvcAptTrade, insertDBAptTrade
from getRTMSDataSvcAptRent import getRTMSDataSvcAptRent
import asyncio

# import getRTMSDataSvcAptTradeDev

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("main method")


#### 실행방법 ####
# 1. source myenv/bin/activate
# ㄴ가상환경 실행
# 2. mysql -u root -p
# ㄴ데이터베이스 서버 구동
# 3. use realEstateTrade;
# ㄴ데이터베이스 연결
# 4. python3 dbUtils.py
# ㄴ실행하려는 PYTHON 파일 실행
