import requests
from .manga import Manga


class MangaDex:
    def __init__(self):
        self.url = "https://mangadex.org"
        self.api = "https://api.mangadex.org/v2"
        self.session = requests.Session()
        self.user = None
        self.login_success = False

    def login(self, username: str, password: str):
        url = "{}/ajax/actions.ajax.php?function=login".format(self.url)
        credentials = {"login_username": username, "login_password": password}
        headers = {
            "method": "POST",
            "path": "/ajax/actions.ajax.php?function=login",
            "scheme": "https",
            "Accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": self.url,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
        }

        post = self.session.post(url, data=credentials, headers=headers)
        if not post.cookies.get("mangadex_session"):
            print("Invalid MangaDex credentials. Some API calls will be unavailable.")
            return False
        else:
            self.login_success = True
            return True

    def get_manga(self, id_: int, full=False) -> Manga:
        p = None
        if full:
            p = {"include": "chapters"}
        req = self.session.get("{}/manga/{}".format(self.api, id_), params=p)

        if req.status_code == 200:
            json = req.json()["data"]
            if full:
                return Manga(json["manga"], self.session, json["chapters"], json["groups"])
            else:
                return Manga(json, self.session)