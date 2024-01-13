from requests import get
import json
from datetime import datetime, timedelta
import math
import time
import os


class LoopElectricity:
    def __init__(self):
        self.url = "https://looop-denki.com/api/prices?select_area=03"

    def _get_json(self):
        for i in range(10):
            response = get(self.url)
            return json.loads(response.text)
        else:
            time.sleep(1)

    def _time_move_down(self, future_minute: int = 60):
        """
        future_minute: 将来の温度をいつまで見るか
        """
        # 現在の時刻を取得
        current_time = datetime.now()

        # 現在の分数を取得
        current_minute = current_time.minute

        # 30分ごとに切り下げ
        if current_minute >= 30:
            current_time -= timedelta(minutes=(current_minute - 30))
        else:
            current_time -= timedelta(minutes=current_minute)

        # 新しい時刻をHHMM形式で表示
        new_hhmm_30 = (current_time + timedelta(minutes=30))
        # 今の時間を取得
        new_hhmm_29 = (current_time + timedelta(minutes=29))
        now_hhmm = f'{current_time.hour}:{current_time.strftime("%M")}' + \
            '~' + f'{new_hhmm_29.hour}:{new_hhmm_29.strftime("%M")}'
        future_hhmm_list = [f'{(new_hhmm_30 + timedelta(minutes=30*i)).hour}:{(new_hhmm_30 + timedelta(minutes=30*i)).strftime("%M")}' +
                            '~' +
                            f'{(new_hhmm_29 + timedelta(minutes=30*(i+1))).hour}:{(new_hhmm_29 + timedelta(minutes=30*(i+1))).strftime("%M")}' for i in range(future_minute//30)]
        return now_hhmm, future_hhmm_list

    def now_percent(self):
        """
        今日の電気料金の平均に対して、現在の電気料金が何パーセント比率かを返す
        """
        json_data = self._get_json()
        now_hhmm, _ = self._time_move_down()
        if datetime.now().hour < 3:
            today_temps = json_data['0']['price_data']
        else:
            today_temps = json_data['1']['price_data']
        # 平均を7:00~24:00のデータで計算
        today_temp_ave = sum(today_temps[14:]) / len(today_temps[14:])
        now_temp_index = [i for i, time in enumerate(
            json_data['timelist']) if time == now_hhmm]
        now_temp = json_data['1']['price_data'][now_temp_index[0]]
        percent = now_temp / today_temp_ave
        return percent


if __name__ == '__main__':
    loop_electricity = LoopElectricity()
    while True:
        # 30分ごとに実行
        now_date = datetime.now()
        percent = loop_electricity.now_percent()
        if now_date.minute % 30 == 0:
            if percent > 1.2:
                print("電気代が高いのでエアコンを消します")
                os.system("python3 swithbot_api.py")
        else:
            print(f"現在の電気代は{percent}です")
        time.sleep(60)
