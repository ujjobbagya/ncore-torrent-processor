from os import close
import xml.etree.ElementTree as ET
import re
import requests

tree = ET.parse('rss.php.xml')
root = tree.getroot()

regexp_list = [
    'Greys\.Anatomy.*720p.*HUN',
    'Joban\.Rosszban.*720p.*',
    'Tricky.*2160p.*']

def get_filename_from_cd(cd):
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

for item in root.findall('.*/item'):
    title = item.findtext('title')
    found = False
    for regexp in regexp_list:
        if re.match(regexp, title):
            found = True
            print('MATCH - ' + title)
            url = item.findtext('link')
            r = requests.get(url, allow_redirects=True)
            if r.status_code == 200:
                filename = get_filename_from_cd(r.headers.get('content-disposition'))
                if filename:
                    print('DOWNLOAD_STARTED - ' + filename)
                    torrent_file = None
                    try:
                        torrent_file = open(filename, 'wb')
                        torrent_file.write(r.content)
                    except IOError:
                        print('ERROR_UNABLE_TO_WRITE - ' + filename)
                    finally:
                        if torrent_file:
                            torrent_file.close
                else:
                    print('ERROR_DOWNLOAD_NO_FILENAME - ' + title)
            else:
                print('ERROR_DOWNLOAD_' + str(r.status_code) + ' - ' + title + ' - ' + url)
