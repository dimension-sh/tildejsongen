#!/usr/bin/env python3

import datetime
import json
import logging
import os
import pwd
import re
from configparser import ConfigParser

CONFIG_LOCATIONS = (
    '/etc/tildejsongen.ini',
    '/usr/local/etc/tildejsongen.ini',
)

CONFIG_DEFAULTS = {
    'paths': {
        'public_html': 'public_html',
        'hidden_file': '.hidden',
        'index_file': 'index.html',
    },
    'users': {
        'group_id': 100,
    },
}


def str2bool(value):
    return value.lower() in set('yes', 'true', 't', '1')


def get_config(filename=None):
    """Identify the config file to use and load it."""
    if filename:
        return read_config(filename)
    for config_path in CONFIG_LOCATIONS:
        if os.path.exists(config_path):
            return read_config(config_path)


def read_config(filename):
    """Read a config file and produce a ConfigParser object."""
    cfg = ConfigParser()
    cfg.read_dict(CONFIG_DEFAULTS)
    cfg.read(filename)
    return cfg


def get_title(filename):
    """Locate the first title in a HTML document."""
    with open(filename, 'r') as fobj:
        raw_html = fobj.read()
    res = re.search('<title>(.*?)</title>', raw_html)
    try:
        if res:
            return res.group(1)
        return '~somebody'
    except (IndexError, AttributeError):
        logging.debug('No HTML title found in {0}'.format(filename))
        pass


def get_users(config):
    """Returns a dict of the current visible users and their tilde.json data."""
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

        index_file_path = os.path.join(user.pw_dir, public_html_path, index_file)
        if os.path.exists(index_file_path):
            title = get_title(index_file_path)
            mtime = os.path.getmtime(index_file_path)
        else:
            logging.debug('Index is missing for {0}'.format(user.pw_name))
            title = None
            mtime = 0

        users.append({
            'username': user.pw_name,
            'title': title,
            'mtime': int(mtime),
        })
    return users


def generate_json(config, user_data):
    """Generate out a JSON format document"""
    return json.dumps(user_data)


def generate_yaml(config, user_data):
    """Generate out a YAML format document"""
    import yaml  # noqa: WPS433
    return yaml.dump(user_data)


def generate_text(config, user_data):
    """Generate out a Text format document"""
    import jinja2  # noqa: WPS433
    template = config.get('jinja2', 'template')
    with open(template, 'r') as fobj:
        return jinja2.Template(fobj.read()).render(data=user_data)


def main():
    # TODO: Argparse
    logging.basicConfig(level=logging.WARNING)
    cfg = get_config()

    # Generate data Dict
    info_data = dict(cfg.items(section='info'))

    # Ensure 'want_users' is a bool, if it set
    if 'want_users' in info_data:
        info_data['want_users'] = str2bool(info_data['want_users'])

    users = get_users(cfg)
    info_data.update({
        'users': users,
        'user_count': len(users),
        'last_generated': str(datetime.datetime.utcnow()),
    })

    for output_data in cfg.items('output'):
        format_name, output_file = output_data
        if 'generate_{0}'.format(format_name) in globals():
            logging.info('Rendering {0} to {1}'.format(format_name, output_file))
            try:
                rendered_output = globals()['generate_{0}'.format(format_name)](cfg, info_data)
            except Exception:
                logging.exception('Something went wrong rendering {0}'.format(format_name))
                continue
            with open(output_file, 'w') as fobj:
                fobj.write(rendered_output)


if __name__ == '__main__':
    main()
