from exceptions.exceptions import DownloaderNotFoundException
from plugins.transmission import Transmission
import plugins.transmission

class DownloaderFactory:

    downloaders = [Transmission]

    def get_downloader(self, downloader_config):
        configuration_name = downloader_config.keys()[0]
        for downloader in self.downloaders:
            instance = downloader()
            if instance.get_configuration_name() == configuration_name:
                print('DOWNLOADER_FOUND - ' + configuration_name)
                instance.configure(downloader_config[configuration_name])
                return instance
        raise DownloaderNotFoundException('DOWNLOADER_NOT_FOUND - ' + configuration_name)
