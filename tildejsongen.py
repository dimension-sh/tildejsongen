#!/usr/bin/env python3

import os
import sys
import re
import pwd
import datetime
import logging
from configparser import ConfigParser

CONFIG_LOCATIONS = [
    '/etc/tildejsongen.ini',
    '/usr/local/etc/tildejsongen.ini',
]

CONFIG_DEFAULTS = {
    'paths': {
        'public_html': 'public_html',
        'hidden_file': '.hidden',
        'index_file': 'index.html',
    },
    'users': {
        'group_id': 100,
    }
}


def get_config(filename=None):
    """Identify the config file to use and load it"""
    if filename:
        return read_config(filename)
    for file in CONFIG_LOCATIONS:
        if os.path.exists(file):
            return read_config(file)


def read_config(filename):
    """Read a config file and produce a ConfigParser object"""
    cfg = ConfigParser()
    cfg.read_dict(CONFIG_DEFAULTS)
    cfg.read(filename)
    return cfg


def get_title(filename):
    """Locate the first title in a HTML document"""
    with open(filename, 'r') as fobj:
        data = fobj.read()
    res = re.search(r'<title>(.*?)</title>', data)
    try:
        if res:
            return res.group(1)
        return '~somebody'
    except (IndexError, AttributeError):
        logging.debug(f'No HTML title found in {filename}')
        pass


def get_users(config):
    """Returns a dict of the current visible users and their tilde.json data"""
    # Get the values of the file locations
    public_html_path = config.get('paths', 'public_html')
    hidden_file = config.get('paths', 'hidden_file')
    index_file = config.get('paths', 'index_file')
    group_id = config.getint('users', 'group_id')

    # Generate array of user information
    users = []
    for user in sorted(pwd.getpwall(), key=lambda x: x.pw_name):
        logging.debug(f'Processing {user.pw_name}')

        # Skip users not in the primary group ID
        if user.pw_gid != group_id:
            continue

        # if the user doesn't have a public_html folder, skip
        if not os.path.exists(os.path.join(user.pw_dir, public_html_path)):
            logging.debug(f'Skipping {user.pw_name} as public_html is missing')
            continue

        # if .hidden exists in the public_html, skip it
        if os.path.exists(os.path.join(user.pw_dir, public_html_path, hidden_file)):
            logging.debug(f'Skipping {user.pw_name} as the user is marked as hidden')
            continue

        index_file_path = os.path.join(user.pw_dir, public_html_path, index_file)
        if os.path.exists(index_file_path):
            title = get_title(index_file_path)
            mtime = os.path.getmtime(index_file_path)
        else:
            logging.debug(f'Index is missing for {user.pw_name}')
            title = None
            mtime = 0

        users.append({
            'username': user.pw_name,
            'title': title,
            'mtime': int(mtime),
        })
    return users


def generate_json(config, data):
    """Generate out a JSON format document"""
    import json
    return json.dumps(data)


def generate_yaml(config, data):
    """Generate out a YAML format document"""
    import yaml
    return yaml.dump(data)


def generate_text(config, data):
    """Generate out a Text format document"""
    import jinja2
    template = config.get('jinja2', 'template')
    with open(template, 'r') as fobj:
        return jinja2.Template(fobj.read()).render(data=data)


def main():
    # TODO: Argparse
    logging.basicConfig(level=logging.WARNING)
    cfg = get_config()

    # Generate data Dict
    data = dict(cfg.items(section='info'))
    users = get_users(cfg)
    data.update({
        'users': users,
        'user_count': len(users),
        'last_generated': str(datetime.datetime.utcnow()),
    })

    for output_data in cfg.items('output'):
        format, output_file = output_data
        if f'generate_{format}' in globals():
            logging.info(f'Rendering {format} to {output_file}')
            try:
                rendered_output = globals()[f'generate_{format}'](cfg, data)
            except Exception:
                logging.exception(f'Something went wrong rendering {format}')
                continue
            with open(output_file, 'w') as fobj:
                fobj.write(rendered_output)


if __name__ == '__main__':
    main()
