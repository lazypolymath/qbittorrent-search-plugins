
# VERSION: 4.17
# AUTHORS: Lima66, ChatGPT
# CONTRIBUTORS: Diego de las Heras (ngosang@hotmail.es)

import re
from datetime import datetime, timedelta
from html.parser import HTMLParser
from typing import Callable, Dict, List, Mapping, Match, Tuple, Union
from urllib.parse import quote, urljoin

from helpers import retrieve_url
from novaprinter import prettyPrinter


class limetorrents:
    """LimeTorrents search engine plugin for qBittorrent."""

    url = "https://limetorrents.fun"
    name = "LimeTorrents"

    # Map qBittorrent categories to LimeTorrents URL categories.
    supported_categories = {
        'all': 'all',
        'anime': 'anime',
        'software': 'applications',
        'games': 'games',
        'movies': 'movies',
        'music': 'music',
        'tv': 'tv',
    }

    class MyHtmlParser(HTMLParser):
        """Parse torrent results from the LimeTorrents results table."""

        # HTML elements and attributes used by the parser.
        A, TD, TR, HREF = ('a', 'td', 'tr', 'href')

        def __init__(self, url: str) -> None:
            super().__init__()

            self.url = url
            self.current_item: Dict[str, object] = {}
            self.page_items = 0

            # Track the results table and current torrent row.
            self.inside_table = False
            self.inside_tr = False
            self.inside_name = False

            # Track the current table column.
            self.column_index = -1
            self.column_name: Union[str, None] = None

            # The Health column is intentionally ignored.
            self.columns = [
                "name",
                "pub_date",
                "size",
                "seeds",
                "leech",
            ]

            # Convert relative publication dates into Unix timestamps.
            now = datetime.now().astimezone()
            self.date_parsers: Mapping[str, Callable[[Match[str]], datetime]] = {
                r"yesterday": lambda m: now - timedelta(days=1),
                r"last\s+month": lambda m: now - timedelta(days=30),
                r"(\d+)\s+years?": lambda m: now - timedelta(days=int(m[1]) * 365),
                r"(\d+)\s+months?": lambda m: now - timedelta(days=int(m[1]) * 30),
                r"(\d+)\s+days?": lambda m: now - timedelta(days=int(m[1])),
                r"(\d+)\s+hours?": lambda m: now - timedelta(hours=int(m[1])),
                r"(\d+)\s+minutes?": lambda m: now - timedelta(minutes=int(m[1])),
            }

        def handle_starttag(
            self,
            tag: str,
            attrs: List[Tuple[str, Union[str, None]]],
        ) -> None:
            params = dict(attrs)
            classes = (params.get('class') or '').split()

            # Identify the torrent results table.
            if tag == 'table' and 'table2' in classes:
                self.inside_table = True
                return

            if not self.inside_table:
                return

            if tag == self.TR:
                # Torrent rows alternate between these two background colors.
                if params.get('bgcolor', '').upper() in ('#F4F4F4', '#FFFFFF'):
                    self.inside_tr = True
                    self.column_index = -1
                    self.column_name = None
                    self.current_item = {"engine_url": self.url}
                return

            if not self.inside_tr:
                return

            if tag == self.TD:
                # Associate each table cell with its corresponding field.
                self.column_index += 1
                self.column_name = (
                    self.columns[self.column_index]
                    if self.column_index < len(self.columns)
                    else None
                )

            elif tag == 'div' and 'tt-name' in classes:
                # Torrent titles are nested inside div.tt-name.
                self.inside_name = True

            elif (
                self.inside_name
                and tag == self.A
                and self.HREF in params
            ):
                link = params[self.HREF]

                # Ignore the .torrent download link and capture the info page.
                if link and link.endswith('.html'):
                    safe_link = quote(
                        urljoin(self.url, link),
                        safe='/:'
                    )
                    self.current_item["link"] = safe_link
                    self.current_item["desc_link"] = safe_link

        def handle_data(self, data: str) -> None:
            if not self.inside_tr or not self.column_name:
                return

            data = data.strip()
            if not data:
                return

            if self.column_name == "name":
                # Capture the actual torrent title, not the download link text.
                if self.inside_name:
                    self.current_item["name"] = data
                return

            if self.column_name in ("size", "seeds", "leech"):
                # Remove thousands separators from numeric fields.
                data = data.replace(',', '')

            elif self.column_name == "pub_date":
                # Dates include category suffixes, e.g. "Last Month - in TV shows".
                date_text = re.split(r'\s+-\s+in\s+', data, maxsplit=1)[0]
                timestamp = -1

                for pattern, calc in self.date_parsers.items():
                    match = re.match(pattern, date_text, re.IGNORECASE)
                    if match:
                        timestamp = int(calc(match).timestamp())
                        break

                # Use -1 when the date format is unknown.
                data = str(timestamp)

            self.current_item[self.column_name] = data
            self.column_name = None

        def handle_endtag(self, tag: str) -> None:
            if tag == 'div' and self.inside_name:
                self.inside_name = False

            if tag == self.TR and self.inside_tr:
                self.inside_tr = False
                self.inside_name = False
                self.column_name = None

                # Only submit complete results to qBittorrent.
                if "name" in self.current_item and "link" in self.current_item:
                    prettyPrinter(self.current_item)  # type: ignore[arg-type]
                    self.page_items += 1

            elif tag == 'table' and self.inside_table:
                self.inside_table = False

    def download_torrent(self, info: str) -> None:
        """Extract and return a magnet link from a torrent info page."""

        info_page = retrieve_url(info)

        # LimeTorrents exposes the magnet URI directly on the info page.
        magnet_match = re.search(
            r'href\s*=\s*["\'](magnet:\?[^"\']+)["\']',
            info_page,
            re.IGNORECASE,
        )

        if magnet_match:
            print(magnet_match.group(1) + " " + info)
        else:
            raise ValueError('Error, please fill a bug report!')

    def search(self, query: str, cat: str = 'all') -> None:
        """Search LimeTorrents and return matching torrents."""

        # qBittorrent may supply URL-encoded spaces.
        query = query.replace("%20", "+")
        category = self.supported_categories[cat]

        # Search up to four result pages.
        for page in range(1, 5):
            page_url = f"{self.url}/search/{category}/{query}/"

            # Subsequent-page URL format is based on the site's pagination.
            if page > 1:
                page_url += f"{page}/"

            html = retrieve_url(page_url)

            parser = self.MyHtmlParser(self.url)
            parser.feed(html)
            parser.close()

            # Stop when the current page contains fewer than 20 results.
            if parser.page_items < 20:
                break
