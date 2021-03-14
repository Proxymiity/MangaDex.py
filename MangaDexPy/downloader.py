from .chapter import Chapter
import time
from pathlib import Path


def dl_page(chapter: Chapter, page, path, fallback=False):
    """Downloads a single page."""
    with chapter.session.get(chapter.format_url(page, fallback)) as p:
        with open(str(Path(path + "/" + page)), "wb") as f:
            f.write(p.content)


def dl_chapter(chapter: Chapter, path, fallback=False, time_controller: int = 1):
    """Downloads an entire chapter."""
    chapter.refresh()
    y = 0
    for x in chapter.pages:
        dl_page(chapter, x, path, fallback)
        if time_controller:
            time.sleep(time_controller)
        y += 1
