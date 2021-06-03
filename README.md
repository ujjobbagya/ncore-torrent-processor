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
- Greys\.Anatomy\.S17E.*720p.*
- Doktor\.Balaton\.S[0-9]{2}E.*720p.*
- Greys\.Anatomy\.S[0-9]{2}E.*720p.*HUN.*
- Joban\.Rosszban.*720p.*
- Raised\.by\.Wolves.*S02E.*720p.*
- A\.Konyhafonok.*720p.*
- The\.Guys.*S02E.*720p.*
- The\.Resident\.S[0-9]{2}E.*720p.*
- Mintaapak\.S[0-9]{2}E.*720p.*
- Resident\.Alien.*S02E.*720p.*
- The\.Good\.Doctor\.S[0-9]{2}E.*720p.*
- Doc\.In\.Your\.Hands.*
- Jupiters\.Legacy\.S02E.*1080p.*
- Better\.Call\.Saul.*S06E.*720p.*
torrentFileDirectory: /Users/aujjobba/dev/python
downloader: 
  transmission:
    host: localhost
    port: 9091
    username:
    password:
```
