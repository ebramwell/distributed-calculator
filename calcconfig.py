import json

class CalcConfig:
    def __init__(self, config_file='calc.json'):
        """
        This class reads the configuration file and provides access to the configuration data.
        """
        self.config_file = config_file
        self._config_data = self._load_config()

    def _load_config(self):
        """
        This function reads the configuration file and returns the data as a dictionary.
        """
        with open(self.config_file, 'r') as file:
            return json.load(file)

    @property
    def api_host(self):
        """
        This property returns the value of the api_host key from the configuration data.
        """
        return self._config_data.get('api_host')

