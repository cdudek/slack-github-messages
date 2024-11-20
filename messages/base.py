# messages/base.py
from typing import Dict, Any
import requests
from datetime import datetime


class BaseSlackMessage:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, message: Dict[str, Any]) -> None:
        """Send message to Slack webhook"""
        response = requests.post(
            self.webhook_url, json=message, headers={"Content-Type": "application/json"}
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to send Slack message: {response.status_code} - {response.text}"
            )

    def _get_current_time(self) -> str:
        """Get formatted current time"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
