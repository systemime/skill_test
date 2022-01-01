r"""
https://playwright.dev/python/docs/intro
playwright codegen https://api.weibo.com/chat\#/chat --save-storage cookie
"""

import random

from playwright.sync_api import sync_playwright

name = "用户5622719478"
talk = [
    "1",
    "1",
    "1",
    "1",
    "1",
    "1",
]
cookie = "SINAGLOBAL=4866067954353.83.1628300829094; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFxdeW_jZwEP67gSgdhSSKg5JpX5KMhUgL.Foq7e0.RS0.0SoB2dJLoI7_yUgxD9g4Xeoz0e7tt; UOR=,,www.google.com; ALF=1667011536; SSOLoginState=1635475536; SCF=AobRjmlnUEdYdfAUsy0gipPoppmDheKN0p40xvyVK1kf3Pjm4WNj3lEsptp6fm8XFKU82QK8vSX4D2eCEUgioX8.; SUB=_2A25MfxAADeRhGeBO6FsZ9yfPzTiIHXVvDQbIrDV8PUNbmtB-LULFkW9NSh2Xy3GuKo0X9A0atMgrc1dWO2bvuvQp; _s_tentry=www.google.com; Apache=7008342798347.976.1635497908356; ULV=1635497908360:3:1:1:7008342798347.976.1635497908356:1632112940882; webim_unReadCount=%7B%22time%22%3A1635498189187%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A45%2C%22msgbox%22%3A0%7D"


def format_cookie(cookie):
    cookie_list = []
    cookies = cookie.split("; ")
    for val in cookies:
        co = val.strip()
        p = co.split("=")
        value = co.replace(p[0] + "=", "").replace('"', "")
        cookie_list.append((p[0], value))

    return [
        {
            "sameSite": "Lax",
            "name": item[0],
            "value": item[1],
            "domain": ".weibo.com",
            "path": "/",
            "expires": -1,
            "httpOnly": False,
            "secure": False,
        }
        for item in cookie_list
    ]


with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    context.add_cookies(format_cookie(cookie))
    page = context.new_page()

    page.goto("https://api.weibo.com/chat#/chat")
    page.click(f"text={name}")
    for i in range(10):
        page.click("textarea")
        page.fill("textarea", "")
        page.press("textarea", "CapsLock")
        page.fill("textarea", random.choice(talk))
        page.press("textarea", "Enter")

    print(page.title())
    context.close()
    browser.close()
