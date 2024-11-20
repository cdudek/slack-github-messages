# messages/github.py
from typing import Optional
from .base import BaseSlackMessage


class GitHubActionMessage(BaseSlackMessage):
    def create_message(
        self,
        repository: str,
        action_name: str,
        repository_url: str,
        branch: str,
        actor: str,
        commit_sha: str,
        event_name: str,
        run_id: str,
        status: str = "Success",
    ) -> None:
        """Create and send GitHub Action notification"""
        message = (
            f"🟢 GitHub `{repository}` Action `{action_name}` {status}\n\n"
            f"*Repository:* *<{repository_url}|{repository}>*\n"
            f"*Branch:* `{branch}`\n"
            f"*Action:* `{action_name}`\n"
            f"*Triggered by:* <https://github.com/{actor}|@{actor}>\n"
            f"*Commit:* <{repository_url}/commit/{commit_sha}|{commit_sha[:7]}>\n"
            f"*Event:* `{event_name}`\n"
            f"*Date:* `{self._get_current_time()}`\n"
            f"*Dashboard:* <https://lookerstudio.google.com/reporting/03d3cf06-feec-4804-90cf-4e02f4014608/page/6A7FE/edit|iWay Looker Dashboard>\n"
            f"<{repository_url}/actions/runs/{run_id}|See Details>\n\n"
        )

        self.send({"text": message})
