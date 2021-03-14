from .partial import PartialChapter, PartialGroup


class Group:
    """Represents a MangaDex Group."""
    __slots__ = ("id", "name", "names", "language", "leader", "members", "desc", "website", "discord", "irc_server",
                 "irc_channel", "email", "founded_on", "follows", "views", "chapters", "thread_id", "thread_posts",
                 "locked", "inactive", "delay", "last_update", "banner", "chapters_uploaded", "collabs")

    def __init__(self, data, chaps=None, groups=None):
        self.id = data["id"]
        self.name = data["name"]
        self.names = data["altNames"]
        self.language = data["language"]
        self.leader = data["leader"]
        self.members = data["members"]
        self.desc = data["description"]
        self.website = data["website"]
        self.discord = data["discord"]
        self.irc_server = data["ircServer"]
        self.irc_channel = data["ircChannel"]
        self.email = data["email"]
        self.founded_on = data["founded"]
        self.follows = data["follows"]
        self.views = data["views"]
        self.chapters = data["chapters"]
        self.thread_id = data["threadId"]
        self.thread_posts = data["threadPosts"]
        self.locked = data["isLocked"]
        self.inactive = data["isInactive"]
        self.delay = data["delay"]
        self.last_update = data["lastUpdated"]
        self.banner = data["banner"]
        self.chapters_uploaded = [PartialChapter(x) for x in chaps or []]
        self.collabs = [PartialGroup(x) for x in groups or []]
