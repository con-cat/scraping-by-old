# Scraping By

A Slack app that lets us know when our favourite products are on special at a certain major supermarket chain.

## Local setup:

In a Python 3.8 virtual environment:

1. `pip install requirements.txt`
1. To connect to Slack:
    * Create a file named `.env` in the top level directory of the project
    * Get the Slack webhook URL for the app at api.slack.com when you're signed into the workspace scrapingby.slack.com. Click on "Your Apps", the name of the app, then "Incoming Webhooks".
    * Add a line in the file to set an environment variable with the Slack webhook URL: `SLACK_URL=URL goes here`.
1. Run the app locally: `python scraping-by/scraping-by.py`
