import requests
import json
from typing import List, Dict, Union, Type, Literal
from .manga import Manga, MangaTag
from .chapter import Chapter
from .group import Group
from .user import User
from .author import Author
from .cover import Cover
from .network import NetworkChapter
from .search import SearchMapping


class MDException(Exception):
    pass


class APIError(MDException):
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


class NotLoggedInError(MDException):
    pass


class NoResultsError(MDException):
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

    def login(self, username: str, password: str) -> bool:
        """Logs in to MangaDex using an username and a password."""
        credentials = {"username": username, "password": password}
        post = self.session.post(f"{self.api}/auth/login", data=json.dumps(credentials))
        return self._store_token(post)

    def logout(self):
        """Resets the current session."""
        self.__init__()

    def refresh(self, token: str = None) -> bool:
        """Refreshes the session using the refresh token."""
        if not self.login_success:
            raise NotLoggedInError
        token = token or self.refresh_token
        data = {"token": token}
        post = self.session.post(f"{self.api}/auth/refresh", data=json.dumps(data))
        return self._store_token(post)

    def check(self) -> bool:
        """Checks if the stored Authorization token is still valid."""
        req = self.session.get(f"{self.api}/auth/check")
        if req.status_code == 200:
            resp = req.json()
            return resp["isAuthenticated"]
        else:
            raise APIError(req)

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

    def get_manga(self, id_: str) -> Manga:
        """Gets a manga with a specific uuid."""
        req = self.session.get(f"{self.api}/manga/{id_}")
        if req.status_code == 200:
            resp = req.json()
            return Manga(resp["data"], resp["relationships"], self)
        elif req.status_code == 404:
            raise NoContentError(req)
        else:
            raise APIError(req)

    def get_chapter(self, id_: str) -> Chapter:
        """Gets a chapter with a specific uuid."""
        req = self.session.get(f"{self.api}/chapter/{id_}")
        if req.status_code == 200:
            resp = req.json()
            return Chapter(resp["data"], resp["relationships"], self)
        elif req.status_code == 404:
            raise NoContentError(req)
        else:
            raise APIError(req)

    def get_chapters(self, ids: List[str]) -> List[Chapter]:
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

    def get_manga_chapters(self, mg: Manga, params: dict = None) -> List[Chapter]:
        """Gets chapters associated with a specific Manga."""
        params = params or {}
        if "limit" in params:
            params.pop("limit")
        if "offset" in params:
            params.pop("offset")
        return self._retrieve_pages(f"{self.api}/manga/{mg.id}/feed", Chapter, call_limit=100, params=params)

    def get_manga_covers(self, mg: Manga, params: dict = None) -> List[Cover]:
        """Gets covers associated with a specific Manga."""
        params = params or {}
        params["manga[]"] = mg.id
        return self._retrieve_pages(f"{self.api}/cover", Cover, call_limit=100, params=params)

    def get_cover(self, id_: str) -> Cover:
        """Gets a cover with a specific uuid."""
        req = self.session.get(f"{self.api}/cover/{id_}")
        if req.status_code == 200:
            resp = req.json()
            return Cover(resp["data"], resp["relationships"], self)
        elif req.status_code == 404:
            raise NoContentError(req)
        else:
            raise APIError(req)

    def read_chapter(self, ch: Chapter, force_443: bool = False) -> NetworkChapter:
        """Pulls a chapter from the MD@H Network."""
        data = {"forcePort443": force_443}
        req = self.session.get(f"{self.api}/at-home/server/{ch.id}", params=data)
        if req.status_code == 200:
            resp = req.json()
            return NetworkChapter(ch, resp["baseUrl"], self)
        else:
            raise APIError(req)

    def network_report(self, url: str, success: bool, cache_header: bool, req_bytes: int, req_duration: int) -> bool:
        """Reports statistics back to the MD@H Network."""
        data = {"url": url, "success": success, "cached": cache_header, "bytes": req_bytes, "duration": req_duration}
        req = self.session.post(f"{self.net_api}/report", data=json.dumps(data))
        if req.status_code == 200:
            return True
        else:
            raise APIError(req)

    def get_group(self, id_: str) -> Group:
        """Gets a group with a specific uuid."""
        req = self.session.get(f"{self.api}/group/{id_}")
        if req.status_code == 200:
            resp = req.json()
            return Group(resp["data"], None, self)
        elif req.status_code == 404:
            raise NoContentError(req)
        else:
            raise APIError(req)

    def get_user(self, id_: str = "me") -> User:
        """Gets an user with a specific uuid."""
        if id_ == "me" and not self.login_success:
            raise NotLoggedInError
        req = self.session.get(f"{self.api}/user/{id_}")
        if req.status_code == 200:
            resp = req.json()
            return User(resp["data"], self)
        elif req.status_code == 404:
            raise NoContentError(req)
        else:
            raise APIError(req)

    def get_user_list(self, limit: int = 100) -> List[Manga]:
        """Gets the currently logged user's manga list."""
        if not self.login_success:
            raise NotLoggedInError
        return self._retrieve_pages(f"{self.api}/user/follows/manga", Manga, limit=limit, call_limit=100)

    def get_user_updates(self, limit: int = 100, params: dict = None) -> List[Chapter]:
        """Gets the currently logged user's manga feed."""
        if not self.login_success:
            raise NotLoggedInError
        params = params or {}
        return self._retrieve_pages(f"{self.api}/user/follows/manga/feed", Chapter, call_limit=100,
                                    limit=limit, params=params)

    def get_author(self, id_: str) -> Author:
        """Gets an author with a specific uuid"""
        req = self.session.get(f"{self.api}/author/{id_}")
        if req.status_code == 200:
            resp = req.json()
            return Author(resp["data"], resp["relationships"], self)
        elif req.status_code == 404:
            raise NoContentError(req)
        else:
            raise APIError(req)

    def transform_ids(self, obj: str, content: List[int]) -> Dict:
        """Gets uuids from legacy ids."""
        data = {"type": obj, "ids": content}
        post = self.session.post(f"{self.api}/legacy/mapping", data=json.dumps(data))
        if post.status_code == 200:
            resp = post.json()
            return {x["data"]["attributes"]["legacyId"]: x["data"]["attributes"]["newId"] for x in resp}
        else:
            raise APIError(post)

    def search(self, obj: Literal["manga", "chapter", "group", "author", "cover"], params: dict,
               limit: int = 100) -> List[Union[Manga, Chapter, Group, Author, Cover]]:
        """Searches an object."""
        m = SearchMapping(obj)
        return self._retrieve_pages(f"{self.api}{m.path}", m.object, limit=limit, call_limit=100, params=params)

    def _retrieve_pages(self, url: str, obj: Type[Union[Manga, Chapter, Group, Author, Cover]],
                        limit: int = 0, call_limit: int = 500,
                        params: dict = None) -> List[Union[Manga, Chapter, Group, Author, Cover]]:
        params = params or {}
        data = []
        offset = 0
        resp = None
        remaining = True
        if "limit" in params:
            params.pop("limit")
        if "offset" in params:
            params.pop("offset")
        while remaining:
            p = {"limit": limit if limit <= call_limit and limit != 0 else call_limit, "offset": offset}
            p = {**p, **params}
            req = self.session.get(url, params=p)
            if req.status_code == 200:
                resp = req.json()
                data += [x for x in resp["results"]]
            elif req.status_code == 204:
                pass
            else:
                raise APIError(req)
            if limit and len(data) >= limit:
                break
            if resp is not None:
                remaining = resp["total"] > offset + call_limit
                offset += call_limit
            else:
                remaining = False
        if not data:
            raise NoResultsError()
        return [obj(x["data"], x["relationships"], self) for x in data]
