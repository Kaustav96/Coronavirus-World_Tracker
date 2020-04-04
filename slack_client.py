import requests
import json
from auth import DEFAULT_SLACK_WEBHOOK

HEADERS = {
    'Content-type': 'application/json'
}
file_path = 'corona_country_data.csv'

def slacker(webhook_url=DEFAULT_SLACK_WEBHOOK):
    def slackit(msg):
        payload = {'text': msg}

        return requests.post(webhook_url, headers=HEADERS, data=json.dumps(payload))
    return slackit


def slacker_file():
    def slackerfile():
        with open(file_path, 'rb') as f:
            payload = {"filename": file_path,
                       "token": YOUR_SLACK_TOKEN,
                       "channels": "coronavirus-world"}
            requests.post("https://slack.com/api/files.upload", params=payload, files={'file': f})

    return slackerfile()

# xoxp-1004629925682-1005947718707-1013237996563-85c053b2c268b1af84ab6ed097003294