import datetime
import time
from swithbot_api import Operate_Switchbot
from loop_electricity import LoopElectricity


def control_air_conditioner(temp: int, mode: int, air_flow: int):
    loop_electricity = LoopElectricity()
    air_conditioner_flag = False
    while True:
        # 30分ごとに実行
        now_date = datetime.datetime.now()
        if now_date.minute % 30 == 0:
            percent = loop_electricity.now_percent()
            if percent > 1.2:
                print(f"{now_date.hour}:{now_date.minute} 電気代が高いのでエアコンを消します")
                swithbot = Operate_Switchbot()
                swithbot.operate_air_conditioner(temp, mode, air_flow, "off")
                air_conditioner_flag = True
            else:
                if air_conditioner_flag:
                    swithbot = Operate_Switchbot()
                    swithbot.operate_air_conditioner(
                        temp, mode, air_flow, "on")
                    air_conditioner_flag = False
                print(f"{now_date.hour}:{now_date.minute} 電気代が高くないのでエアコンを消しません")
        else:
            print(f"{now_date.hour}:{now_date.minute}")
        time.sleep(60)


if __name__ == '__main__':
    control_air_conditioner(23, 5, 1)
