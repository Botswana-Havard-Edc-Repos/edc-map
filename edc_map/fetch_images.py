import aiohttp
import asyncio
import logging

from contextlib import closing


class FetchImages:
    """Use aiohttp to download multiple map images at a time.

    Get the url and filename list from `Snapshot`.

    For example:
        # SubjectLocation model class has `geopy.Point(lat, lon)` and `map_area` name data
        zoom_levels = ['16', '17', '18']
        for obj in SubjectLocation.objects.all():
            s = Snapshot(obj.pk, obj.point, obj.map_area,
                         zoom_levels=zoom_levels, app_label='bcpp_map')
            for zoom_level in zoom_levels:
                download_items.append(
                    (s.image_url(zoom_level),
                    s.image_filename(zoom_level, include_path=True)))
        fetch_images = FetchImages(download_items=download_items, sephamores=12)
    """
    def __init__(self, download_items=None, sephamores=None):
        self.download_items = download_items  # [(url, file), ...]
        self.sephamores = sephamores or 25

    async def download(self, url, filename, session, semaphore, chunk_size=1 << 15):
        with (await semaphore):  # limit number of concurrent downloads
            logging.info('downloading %s', filename)
            response = await session.get(url)
            with closing(response), open(filename, 'wb') as file:
                while True:  # save file
                    chunk = await response.content.read(chunk_size)
                    if not chunk:
                        break
                    file.write(chunk)
            logging.info('done %s', filename)
        return filename, (response.status, tuple(response.headers.items()))

    def fetch(self):
        results = []
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
        with closing(asyncio.get_event_loop()) as loop, closing(aiohttp.ClientSession()) as session:
            semaphore = asyncio.Semaphore(self.sephamores)
            download_tasks = (self.download(url, filename, session, semaphore) for url, filename in self.download_items)
            result = loop.run_until_complete(asyncio.gather(*download_tasks))
            results.append(result)
        return results
