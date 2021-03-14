import requests
import time
from .manga import Manga
from .chapter import Chapter
from .group import Group
from .user import User, UserSettings, UserFollow, UserUpdate


class APIError(Exception):
    pass


class LoginError(Exception):
    pass


class MangaDex:
    """Represents the MangaDex API Client."""
    def __init__(self):
        self.url = "https://mangadex.org"
        self.api = "https://api.mangadex.org/v2"
        self.session = requests.Session()
        self.login_success = False

    def login(self, username: str, password: str):
        """Logs in to MangaDex using an username and a password."""
        url = f"{self.url}/ajax/actions.ajax.php?function=login"
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
            raise LoginError("Invalid credentials.")
        else:
            self.login_success = True
            return True

    def logout(self):
        """Resets the current session."""
        self.session = requests.Session()
        self.login_success = False

    def get_manga(self, id_: int, full=False) -> Manga:
        """Gets a manga with a specific id. Set full to True to populate Manga.chapters and Manga.groups"""
        p = None
        if full:
            p = {"include": "chapters"}
        req = self.session.get(f"{self.api}/manga/{id_}", params=p)

        if req.status_code == 200:
            json = req.json()["data"]
            if full:
                return Manga(json["manga"], self.session, json["chapters"], json["groups"])
            else:
                return Manga(json, self.session)
        else:
            self.raise_err(req)

    def get_chapter(self, id_: int, low_quality=False, mark_read=False) -> Chapter:
        """Gets a chapter with a specific id."""
        p = {"saver": low_quality, "mark_read": mark_read}
        req = self.session.get(f"{self.api}/chapter/{id_}", params=p)

        if req.status_code == 200:
            return Chapter(req.json()["data"], self.session)
        else:
            self.raise_err(req)

    def get_group(self, id_: int, full=False) -> Group:
        """Gets a group with a specific id. Set full to True to populate Group.chapters_uploaded and Group.collabs."""
        p = None
        if full:
            p = {"include": "chapters"}
        req = self.session.get(f"{self.api}/group/{id_}", params=p)

        if req.status_code == 200:
            json = req.json()["data"]
            if full:
                return Group(json["group"], json["chapters"], json["groups"])
            else:
                return Group(json)
        else:
            self.raise_err(req)

    def get_user(self, id_: int = 0, full=False) -> User:
        """Gets an user with a specific id. Set full to True to populate User.chapters_uploaded and User.groups."""
        p = None
        if full:
            p = {"include": "chapters"}
        if id_ == 0 and self.login_success:
            id_ = "me"
        req = self.session.get(f"{self.api}/user/{id_}", params=p)

        if req.status_code == 200:
            json = req.json()["data"]
            if full:
                return User(json["user"], json["chapters"], json["groups"])
            else:
                return User(json)
        else:
            self.raise_err(req)

    def get_user_settings(self, id_: int = 0) -> UserSettings:
        """Gets an user's settings. To retrieve another user's settings than the one currently logged in, you must
        be a MangaDex staff member."""
        if id_ == 0 and self.login_success:
            id_ = "me"
        req = self.session.get(f"{self.api}/user/{id_}/settings")

        if req.status_code == 200:
            json = req.json()["data"]
            return UserSettings(json)
        else:
            self.raise_err(req)

    def get_user_list(self, id_: int = 0, follow_type: int = 0, hentai_mode: int = 1) -> []:
        """Gets an user's manga list. This settings follows the privacy mode of user's MDList."""
        p = {"hentai": hentai_mode}
        if follow_type != 0:
            p["type"] = follow_type
        if id_ == 0 and self.login_success:
            id_ = "me"
        req = self.session.get(f"{self.api}/user/{id_}/followed-manga", params=p)

        if req.status_code == 200:
            json = req.json()["data"]
            if json:
                return [UserFollow(x) for x in json]
        else:
            self.raise_err(req)

    def get_user_updates(self, id_: int = 0, follow_type: int = 0, hentai_mode: int = 1, delayed=False,
                         include_blocked=False) -> []:
        """Gets an user's manga feed. To retrieve another user's feed than the one currently logged in, you must be a
        MangaDex staff member."""
        p = {"type": follow_type, "hentai": hentai_mode, "delayed": delayed, "blockgroups": include_blocked}
        if id_ == 0 and self.login_success:
            id_ = "me"
        req = self.session.get(f"{self.api}/user/{id_}/followed-updates", params=p)

        if req.status_code == 200:
            json = req.json()["data"]["chapters"]
            if json:
                return [UserUpdate(x) for x in json]
        else:
            self.raise_err(req)

    def get_user_ratings(self, id_: int = 0) -> {}:
        """Gets an user's ratings."""
        if id_ == 0 and self.login_success:
            id_ = "me"
        req = self.session.get(f"{self.api}/user/{id_}/ratings")

        if req.status_code == 200:
            json = req.json()["data"]
            if json:
                return {x["mangaId"]: x["rating"] for x in json}
        else:
            self.raise_err(req)

    def get_user_manga(self, id_: int, uid: int = 0) -> UserFollow:
        """Gets an user's manga from their MDList."""
        if uid == 0 and self.login_success:
            uid = "me"
        req = self.session.get(f"{self.api}/user/{uid}/manga/{id_}")

        if req.status_code == 200:
            json = req.json()["data"]
            return UserFollow(json)
        else:
            self.raise_err(req)

    def set_user_markers(self, mangas: list, read: bool, id_: int = 0):
        """Sets chapters as read or unread."""
        reqs = []
        lists = [mangas[x:x + 100] for x in range(0, len(mangas), 100)]
        if id_ == 0 and self.login_success:
            id_ = "me"

        for y in lists:
            p = {"chapters": y, "read": read}
            reqs.append(self.session.post(f"{self.api}/user/{id_}/marker", json=p))
            time.sleep(1)

        if reqs[-1].status_code == 200:
            return True
        else:
            self.raise_err(reqs[-1])

    def raise_err(self, req):
        print("There was an error while handling this API Request. Please make sure that you're logged in"
              " if you're trying to access personal data. Refer to the docs for more information.")
        raise APIError(f"API Request Error. Status={req.status_code} LoggedIn={self.login_success}")
