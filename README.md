# Search Plugins

A collection of search engine plugins for [qBittorrent](https://www.qbittorrent.org/), providing support for multiple torrent search providers.

## Providers

### Completed

| Provider | Website | API |
|---|---|---|
| LimeTorrents | [limetorrents.fun](https://limetorrents.fun/) | Website |
| The Pirate Bay | [thepiratebay.org](https://thepiratebay.org/) | [Apibay](https://apibay.org/) |

Additional providers are planned and will be added progressively.

## Installation

1. Open qBittorrent.
2. Navigate to **Search → Search Plugins → Install a new one**.
3. Select **Install a plugin from a file**.
4. Select the desired provider's `.py` plugin file.

Alternatively, copy the plugins into your qBittorrent search engine directory:

```bash
~/.local/share/qBittorrent/nova3/engines/
```

Restart qBittorrent or refresh the search plugins.

---

## LimeTorrents

The LimeTorrents provider is adapted from the original qBittorrent search plugin to support the updated LimeTorrents website.

**Download Plugin:**

[limetorrents.py](https://raw.githubusercontent.com/lazypolymath/qbittorrent-search-plugins/main/limetorrents.py)

**Original implementation:**

[qBittorrent Search Plugins — limetorrents.py](https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/limetorrents.py)

**Related discussion:**

[qBittorrent Search Plugins — Discussion #208](https://github.com/qbittorrent/search-plugins/discussions/208#discussioncomment-3622963)

### Features

- Search across supported categories.
- Retrieve torrent names, publication dates, sizes, seeders, and leechers.
- Resolve torrent information pages.
- Extract magnet links directly from torrent pages.
- Support up to four pages of search results.

### Supported Categories

| qBittorrent Category | LimeTorrents Category |
|---|---|
| All | all |
| Anime | anime |
| Software | applications |
| Games | games |
| Movies | movies |
| Music | music |
| TV | tv |

### Development

The plugin uses Python's standard library for HTML parsing, date conversion, and URL handling.

It integrates with qBittorrent's Nova search engine API:

- `retrieve_url` — retrieve web pages.
- `prettyPrinter` — format and return search results.

### Version

4.17

### Credits

- **Converted to limetorrents.fun:** ChatGPT
- **Original author:** Lima66
- **Original contributor:** Diego de las Heras (ngosang@hotmail.es)
- **Original project:** [qBittorrent Search Plugins](https://github.com/qbittorrent/search-plugins)

### License

Refer to the original plugin's licensing terms and include the applicable license when redistributing modified code.

---

## The Pirate Bay

The Pirate Bay provider uses the [Apibay API](https://apibay.org/) to retrieve torrent search results in JSON format.

**Download Plugin:**

[thepiratebay.py](https://raw.githubusercontent.com/lazypolymath/qbittorrent-search-plugins/main/thepiratebay.py)

### Features

- Search using the Apibay JSON API.
- Retrieve torrent names, publication dates, sizes, seeders, and leechers.
- Generate magnet links directly from torrent info hashes.
- Resolve torrent IDs and information pages.
- Display uploader and torrent status information.
- Map qBittorrent search categories to The Pirate Bay categories.

### API

Search endpoint:

```text
https://apibay.org/q.php?q={query}&cat={category}
```

Torrent information endpoint:

```text
https://apibay.org/t.php?id={torrent_id}
```

The search API returns structured JSON containing fields such as:

- `id` — torrent identifier.
- `name` — torrent name.
- `info_hash` — BitTorrent info hash.
- `seeders` — seed count.
- `leechers` — leech count.
- `size` — file size in bytes.
- `added` — Unix publication timestamp.
- `username` — uploader.
- `status` — uploader/torrent status.
- `category` — TPB category ID.

### Supported Categories

| qBittorrent Category | TPB Category ID | TPB Category |
|---|---:|---|
| All | 0 | All |
| Anime | 200 | Video |
| Books | 601 | E-books |
| Games | 400 | Games |
| Movies | 200 | Video |
| Music | 100 | Audio |
| Pictures | 603 | Pictures |
| Software | 300 | Applications |
| TV | 205 | TV shows |

The plugin also maintains the complete TPB category hierarchy internally, including subcategories for audio, video, applications, games, adult content, and other files.

### Development

The plugin uses Python's standard library for JSON parsing, URL encoding, regular expressions, and magnet URI generation.

It integrates with qBittorrent's Nova search engine API:

- `retrieve_url` — retrieve API responses.
- `prettyPrinter` — format and return search results.

### Version

2.0

### Credits

- **API:** [Apibay](https://apibay.org/)
- **Original project:** [The Pirate Bay](https://thepiratebay.org/)
- **Implementation:** ChatGPT

### License

Refer to the applicable API terms and licensing requirements before redistributing modified code.

---

## Contributing

Contributions, provider suggestions, bug reports, and improvements are welcome.

When contributing a new provider, include:

- The provider's website and API (if available).
- A qBittorrent-compatible Python search plugin.
- Supported category mappings.
- Installation and usage documentation.