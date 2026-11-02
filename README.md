# Search Plugins

A collection of search engine plugins for [qBittorrent](https://www.qbittorrent.org/), providing support for multiple torrent search providers.

## Providers

### Completed

| Provider     | Website                                       |
| ------------ | --------------------------------------------- |
| LimeTorrents | [limetorrents.fun](https://limetorrents.fun/) |

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
- Supports up to four pages of search results.

### Supported Categories

| qBittorrent Category | LimeTorrents Category |
| -------------------- | --------------------- |
| All                  | all                   |
| Anime                | anime                 |
| Software             | applications          |
| Games                | games                 |
| Movies               | movies                |
| Music                | music                 |
| TV                   | tv                    |

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

## Contributing

Contributions, provider suggestions, and improvements are welcome.
