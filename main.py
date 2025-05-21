import requests
from dotenv import load_dotenv
import os


BASE_URL = "https://www.pythonanywhere.com"
LOGIN_URL = f"{BASE_URL}/login/"
API_RELOAD_URL = f"{BASE_URL}/api/v0/user/manuelseromenho/webapps/manuelseromenho.pythonanywhere.com/reload/"
EXTEND_URL = "https://www.pythonanywhere.com/user/manuelseromenho/webapps/manuelseromenho.pythonanywhere.com/extend"
WEB_APP_TAP_TYPE = "%23tab_id_manuelseromenho_pythonanywhere_com"

load_dotenv()


class PythonAnywhereTool:
    def __init__(self):
        self.client = requests.Session()
        self.session_id = ""
        self.csrftoken = ""

    def login(self) -> None:
        self.client.get(LOGIN_URL)
        if "csrftoken" in self.client.cookies:
            self.csrftoken = self.client.cookies["csrftoken"]
        else:
            # older versions
            self.csrftoken = self.client.cookies["csrf"]

        login_data = {
            "auth-username": os.getenv("AUTH_USERNAME"),
            "auth-password": os.getenv("AUTH_PASSWORD"),
            "csrfmiddlewaretoken": self.csrftoken,
            "login_view-current_step": "auth",
        }
        self.client.post(LOGIN_URL, data=login_data, headers=dict(Referer=LOGIN_URL))
        self.session_id = self.client.cookies["sessionid"]

    def extend_python_anywhere(self) -> None:
        headers = {
            "Host": "www.pythonanywhere.com",
            "Referer": "https://www.pythonanywhere.com/user/manuelseromenho/webapps/",
            "X-CSRFToken": self.csrftoken,
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.pythonanywhere.com",
            "Cookie": f"web_app_tab_type={WEB_APP_TAP_TYPE};"
                      f"cookie_warning_seen=True;"
                      f"csrftoken={self.csrftoken};"
                      f"sessionid={self.session_id};",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        r = self.client.post(
            EXTEND_URL,
            data={"csrfmiddlewaretoken": self.csrftoken, "next": "/"},
            headers=headers,
        )

        print(r.status)

    @staticmethod
    def api_reload_python_anywhere(self) -> None:
        username = os.getenv("API_USERNAME")
        token = os.getenv("API_TOKEN")

        requests.post(
            API_RELOAD_URL,
            headers={"Authorization": "Token {token}".format(token=token)},
        )

python_anywhere_tool = PythonAnywhereTool()
python_anywhere_tool.login()
python_anywhere_tool.extend_python_anywhere()
