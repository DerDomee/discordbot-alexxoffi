<h3 align="center">AlexxBot</h3>
<p align="center">
  This self-hosted discord bot can auto-moderate, run guild-specific commands and show fancy statistics.
  <br>
  <a href="https://discord.com/invite/yq8zGWy">Join the Discord</a>
  <br>
  <br>
  <a href="https://github.com/derdomee/discordbot-alexxoffi/issues/new?template=bug_report.md">Report bug</a>
  ·
  <a href="https://github.com/derdomee/discordbot-alexxoffi/issues/new?template=feature_request.md">Request feature</a>
  ·
  <a href="https://dominikriedig.de">Visit Author</a>
</p>

# This has been discontinued!
The bot is no longer in development.

## Table of contents

- [Prerequisites](#prerequisites)
- [Quick start](#quick-start)
- [Contributing](#contributing)

## Prerequisites

Following programs and scripts are required to run this bot:
- Python `>3.7,<=3.8`
- Pip `>=18.1`
- Pipenv `>=v2020.6.2` (`pip install pipenv`)

## Quick start

1. Create your bot application at https://discord.com/developers/ and follow all steps to create a bot and invite it to your server
  1. Please note that this bot requires the "Server Members Intent" option or multiple features of this bot will break.
  2. As some statistic-tracking will likely be implemented in the near future, it is recommended to enable the "Presence Intent" option.
  2. It is recommended not to enable the "Public Bot" setting
2. Clone this repository `git clone https://github.com/derdomee/discordbot-alexxoffi.git`
3. Create a file `.env` from `.env.preset` and insert your settings, most importantly your discord bot token
4. Install the virtual environment: `pipenv sync`
5. Run the bot with `pipenv run start` (Or translate and run manually: `pipenv run translate && pipenv run bot`)

## Running with different python versions

This bot is developed and tested in Python 3.7 only, but it should run flawlessly in Python `>=3.6`. Pipenv forces a single pinned python version as application requirement, thus I can not provide a wider version range for it. Just remove the python requirement in `Pipfile` or change the value to your desired python version.
## Contributing

Feel free to fork this project and create a pull request containing your changes.
