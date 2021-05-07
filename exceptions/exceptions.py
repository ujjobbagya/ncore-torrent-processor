class TorrentProcessorException(Exception):
    pass

class DownloaderConfigurationException(TorrentProcessorException):
    pass

class DownloaderNotFoundException(TorrentProcessorException):
    pass

class ConfigurationException(TorrentProcessorException):
    pass

class RssLoadingException(TorrentProcessorException):
    pass

class DownloadTorrentFileException(TorrentProcessorException):
    pass

class DownloadTorrentException(TorrentProcessorException):
    pass
