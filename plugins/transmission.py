from exceptions.exceptions import DownloaderConfigurationException

class Transmission:

    configuration_name = 'transmission'
    uri = None
    username_password = None

    def configure(self, configuration):
        try:
            self.uri = str(configuration['host']) + ':' + str(configuration['port'])
            username_config = configuration['username']
            password_config = configuration['password']
            if username_config.exists() and username_config.get() and password_config.exists() and password_config.get():
                self.username_password = username_config.get() + ':' + password_config.get()
        except Exception as e:
            raise DownloaderConfigurationException('CANNOT_CONFIGURE_DOWNLOADER - ' + str(e))

    def construct_command_array(self, torrent_file_path):
        command_array = ['transmission-remote', self.uri]
        if self.username_password:
            command_array.extend(['-n', self.username_password])
        command_array.extend(['--add', torrent_file_path])

        return command_array

    def get_configuration_name(self):
        return self.configuration_name