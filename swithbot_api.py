import json
import time
import hashlib
import hmac
import base64
import uuid
import os
import requests
import datetime
from dotenv import load_dotenv


class Operate_Switchbot:
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
        # open token
        self.token = os.environ.get('CLIENT_TOKEN')
        # secret key
        self.secret = os.environ.get('SECRET_TOKEN')
        self.base_url = "https://api.switch-bot.com/v1.1/"

    def set_header(self):
        nonce = uuid.uuid4()
        t = int(round(time.time() * 1000))
        string_to_sign = '{}{}{}'.format(self.token, t, nonce)
        string_to_sign = bytes(string_to_sign, 'utf-8')
        secret = bytes(self.secret, 'utf-8')
        sign = base64.b64encode(
            hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
        self.apiHeader = {}
        self.apiHeader["Authorization"] = self.token
        self.apiHeader["Content-Type"] = "application/json"
        self.apiHeader["charset"] = "utf8"
        self.apiHeader["t"] = str(t)
        self.apiHeader["sign"] = str(sign, "utf-8")
        self.apiHeader["nonce"] = str(nonce)

    def get_devices(self):
        self.set_header()
        url = self.base_url + "devices"
        response = requests.get(url, headers=self.apiHeader)
        devices = response.json()
        response_file = f"device_json/devices.json"
        with open(response_file, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=2, ensure_ascii=False)
        print(f"Get devices: {devices}")

    def get_hub2(self):
        self.set_header()
        devices_json = json.load(
            open("device_json/devices.json"))["body"]["deviceList"]
        device_id = [device["deviceId"]
                     for device in devices_json if device["deviceName"] == "ハブ２ "][0]
        url = self.base_url + f"devices/{device_id}/status"
        response = requests.get(url, headers=self.apiHeader)
        print(response.json())
        temp = response.json()["body"]["temperature"]
        humidity = response.json()["body"]["humidity"]
        print(f"Get temp: {temp}, humidity: {humidity}")

    def operate_air_conditioner(self, temp: int, mode: int, air_flow: int, power: int):
        """
        modes include 0/1 (auto), 2 (cool), 3 (dry), 4 (fan), 5 (heat);
        fan speed includes 1 (auto), 2 (low), 3 (medium), 4 (high);
        power state includes on and off
        """
        def _turnon(self):
            self.set_header()
            devices_json = json.load(
                open("device_json/devices.json"))["body"]["infraredRemoteList"]
            device_id = [device["deviceId"]
                         for device in devices_json if device["deviceName"] == f"エアコン"][0]
            url = self.base_url + f"devices/{device_id}/commands"
            payload = {
                "command": "turnOn",
                "commandType": "command",
                "parameter": "",
            }
            response = requests.post(
                url, headers=self.apiHeader, data=json.dumps(payload))
            print(response.json())
        def _trunoff(self):
            self.set_header()
            devices_json = json.load(
                open("device_json/devices.json"))["body"]["infraredRemoteList"]
            device_id = [device["deviceId"]
                         for device in devices_json if device["deviceName"] == f"エアコン"][0]
            url = self.base_url + f"devices/{device_id}/commands"
            payload = {
                "command": "turnOff",
                "commandType": "command",
                "parameter": "",
            }
            response = requests.post(
                url, headers=self.apiHeader, data=json.dumps(payload))
            print(response.json())
        if power == "on":
            _turnon(self)
        elif power == "off":
            _trunoff(self)
        self.set_header()
        devices_json = json.load(
            open("device_json/devices.json"))["body"]["infraredRemoteList"]
        device_id = [device["deviceId"]
                     for device in devices_json if device["deviceName"] == f"エアコン"][0]
        url = self.base_url + f"devices/{device_id}/commands"
        parameter = f"{temp},{mode},{air_flow},{power}"
        payload = {
            "command": "setAll",
            "commandType": "command",
            "parameter": f"{parameter}",
        }
        response = requests.post(
            url, headers=self.apiHeader, data=json.dumps(payload))
        print(response.json())


if __name__ == "__main__":
    temp = 23
    air_flow = 1
    mode = 5
    power = "off"
    get_api = Operate_Switchbot()
    get_api.operate_air_conditioner(temp, mode, air_flow, power)
