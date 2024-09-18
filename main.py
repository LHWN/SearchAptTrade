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
    data = getRTMSDataSvcAptTrade(11200, 202408)  # 2022년 01월 성동구
    # data = getRTMSDataSvcAptTrade(11200, 202212)  # 2022년 02월 성동구

    loop = asyncio.get_event_loop()
    loop.run_until_complete(insertDBAptTrade(data))
    # print("최종 데이터 : %r" % data)

    # fromDate = 202201
    # for i in range(11):
    #     fromDate += i
    #     print("for 문 요청 시작 : %r" % fromDate)
    #     data = getRTMSDataSvcAptTrade(11200, fromDate)
    #
    #     # 비동기 함수 실행
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(insertDBAptTrade(data))