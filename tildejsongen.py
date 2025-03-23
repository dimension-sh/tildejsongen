#!/usr/bin/env python3
"""
tildejsongen.

A simple tool to generate a `tilde.json` file from a standard Linux shell
system.
"""

import datetime
import json
import logging
import os
import pwd
import re
import types
from configparser import ConfigParser

__version__ = '0.3.2'  # noqa: WPS410

CONFIG_LOCATIONS = (
    '/etc/tildejsongen.ini',
    '/usr/local/etc/tildejsongen.ini',
)

CONFIG_DEFAULTS = types.MappingProxyType({
    'paths': {
        'public_html': 'public_html',
        'hidden_file': '.hidden',
        'index_file': 'index.html',
    },
    'users': {
        'group_id': 100,
    },
})


def str2bool(string_value: str) -> bool:
    """Convert common string truthy values to a boolean."""
    return string_value.lower() in {'yes', 'true', 't', '1', 'on'}


def get_config(filename: str = None) -> ConfigParser:
    """Identify the config file to use and load it."""
    if filename:
        return read_config(filename)
    for config_path in CONFIG_LOCATIONS:
        if os.path.exists(config_path):
            return read_config(config_path)


def read_config(filename: str) -> ConfigParser:
    """Read a config file and produce a ConfigParser object."""
    cfg = ConfigParser()
    cfg.read_dict(CONFIG_DEFAULTS)
    cfg.read(filename)
    return cfg


def get_title(filename: str) -> str:
    """Locate the first title in a HTML document."""
    with open(filename, 'r') as index:
        raw_html = index.read()
    res = re.search('<title>(.*?)</title>', raw_html)
    if res and len(res.groups()):
        return res.group(1)
    return '~somebody'


def get_users(config: ConfigParser) -> list:
    """Return a dict of the current visible users and their tilde.json data."""
    # Get the values of the file locations
    public_html_path = config.get('paths', 'public_html')
    hidden_file = config.get('paths', 'hidden_file')
    index_file = config.get('paths', 'index_file')
    group_id = config.getint('users', 'group_id')

    # Generate array of user information
    users = []
    for user in sorted(pwd.getpwall(), key=lambda entry: entry.pw_name):
        logging.debug('Processing {0}'.format(user.pw_name))

        # Skip users not in the primary group ID
        if user.pw_gid != group_id:
            continue

        # if the user doesn't have a public_html folder, skip
        if not os.path.exists(os.path.join(user.pw_dir, public_html_path)):
            logging.debug('Skipping {0} as public_html is missing'.format(user.pw_name))
            continue

        # if .hidden exists in the public_html, skip it
        if os.path.exists(os.path.join(user.pw_dir, public_html_path, hidden_file)):
            logging.debug('Skipping {0} as the user is marked as hidden'.format(user.pw_name))
            continue

        # Get title and mtime from the user's index file.
        index_file_path = os.path.join(user.pw_dir, public_html_path, index_file)
        if os.path.exists(index_file_path):
            title = get_title(index_file_path)
            mtime = os.path.getmtime(index_file_path)
        else:
            logging.debug('Index is missing for {0}'.format(user.pw_name))
            title = None
            mtime = 0

        # Add the user to the user list
        users.append({
            'username': user.pw_name,
            'title': title,
            'mtime': int(mtime),
        })
    return users


def generate_json(config: dict, user_data: dict) -> str:
    """Generate out a JSON format document."""
    return json.dumps(user_data)


def generate_yaml(config: dict, user_data: dict) -> str:
    """Generate out a YAML format document."""
    import yaml  # noqa: WPS433
    return yaml.dump(user_data)


def generate_text(config: dict, user_data: dict) -> str:
    """Generate out a Text format document."""
    import jinja2  # noqa: WPS433
    template = config.get('jinja2', 'template')
    with open(template, 'r') as template_file:
        return jinja2.Template(template_file.read()).render(data=user_data)


def main():  # noqa: WPS421
    """Run tildejsongen."""
    # TODO: Argparse
    logging.basicConfig(level=logging.WARNING)
    cfg = get_config()

    # Generate data Dict
    info_data = dict(cfg.items(section='info'))

    # Ensure 'want_users' is a bool, if it set
    want_users = info_data.get('want_users')
    if want_users:
        info_data['want_users'] = str2bool(want_users)

    users = get_users(cfg)
    info_data.update({
        'users': users,
        'user_count': len(users),
        'last_generated': str(datetime.datetime.utcnow()),
    })

    for output_data in cfg.items('output'):
        format_name, output_file = output_data
        format_func = globals().get('generate_{0}'.format(format_name))  # noqa: WPS421
        if format_func:
            logging.info('Rendering {0} to {1}'.format(format_name, output_file))
            try:
                rendered_output = format_func(cfg, info_data)
            except Exception:
                logging.exception('Something went wrong rendering {0}'.format(format_name))
                continue
            with open(output_file, 'w') as output:
                output.write(rendered_output)


if __name__ == '__main__':
    main()
