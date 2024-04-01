# tildejsongen

<img src="https://img.shields.io/liberapay/receives/dimension.sh.svg?logo=liberapay">

A simple Python script to generate a [Tilde Description Protocol](http://protocol.club/~datagrok/beta-wiki/tdp.html) a.k.a. `tilde.json` file for Tilde-style servers.

## Installation

`tildejsongen` is a standard Python package that can be installed using Poetry.

It requires the following packages:

* `pyyaml`
* `jinja2`

## Usage

By default, `tildejsongen` will look in the following location for a configuration file:

* `/etc/tildejsongen.ini`
* `/usr/local/etc/tildejsongen.ini`

A sample configuration file can be found in [`config-example.ini`](config-example.ini):

```ini
[info]
name = dimension.sh
url = https://dimension.sh
signup_url = https://dimension.sh/join.html
want_users = true
admin_email = hostmaster@dimension.sh
description = dimension.sh is a small public linux shell host (or pubnix system) that is open to anyone who wants to learn, experiment, and socialize with other like minded people.

[paths]
public_html = public_html
hidden_file = .hidden
index_file = index.html

[users]
group_id = 100

[output]
json = /var/www/dimension.sh/tilde.json
yaml = /var/www/dimension.sh/tilde.yaml
```

### Info Section

| Value         | Description                                                     |
| ------------- | --------------------------------------------------------------- |
| `name`        | Name of the pubnix/tilde                                        |
| `url`         | Website URL for the pubnix/tilde                                |
| `signup_url`  | The URL where new users can sign up                             |
| `want_users`  | A boolean indicating if the pubnix/tilde is accepting new users |
| `admin_email` | Email address of the admin                                      |
| `description` | Long description of the pubnix                                  |

### Paths Section

| Value         | Description                                                                            |
| ------------- | -------------------------------------------------------------------------------------- |
| `public_html` | The folder name of the `public_html` folder for each user                              |
| `hidden_file` | The file the user can create in their home directory to be excluded from the user list |
| `index_file`  | The name of the file in the `public_html` to get the last modified date from           |

### Users Section

| Value      | Description                                                        |
| ---------- | ------------------------------------------------------------------ |
| `group_id` | The GID of the user group to identify users from for the user list |

### Output Section

| Value  | Description                                 |
| ------ | ------------------------------------------- |
| `json` | Where to write the JSON formatted output to |
| `yaml` | Where to write the YAML formatted output    |

## Similar Projects

* [William Jackson's original Python generator](https://github.com/williamjacksn/tilde-description-protocol)
* [instistats](https://github.com/tildeinstitute/instistats) - tilde.institute's stats generator