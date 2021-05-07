# ncore-torrent-processor
This tool is intended to search torrent within a configured RSS, by using regular expressions, than add those to the queue.
## Limitations
Currently only Transmission is supported, another tools can be integrated in the future.
## Config file
The configuration file is in YAML format, must be placed as CONFIG_HOME/torrent-processor/config.yaml.  For more info about where the tool is searching for the config can be found at [Confuse's documentation](https://confuse.readthedocs.io/en/latest/usage.html#search-paths).
## Example configuration file
```yaml
rss: https://ncore.pro/rss.php?key=<mykey>
regexps:
- Greys\.Anatomy.*720p.*
- Joban\.Rosszban.*720p.*
- Raised\.by\.Wolfs.*720p.*
- A\.Konyhafonok.*720p.*
- The\.Guys.*720p.*
- The\.Resident.*720p.*
- Mintaapak.*720p.*
- Resident\.Alien.*720p.*
- The\.Good\.Doctor.*720p.*
- Doc\.in\.Your\.Hands.*
torrentFileDirectory: /Users/aujjobba/dev/python
downloader: 
  transmission:
    host: localhost
    port: 9091
    username:
    password:
```
