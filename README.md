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

## Alpha Stage

This bot is currently in the alpha stage, with lots of changes proposed. While in alpha, most development is done on master branch only, except when there are changes coming from forks. When leaving alpha, a full repository refactor will take place, creating, renaming and moving various branches and other refs.

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
2. Clone this repository `git clone https://github.com/derdomee/discordbot-alexxoffi.git`
3. Create a file `.env` from `.env.preset` and insert your settings, most importantly your discord bot token
4. Install the virtual environment: `pipenv install`
5. Run the bot with `pipenv run bot`

## Contributing

Feel free to fork this project and create a pull request containing your changes.
