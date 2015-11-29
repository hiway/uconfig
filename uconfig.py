import os
import yaml

defaults = {
    'config_root': '~',
    'config_extension': '.yaml',
}


class uConfig(object):
    def __init__(self, app_name, config_name, default):
        self._app_name = app_name
        self._config_name = config_name
        self._default_config = default
        self._config = {}
        self._config = self._get_or_create_config(default)

    def __getattribute__(self, item):
        if item.startswith('_'):
            return object.__getattribute__(self, item)
        return self._config.get(item)

    def __getitem__(self, item):
        return self._config.get(item)

    def __setitem__(self, key, value):
        self._config[key] = value
        self._save_config()

    def __iter__(self):
        for key, value in self._config.items():
            yield key, value

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
            return
        self._config[key] = value
        self._save_config()

    def _update(self, dictionary):
        assert type(self._config) == dict
        assert type(dictionary) == dict
        self._config.update(dictionary)
        self._save_config()

    def _exists(self, key):
        return key in self._config

    def _reset(self):
        self._config = self._default_config
        self._save_config()

    def _get_or_create_config(self, default_config):
        base_path = os.path.expanduser(defaults['config_root'])
        app_path = os.path.join(base_path, '.' + self._app_name)
        config_path = os.path.join(app_path, self._config_name + defaults['config_extension'])
        self._config_path = config_path
        if not (os.path.exists(app_path) and os.path.isdir(app_path)):
            os.mkdir(app_path)
        if not os.path.exists(config_path):
            with open(config_path, 'w') as config_file:
                yaml.dump(default_config, config_file)
        with open(config_path, 'r') as config_file:
            return yaml.load(config_file)

    def _save_config(self):
        with open(self._config_path, 'w') as config_file:
            yaml.dump(self._config, config_file,
                      explicit_start=False,
                      default_flow_style=False)
