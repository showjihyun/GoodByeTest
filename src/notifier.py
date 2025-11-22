import requests
import json

class SlackNotifier:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url

    def send_notification(self, message, status="info"):
        """
        Sends a message to Slack.
        status: info, success, error (determines color)
        """
        if not self.webhook_url:
            print("Slack Notifier: No Webhook URL provided. Skipping.")
            return

        color = "#36a64f" # green
        if status == "error":
            color = "#ff0000" # red
        elif status == "warning":
            color = "#ffcc00" # yellow

        payload = {
            "attachments": [
                {
                    "color": color,
                    "text": message,
                    "mrkdwn_in": ["text"]
                }
            ]
        }

        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code != 200:
                print(f"Slack Notification Failed: {response.status_code} - {response.text}")
            else:
                print("Slack Notification Sent.")
        except Exception as e:
            print(f"Slack Notification Error: {e}")
