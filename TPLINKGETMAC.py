import requests
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import NetworkConfig


def getMacList():
    IP1 = NetworkConfig.TPLINKIP
    ss = requests.session()
    Header = {
        "Content-Type":"application/json"
    }
    Login_Data = {
        "login":{
            "password":NetworkConfig.LOGINPASSWORD
        },
        "method":"do"
    }
    stok = ss.post(IP1,json=Login_Data).json().get("stok")
    getMacData = {
        "ip_mac_bind": {
            "table": [
                "user_bind",
                "sys_arp"
            ]
        },
        "method": "get"
    }
    MAC_URL = IP1+"/stok="+stok+"/ds"
    Mac_Data = ss.post(MAC_URL,json=getMacData).json()
    Mac_List = [mac.get("sys_arp_"+str(index+1)).get('mac') for index,mac in enumerate(Mac_Data.get("ip_mac_bind").get('sys_arp'))]
    return Mac_List