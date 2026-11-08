# VERSION: 2.0
# AUTHORS: ChatGPT

import json
import re
from urllib.parse import quote, unquote, urlencode, urljoin, urlparse, parse_qs

from helpers import retrieve_url
from novaprinter import prettyPrinter


class thepiratebay:
    """The Pirate Bay search plugin using the apibay.org JSON API."""

    url = "https://thepiratebay.org"
    name = "ThePirateBay"

    search_url = "https://apibay.org/q.php"
    torrent_url = "https://apibay.org/t.php"

    # qBittorrent's standard categories mapped to TPB category IDs.
    # TPB does not have a dedicated anime category.
    supported_categories = {
        "all": "0",
        "anime": "200",
        "books": "601",
        "games": "400",
        "movies": "200",
        "music": "100",
        "pictures": "603",
        "software": "300",
        "tv": "205",
    }

    # Complete TPB category hierarchy.
    tpb_categories = {
        "audio": {
            "100": "Audio",
            "101": "Music",
            "102": "Audio books",
            "103": "Sound clips",
            "104": "FLAC",
            "199": "Other",
        },
        "video": {
            "200": "Video",
            "201": "Movies",
            "202": "Movies DVDR",
            "203": "Music videos",
            "204": "Movie clips",
            "205": "TV shows",
            "206": "Handheld",
            "207": "HD - Movies",
            "208": "HD - TV shows",
            "209": "3D",
            "210": "CAM/TS",
            "211": "UHD/4k - Movies",
            "212": "UHD/4k - TV shows",
            "299": "Other",
        },
        "applications": {
            "300": "Applications",
            "301": "Windows",
            "302": "Mac",
            "303": "UNIX",
            "304": "Handheld",
            "305": "IOS",
            "306": "Android",
            "399": "Other OS",
        },
        "games": {
            "400": "Games",
            "401": "PC",
            "402": "Mac",
            "403": "PSx",
            "404": "XBOX360",
            "405": "Wii",
            "406": "Handheld",
            "407": "IOS",
            "408": "Android",
            "499": "Other",
        },
        "porn": {
            "500": "Porn",
            "501": "Movies",
            "502": "Movies DVDR",
            "503": "Pictures",
            "504": "Games",
            "505": "HD - Movies",
            "506": "Movie clips",
            "507": "UHD/4k - Movies",
            "599": "Other",
        },
        "other": {
            "600": "Other",
            "601": "E-books",
            "602": "Comics",
            "603": "Pictures",
            "604": "Covers",
            "605": "Physibles",
            "699": "Other",
        },
    }

    @staticmethod
    def normalize_query(query):
        """
        Normalize a qBittorrent search query.

        Accepts ordinary text or an already percent-encoded query.
        A literal '+' in ordinary text is preserved.
        """

        query = (query or "").strip()

        if re.search(r"%[0-9a-fA-F]{2}", query):
            query = unquote(query)

        return query

    @staticmethod
    def make_magnet(info_hash, name):
        """Build a magnet URI from an info hash and torrent name."""

        return f"magnet:?xt=urn:btih:{info_hash}" f"&dn={quote(name)}"

    @staticmethod
    def parse_torrent(item):
        """Convert an API result into qBittorrent's result format."""

        info_hash = str(item.get("info_hash", "")).strip().upper()
        name = str(item.get("name", "")).strip()

        # Reject malformed API entries.
        if not name or not re.fullmatch(r"[A-F0-9]{40}", info_hash):
            return None

        try:
            torrent_id = str(item.get("id", ""))
            size = int(item.get("size", 0))
            seeds = int(item.get("seeders", 0))
            leech = int(item.get("leechers", 0))
            pub_date = int(item.get("added", -1))
        except (TypeError, ValueError):
            return None

        return {
            "site": thepiratebay.name,
            "engine_url": "https://thepiratebay.org",
            "name": name,
            "link": thepiratebay.make_magnet(info_hash, name),
            "size": size,
            "seeds": seeds,
            "leech": leech,
            "pub_date": pub_date,
            "desc_link": (
                (
                    f"https://thepiratebay.org/description.php?id={torrent_id}"
                    if torrent_id.isdigit()
                    else ""
                ),
            )[0],
            "uploader": str(item.get("username", "")),
            "category": str(item.get("category", "")),
            "status": str(item.get("status", "")),
        }

    def search(self, query, cat="all"):
        """Search TPB through the apibay.org API."""

        query = self.normalize_query(query)

        category = self.supported_categories.get(
            (cat or "all").lower(),
            "0",
        )

        params = {
            "q": query,
            "cat": category,
        }

        search_url = f"{self.search_url}?{urlencode(params)}"

        try:
            response = retrieve_url(search_url)

            if not response:
                return

            results = json.loads(response)

            if not isinstance(results, list):
                return

            for item in results:
                if not isinstance(item, dict):
                    continue

                result = self.parse_torrent(item)

                if result:
                    prettyPrinter(result)

        except (ValueError, TypeError):
            return
        except Exception as error:
            print(f"The Pirate Bay search error: {error}")

    def download_torrent(self, info):
        """
        Resolve a torrent ID or TPB description URL to a magnet URI.
        """

        if info.startswith("magnet:"):
            print(info)
            return

        torrent_id = None

        if info.isdigit():
            torrent_id = info
        else:
            parsed_url = urlparse(info)

            if parsed_url.netloc.endswith("apibay.org"):
                torrent_id = parse_qs(parsed_url.query).get("id", [None])[0]

            if not torrent_id:
                torrent_id = parse_qs(parsed_url.query).get("id", [None])[0]

        if not torrent_id or not torrent_id.isdigit():
            raise ValueError("Invalid TPB torrent ID.")

        response = retrieve_url(f"{self.torrent_url}?id={torrent_id}")

        if not response:
            raise ValueError("Could not retrieve torrent information.")

        item = json.loads(response)

        if not isinstance(item, dict):
            raise ValueError("Invalid API response.")

        result = self.parse_torrent(item)

        if not result:
            raise ValueError("Invalid torrent information.")

        print(result["link"])
