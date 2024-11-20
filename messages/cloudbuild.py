# messages/cloudbuild.py
from typing import Literal, Optional
from .base import BaseSlackMessage


class CloudBuildMessage(BaseSlackMessage):
    def __init__(self, webhook_url: str):
        super().__init__(webhook_url)
        self.dashboard_url = "https://lookerstudio.google.com/reporting/03d3cf06-feec-4804-90cf-4e02f4014608/page/6A7FE/edit"
        self.status_emoji = {
            "SUCCESS": "🟢",
            "FAILURE": "🔴",
            "TIMEOUT": "⚠️",
            "CANCELLED": "⚫",
        }

    def _get_build_urls(
        self, region: str, build_id: str, project_id: str
    ) -> tuple[str, str]:
        """Get Cloud Build URLs"""
        base_url = f"https://console.cloud.google.com/cloud-build/builds;region={region}/{build_id}"
        build_url = f"{base_url}?project={project_id}"
        logs_url = f"{base_url}/logs?project={project_id}"
        return build_url, logs_url

    def create_message(
        self,
        project_id: str,
        repository_name: str,
        image_name: str,
        region: str,
        short_sha: str,
        build_id: str,
        status: Literal["SUCCESS", "FAILURE", "TIMEOUT", "CANCELLED"] = "SUCCESS",
        trigger_name: Optional[str] = None,
        error_logs: Optional[str] = None,
    ) -> None:
        """Create and send Cloud Build notification"""
        build_url, logs_url = self._get_build_urls(region, build_id, project_id)
        image_url = f"{region}-docker.pkg.dev/{project_id}/{repository_name}/{image_name}:{short_sha}"

        base_message = (
            f"{self.status_emoji.get(status, '❓')} Cloud Build `{repository_name}` {status}\n\n"
            f"*Project ID:* `{project_id}`\n"
            f"*Repository:* `{repository_name}`\n"
            f"*Build ID:* `{build_id}`\n"
            f"*Trigger:* `{trigger_name or 'Manual'}`\n"
            f"*Date:* `{self._get_current_time()}`\n"
        )

        if status == "SUCCESS":
            base_message += f"*Image:* `{image_url}`\n"

        if status in ["FAILURE", "TIMEOUT"] and error_logs:
            base_message += f"\n*Error Logs:*\n```{error_logs}```\n"

        base_message += (
            f"*Dashboard:* <{self.dashboard_url}|iWay Looker Dashboard>\n"
            f"<{build_url}|See Build Details> | <{logs_url}|View Logs>\n\n"
        )

        self.send({"text": base_message})
