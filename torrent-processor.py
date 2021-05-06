from os import close, scandir
from pathlib import Path
import xml.etree.ElementTree as ET
import re
from confuse.exceptions import NotFoundError
import requests
import confuse
import subprocess

mandatory_config_values = ['regexps', 'rss', 'torrentFileDirectory']

def load_configuration():
    config = confuse.Configuration('torrent-processor', __name__)
    for cfg in mandatory_config_values:
        try:
            config[cfg].get()
        except NotFoundError:
            print('ERROR_CONFIG - Configuration value "' + cfg + '" not found.')
            return None

    return config

def load_rss(rss_url):
    root = None
    try:
        root = ET.fromstring(requests.get(rss_url, allow_redirects=True).content)
    except Exception:
        print('CANNOT_LOAD_RSS - ' + rss_url)

    return root

def get_filename_from_cd(cd):
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

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

    r = requests.get(url, allow_redirects=True)
    if r.status_code == 200:
        filename = get_filename_from_cd(r.headers.get('content-disposition'))
        if not filename:
            print('ERROR_DOWNLOAD_TORRENTFILE_NO_FILENAME - ' + title)
        elif not is_duplicate(filename, torrent_file_directory):
            print('DOWNLOAD_STARTED_TORRENTFILE - ' + filename)
            torrent_file = None
            try:
                torrent_file = open(torrent_file_directory + '/' + filename, 'wb')
                torrent_file.write(r.content)
                downloaded = True
            except IOError:
                print('ERROR_UNABLE_TO_WRITE_TORRENTFILE - ' + filename)
            finally:
                if torrent_file:
                    torrent_file.close()     
    else:
        print('ERROR_DOWNLOAD_TORRENTFILE_' + str(r.status_code) + ' - ' + title + ' - ' + url)

    return filename, downloaded

def download_torrent(filename, torrent_file_directory):
    try:
        download_process = subprocess.run(['transmission-remote', 'localhost:9091', '--add', torrent_file_directory + '/' + filename], stdout=subprocess.PIPE)
        if download_process.returncode != 0:
            print('ERROR_DOWNLOADING_TORRENT - ' + download_process.stdout)
        else:
            print('TORRENT_ADDED_TO_QUEUE - ' + filename)
    except Exception:
        print('ERROR_DOWNLOADING_TORRENT - ' + filename)

def main():
    config = load_configuration()
    if not config:
        return

    root = load_rss(config['rss'].get())
    if not root:
        return

    torrent_file_directory = config['torrentFileDirectory'].get()

    regexp_list = config['regexps'].get()
    for item in root.findall('.*/item'):
        title = item.findtext('title')
        for regexp in regexp_list:
            if re.match(regexp, title):
                print('MATCH - ' + title)
                url = item.findtext('link')
                filename, downloaded = download_torrent_file(url, title, torrent_file_directory)
                if downloaded:
                    download_torrent(filename, torrent_file_directory)

if __name__ == "__main__":
    main()

