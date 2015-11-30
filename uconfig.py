"""
Module Defaults:


The default config_root is set to user's home directory, you can
override it thus:

    import uconfig
    uconfig.defaults.update({'config_root': '/another/path/'})

Default config_extension is set to '.yaml', you may change this,
though uconfig currently continues to serialize using yaml, this
limitation will change later.

    uconfig.defaults.update({'config_extension': '.conf'})

Default config_folder_prefix creates a hidden folder placing
a dot before the folder name, you can change this to an empty
string if you don't want to hide folders, or use another prefix.

    uconfig.defaults.update({'config_folder_prefix': ''})

Default auto_save is True, which ensures that every time you set
a key on uConfig, it automatically writes the changes to file.
You can set this to False, and use uConfig._save() to
explicitly write the config.

    uconfig.defaults.update({'auto_save': False})
    conf = uconfig.uConfig('app', 'config', {})
    conf._update({'some':'new', 'keys': True})
    conf._save()
"""

import os
import yaml
import inspect
from pathlib import Path

defaults = {
    'config_root': '~',  # base folder where app-config folder will be created
    'config_extension': '.yaml',  # default file extensions (internally, it's still yaml)
    'config_folder_prefix': '.',
    'auto_save': True,
}


class uConfig(object):
    """
    A dict-like object that supports accessing keys via attributes,
    automatically saves its contents to a config file defined by
    app_name and config_name, automatically creates the config file
    if it doesn't exist, and populates it with the default dictionary
    provided.
    """

    def __init__(self, app_name, config_name, default):
        assert isinstance(app_name, str)
        assert isinstance(config_name, str)
        assert isinstance(default, dict)

        self._app_name = app_name
        self._config_name = config_name
        self._default_config = default
        self._config = {}
        self._config = self._get_or_create_config(default)

    def __getattribute__(self, item):
        if item.startswith('_'):
            return object.__getattribute__(self, item)
        return self._config.get(item)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
            return
        self._config[key] = value
        self._auto_save()

    def __getitem__(self, item):
        return self._config.get(item)

    def __setitem__(self, key, value):
        self._config[key] = value
        self._auto_save()

    def __iter__(self):
        for key, value in self._config.items():
            yield key, value

    def _update(self, dictionary):
        assert isinstance(self._config, dict)
        assert isinstance(dictionary, dict)
        self._config.update(dictionary)
        self._auto_save()

    def _exists(self, key):
        return key in self._config

    def _changed(self, key):
        return self._default_config.get(key) != self._config.get(key)

    def _reset(self):
        self._config = self._default_config
        self._auto_save()

    def _get_or_create_config(self, default_config):
        assert isinstance(default_config, dict)

        base_path = Path(os.path.expanduser(defaults['config_root']))
        app_path = base_path.joinpath(defaults['config_folder_prefix'] + self._app_name)
        config_path = app_path.joinpath(self._config_name + defaults['config_extension'])
        self._config_path = config_path

        if not (app_path.exists() and app_path.is_dir()):
            app_path.mkdir()

        if not config_path.exists():
            with config_path.open('w') as config_file:
                yaml.dump(default_config, config_file)

        with config_path.open('r') as config_file:
            return yaml.load(config_file)

    def _save(self):
        with self._config_path.open('w') as config_file:
            yaml.dump(self._config, config_file,
                      explicit_start=False,
                      default_flow_style=False)

    def _auto_save(self):
        if defaults['auto_save']:
            self._save()

    def _wizard(self, func, help_text=None):
        assert callable(func)
        assert isinstance(help_text, dict)

        sig = inspect.signature(func)
        args_required = [v.name for p, v in sig.parameters.items() if isinstance(v.default, type)]
        args_optional = [(v.name, v.default) for p, v in sig.parameters.items() if isinstance(v.default, type)]
        config = {}

        def print_help(name):
            if help_text and help_text.get(name):
                print(help_text[name])

        for name in args_required:
            print_help(name)
            value = input('Required: {name}:'.format(name=name))
            if value:
                config.update({name: value})

        for name, value in args_optional:
            print_help(name)
            newvalue = input('Optional: {name} (default: {value}):'.format(name=name, value=repr(value)))
            if newvalue:
                config.update({name: newvalue})
            else:
                config.update({name: value})

        return config
