from exceptions.exceptions import ConfigurationException, DownloadTorrentException, DownloadTorrentFileException, RssLoadingException, TorrentProcessorException
from os import close, scandir
from pathlib import Path
import xml.etree.ElementTree as ET
import re
from confuse.exceptions import NotFoundError
import requests
import confuse
import subprocess
import plugins.transmission as TM
import downloaderfactory as DF

mandatory_config_values = ['regexps', 'rss', 'torrentFileDirectory', 'downloader']

def load_configuration():
    config = confuse.Configuration('torrent-processor', __name__)

    for cfg in mandatory_config_values:
        if not config[cfg].exists():
            raise ConfigurationException('ERROR_CONFIG - Configuration value "' + cfg + '" not found.')

    try:
        config['downloader'].keys()[0]
    except Exception as e:
        raise ConfigurationException('ERROR_CONFIG - Configuration value "downloader" is invalid. - ' + str(e))

    return config

def load_rss(rss_url):
    try:
        root = ET.fromstring(requests.get(rss_url, allow_redirects=True).content)
    except Exception as e:
        raise RssLoadingException('CANNOT_LOAD_RSS - ' + rss_url + ' - ' + str(e))

    print('RSS_LOADED')

    return root

def get_filename_from_cd(cd):
    if cd:
        fname = re.findall('filename="(.+)"', cd)
        if len(fname) != 0:
            return fname[0]
    
    raise DownloadTorrentFileException('ERROR_DOWNLOAD_TORRENTFILE_NO_FILENAME')

def is_duplicate(filename, torrent_file_directory):
    duplicate = False
    for file in scandir(torrent_file_directory):
        if file.is_file and file.name == filename:
            print('SKIP_ALREADY_DOWNLOADED_TORRENTFILE - ' + filename)
            duplicate = True

    return duplicate

def download_torrent_file(url, title, torrent_file_directory):
    filename = None
    downloaded = False

    try:
        r = requests.get(url, allow_redirects=True)
    except Exception as e:
        raise DownloadTorrentFileException('ERROR_DOWNLOAD_TORRENTFILE_' + str(e))

    if r.status_code == 200:
        filename = get_filename_from_cd(r.headers.get('content-dispositio'))

        if not is_duplicate(filename, torrent_file_directory):
            print('DOWNLOAD_STARTED_TORRENTFILE - ' + filename)
            torrent_file = None
            try:
                torrent_file = open(torrent_file_directory + '/' + filename, 'wb')
                torrent_file.write(r.content)
                downloaded = True
                print('DOWNLOADED_TORRENTFILE - ' + filename)
            except IOError as e:
                raise DownloadTorrentFileException('ERROR_UNABLE_TO_WRITE_TORRENTFILE - ' + filename + ' - ' + str(e))
            finally:
                if torrent_file:
                    torrent_file.close()     
    else:
        raise DownloadTorrentFileException('ERROR_DOWNLOAD_TORRENTFILE_' + str(r.status_code) + ' - ' + title + ' - ' + url)

    return filename, downloaded

def download_torrent(filename, torrent_file_directory, downloader):
    try:
        download_process = subprocess.run(downloader.construct_command_array(torrent_file_directory + '/' + filename), stdout=subprocess.PIPE)
        if download_process.returncode != 0:
            raise DownloadTorrentException('ERROR_DOWNLOADING_TORRENT - ' + download_process.stdout)
        else:
            print('TORRENT_ADDED_TO_QUEUE - ' + filename)
    except Exception as e:
        raise DownloadTorrentException('ERROR_DOWNLOADING_TORRENT - ' + filename + ' - ' + str(e))

def main():
    try:   
        config = load_configuration()
        downloader = DF.DownloaderFactory().get_downloader(config['downloader'])
        root = load_rss(config['rss'].get())
    except TorrentProcessorException as e:
        print(str(e))
        return

    torrent_file_directory = config['torrentFileDirectory'].get()

    regexp_list = config['regexps'].get()
    for item in root.findall('.*/item'):
        title = item.findtext('title')
        for regexp in regexp_list:
            if re.match(regexp, title):
                print('MATCH - ' + title)
                url = item.findtext('link')
                try:
                    filename, downloaded = download_torrent_file(url, title, torrent_file_directory)
                    if downloaded:
                        download_torrent(filename, torrent_file_directory, downloader)
                except TorrentProcessorException as e:
                    print(str(e))

if __name__ == "__main__":
    main()

