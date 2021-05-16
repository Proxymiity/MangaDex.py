from .chapter import Chapter
import time
from requests import exceptions as rex
from pathlib import Path


def dl_page(net, page, path):
    """Helper for dl_chapter to download pages with."""
    try:
        with net.client.session.get(page) as p:
            with open(str(Path(path + "/" + page.rsplit("/", 1)[1])), "wb") as f:
                f.write(p.content)
            success = True if p.status_code <= 400 else False
            cached = True if p.headers["x-cache"] == "HIT" else False
            net.report(page, success, cached, len(p.content), int(p.elapsed.microseconds/1000))
            print(f"Statistics for {page}\nTime: {int(p.elapsed.microseconds/1000)}, length: {len(p.content)}"
                  f"\nSuccess: {success}, was cached on server: {cached}\nHeaders: {p.headers}")
            return True
    except rex.RequestException:
        net.report(page, False, False, 0, 0)
        print(f"Request for {page} failed. This was reported to the MD backend, you should try to download the image"
              f" again to get a new server.")
        return False


def dl_chapter(chapter: Chapter, path, light: bool = False, time_controller: int = 1):
    """Downloads an entire chapter."""
    net = chapter.get_md_network()
    print(f"Got assigned a MD@H node to download: {net.node_url}. Attempting to download {len(net.pages)} pages.")
    if light:
        pages = net.pages_redux
    else:
        pages = net.pages
    for x in pages:
        while True:
            resp = dl_page(net, x, path)
            if resp:
                break
            else:
                net = chapter.get_md_network()
                print(f"Got assigned a new MD@H node to download: {net.node_url}. Resuming downloads...")
        if time_controller:
            time.sleep(time_controller)
    print(f"Successfully downloaded and reported status for {len(net.pages)} pages.")
