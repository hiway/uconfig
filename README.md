# uconfig

Minimalist configuration manager

## Usage

    import uconfig

    tldr = uconfig.uConfig('example', 'tldr', {})  # ~/.example/tldr.yaml
    tldr.save_to_any_key = 'Your config file gets updated automatically.'

    tldr.access_any_key  # Missing keys will return None
    tldr._exists('a_missing_key')  # You can check explicitly

    # More

    config = uconfig.uConfig(
        app_name='example',  # creates ~/.app_name folder
        config_name='base',  # created ~/.app_name/config_name.yaml file
        default={
            'aws_key': 'PASTE_AWS_KEY_HERE',  # Lets you create a default configuration
            'aws_key_secret': 'PASTE_AWS_KEY_SECRET_HERE',  # with hints for users
        })

    # Bulk update keys
    config._update({'aws_key': 'a new value', 'aws_key_secret': 'another new value'})

    # Returns True is user has overridden the default value
    config._changed('aws_key')

    # Every time you assign to uConfig, the config file is updated transparently
    # Also, you can save Python objects that can be serialized by PyYAML
    config.twitter_config = {
        'oauth_token':'',
        'oauth_secret': '',
    }

    # Reset configuration and go back to default set here => uconfig.uConfig(app, conf, default={})
    config._reset()
