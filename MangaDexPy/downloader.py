from .chapter import Chapter
import time
from pathlib import Path


def dl_page(net, page, path):
    """Downloads a single page."""
    with net.client.session.get(page) as p:
        with open(str(Path(path + "/" + page.rsplit("/", 1)[1])), "wb") as f:
            f.write(p.content)
        success = True if p.status_code <= 400 else False
        cached = True if p.headers["x-cache"] == "HIT" else False
        net.report(page, success, cached, len(p.content), int(p.elapsed.microseconds/1000))
        print(f"Statistics for {page}\nTime: {int(p.elapsed.microseconds/1000)}, length: {len(p.content)}"
              f"\nSuccess: {success}, was cached on server: {cached}\nHeaders: {p.headers}")


def dl_chapter(chapter: Chapter, path, time_controller: int = 1):
    """Downloads an entire chapter."""
    net = chapter.get_md_network()
    for x in net.pages:
        dl_page(net, x, path)
        if time_controller:
            time.sleep(time_controller)
