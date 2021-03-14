import requests
import time
from .manga import Manga
from .chapter import Chapter
from .group import Group
from .user import User, UserSettings, UserFollow, UserUpdate, UserManga


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

    def get_chapter(self, id_: int, low_quality=False, mark_read=False) -> Chapter:
        p = {"saver": low_quality, "mark_read": mark_read}
        req = self.session.get("{}/chapter/{}".format(self.api, id_), params=p)

        if req.status_code == 200:
            return Chapter(req.json()["data"], self.session)

    def get_group(self, id_: int) -> Group:
        req = self.session.get("{}/group/{}".format(self.api, id_))

        if req.status_code == 200:
            json = req.json()["data"]
            return Group(json)

    def get_user(self, id_: int = 0) -> User:
        if id_ == 0 and self.login_success:
            id_ = "me"
        req = self.session.get("{}/user/{}".format(self.api, id_))

        if req.status_code == 200:
            json = req.json()["data"]
            return User(json)

    def get_user_settings(self, id_: int = 0) -> UserSettings:
        if id_ == 0 and self.login_success:
            id_ = "me"
        req = self.session.get("{}/user/{}/settings".format(self.api, id_))

        if req.status_code == 200:
            json = req.json()["data"]
            return UserSettings(json)

    def get_user_list(self, id_: int = 0, follow_type: int = 0, hentai_mode: int = 1) -> []:
        p = {"hentai": hentai_mode}
        if follow_type != 0:
            p["type"] = follow_type
        if id_ == 0 and self.login_success:
            id_ = "me"
        req = self.session.get("{}/user/{}/followed-manga".format(self.api, id_), params=p)

        if req.status_code == 200:
            json = req.json()["data"]
            if json:
                return [UserFollow(x) for x in json]

    def get_user_updates(self, id_: int = 0, follow_type: int = 0, hentai_mode: int = 1, delayed=False,
                         include_blocked=False) -> []:
        p = {"type": follow_type, "hentai": hentai_mode, "delayed": delayed, "blockgroups": include_blocked}
        if id_ == 0 and self.login_success:
            id_ = "me"
        req = self.session.get("{}/user/{}/followed-updates".format(self.api, id_), params=p)

        if req.status_code == 200:
            json = req.json()["data"]["chapters"]
            if json:
                return [UserUpdate(x) for x in json]

    def get_user_ratings(self, id_: int = 0) -> {}:
        if id_ == 0 and self.login_success:
            id_ = "me"
        req = self.session.get("{}/user/{}/ratings".format(self.api, id_))

        if req.status_code == 200:
            json = req.json()["data"]
            if json:
                return {x["mangaId"]: x["rating"] for x in json}

    def get_user_manga(self, id_: int, uid: int = 0) -> UserManga:
        if uid == 0 and self.login_success:
            uid = "me"
        req = self.session.get("{}/user/{}/manga/{}".format(self.api, uid, id_))

        if req.status_code == 200:
            json = req.json()["data"]
            return UserManga(json)

    def set_user_markers(self, mangas: list, read: bool, id_: int = 0):
        reqs = []
        lists = [mangas[x:x + 100] for x in range(0, len(mangas), 100)]
        if id_ == 0 and self.login_success:
            id_ = "me"

        for y in lists:
            p = {"chapters": y, "read": read}
            reqs.append(self.session.post("{}/user/{}/marker".format(self.api, id_), json=p))
            time.sleep(1)

        if reqs[-1].status_code == 200:
            return True
