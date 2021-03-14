from .partial import PartialChapter, PartialGroup
hentai_mode = {0: "disabled", 1: "show", 2: "only"}


class User:
    """Represents a MangaDex User."""
    __slots__ = ("id", "username", "level_id", "joined", "last_seen", "website", "bio", "views", "uploads", "premium",
                 "md_ah", "avatar", "chapters_uploaded", "groups")

    def __init__(self, data, chaps=None, groups=None):
        self.id = data["id"]
        self.username = data["username"]
        self.level_id = data["levelId"]
        self.joined = data["joined"]
        self.last_seen = data["lastSeen"]
        self.website = data["website"]
        self.bio = data["biography"]
        self.views = data["views"]
        self.uploads = data["uploads"]
        self.premium = data["premium"]
        self.md_ah = data["mdAtHome"]
        self.avatar = data["avatar"]
        self.chapters_uploaded = [PartialChapter(x) for x in chaps or []]
        self.groups = [PartialGroup(x) for x in groups or []]


class UserSettings:
    """Represents a MangaDex User's settings."""
    __slots__ = ("id", "hentai_mode", "latest_update", "show_moderated_posts", "show_unavailable_chapters",
                 "whitelisted_languages", "blacklisted_tags")

    def __init__(self, data):
        self.id = data["id"]
        self.hentai_mode = hentai_mode[data["hentaiMode"]]
        self.latest_update = data["latestUpdates"]
        self.show_moderated_posts = data["showModeratedPosts"]
        self.show_unavailable_chapters = data["showUnavailableChapters"]
        self.whitelisted_languages = data["shownChapterLangs"]
        self.blacklisted_tags = data["excludedTags"]


class UserFollow:
    """Represents a MangaDex User's followed manga."""
    __slots__ = ("user", "id", "title", "hentai", "follow_type", "user_volume", "user_chapter", "user_rating", "cover")

    def __init__(self, data):
        self.user = data["userId"]
        self.id = data["mangaId"]
        self.title = data["mangaTitle"]
        self.hentai = data["isHentai"]
        self.follow_type = data["followType"]
        self.user_volume = data["volume"]
        self.user_chapter = data["chapter"]
        self.user_rating = data["rating"]
        self.cover = data["mainCover"]


class UserUpdate:
    """Represents a MangaDex User's feed item."""
    __slots__ = ("id", "hash", "manga_id", "manga_title", "volume", "chapter", "title", "language", "groups",
                 "uploader", "timestamp", "thread_id", "comments", "views", "read")

    def __init__(self, data):
        self.id = data["id"]
        self.hash = data["hash"]
        self.manga_id = data["mangaId"]
        self.manga_title = data["mangaTitle"]
        self.volume = data["volume"]
        self.chapter = data["chapter"]
        self.title = data["title"]
        self.language = data["language"]
        self.groups = data["groups"]
        self.uploader = data["uploader"]
        self.timestamp = data["timestamp"]
        self.thread_id = data["threadId"]
        self.comments = data["comments"]
        self.views = data["views"]
        self.read = data["read"]
