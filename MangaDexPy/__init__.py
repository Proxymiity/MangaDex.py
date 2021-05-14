import requests
import time
import json
from .manga import Manga, MangaTag
from .chapter import Chapter
from .group import Group
from .user import User, UserSettings, UserFollow, UserUpdate
from .partial import PartialChapter, PartialGroup, PartialUser
from .network import NetworkChapter


class APIError(Exception):
    def __init__(self, r):
        self.status = r.status_code
        self.data = None
        try:
            self.data = r.json()
        except Exception as e:
            print(e)


class NoContentError(APIError):
    pass


class LoginError(APIError):
    pass


class NotLoggedInError(Exception):
    pass


class NoResultsError(Exception):
    pass


class MangaDex:
    """Represents the MangaDex API Client."""
    def __init__(self):
        self.api = "https://api.mangadex.org"
        self.net_api = "https://api.mangadex.network"
        self.session = requests.Session()
        self.session.headers["Authorization"] = ""
        self.login_success = False
        self.session_token = None
        self.refresh_token = None

    def login(self, username: str, password: str):
        """Logs in to MangaDex using an username and a password."""
        url = f"{self.api}/auth/login"
        credentials = {"username": username, "password": password}
        post = self.session.post(url, data=json.dumps(credentials))
        return self._store_token(post)

    def logout(self):
        """Resets the current session."""
        self.__init__()

    def refresh(self, token=None):
        """Refreshes the session using the refresh token."""
        if not self.login_success:
            raise NotLoggedInError
        token = token or self.refresh_token
        url = f"{self.api}/auth/refresh"
        data = {"token": token}
        post = self.session.post(url, data=json.dumps(data))
        return self._store_token(post)

    def _store_token(self, post):
        if post.status_code == 401:
            raise LoginError(post)
        elif not post.status_code == 200:
            raise APIError(post)
        else:
            resp = post.json()
            self.login_success = True
            self.session_token = resp["token"]["session"]
            self.refresh_token = resp["token"]["refresh"]
            self.session.headers["Authorization"] = resp["token"]["session"]
            return True

    def get_manga(self, id_: str,) -> Manga:
        """Gets a manga with a specific uuid."""
        req = self.session.get(f"{self.api}/manga/{id_}")
        if req.status_code == 200:
            resp = req.json()
            return Manga(resp["data"], resp["relationships"], self)
        elif req.status_code == 204:
            raise NoContentError(req)
        else:
            raise APIError(req)

    def get_chapter(self, id_: str) -> Chapter:
        """Gets a chapter with a specific id."""
        req = self.session.get(f"{self.api}/chapter/{id_}")
        if req.status_code == 200:
            resp = req.json()
            return Chapter(resp["data"], resp["relationships"], self)
        elif req.status_code == 204:
            pass
        else:
            raise APIError(req)

    def get_chapters(self, ids: list) -> []:
        """Gets chapters with specific uuids."""
        chapters = []
        sub = [ids[x:x+100] for x in range(0, len(ids), 100)]
        for s in sub:
            p = {"ids[]": s}
            req = self.session.get(f"{self.api}/chapter", params=p)
            if req.status_code == 200:
                resp = req.json()
                chapters += [x for x in resp["results"]]
            elif req.status_code == 204:
                pass
            else:
                raise APIError(req)
        if not sub or not chapters:
            raise NoResultsError()
        return [Chapter(x["data"], x["relationships"], self) for x in chapters]

    def get_manga_chapters(self, mg: Manga) -> []:
        """Gets chapters associated with a specific Manga."""
        chapters = []
        offset = 0
        resp = None
        remaining = True
        while remaining:
            p = {"limit": 500, "offset": offset}
            req = self.session.get(f"{self.api}/manga/{mg.id}/feed", params=p)
            if req.status_code == 200:
                resp = req.json()
                chapters += [x for x in resp["results"]]
            elif req.status_code == 204:
                pass
            else:
                raise APIError(req)
            if resp is not None:
                remaining = resp["total"] > offset + 500
                offset += 500
            else:
                remaining = False
        if not chapters:
            raise NoResultsError()
        return [Chapter(x["data"], x["relationships"], self) for x in chapters]

    def read_chapter(self, ch: Chapter, force_443: bool = False) -> NetworkChapter:
        """Pulls a chapter from the MD@H Network."""
        data = {"forcePort443": force_443}
        req = self.session.get(f"{self.api}/at-home/server/{ch.id}", params=data)
        if req.status_code == 200:
            resp = req.json()
            return NetworkChapter(ch, resp["baseUrl"], self)
        else:
            raise APIError(req)

    def network_report(self, url, success, cache_header, req_bytes, req_duration) -> bool:
        """Reports statistics back to the MD@H Network."""
        data = {"url": url, "success": success, "cached": cache_header, "bytes": req_bytes, "duration": req_duration}
        req = self.session.post(f"{self.net_api}/report", data=json.dumps(data))
        if req.status_code == 200:
            return True
        else:
            raise APIError(req)

    def get_group(self, id_: str) -> Group:
        """Gets a group with a specific id."""
        req = self.session.get(f"{self.api}/group/{id_}")
        if req.status_code == 200:
            resp = req.json()
            return Group(resp["data"], self)
        elif req.status_code == 204:
            pass
        else:
            raise APIError(req)

    def get_user(self, id_: str = "me") -> User:
        """Gets an user with a specific id."""
        if id_ == "me" and not self.login_success:
            raise NotLoggedInError
        req = self.session.get(f"{self.api}/user/{id_}")
        if req.status_code == 200:
            resp = req.json()
            return User(resp["data"], self)
        elif req.status_code == 204:
            pass
        else:
            raise APIError(req)

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
            raise APIError(req)

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
            raise APIError(req)

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
            raise APIError(req)

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
            raise APIError(req)

    def get_user_manga(self, id_: int, uid: int = 0) -> UserFollow:
        """Gets an user's manga from their MDList."""
        if uid == 0 and self.login_success:
            uid = "me"
        req = self.session.get(f"{self.api}/user/{uid}/manga/{id_}")

        if req.status_code == 200:
            json = req.json()["data"]
            return UserFollow(json)
        else:
            raise APIError(req)

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
            raise APIError(reqs[-1])
