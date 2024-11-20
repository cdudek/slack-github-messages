# messages/cloudbuild.py
from typing import Literal, Optional
from .base import BaseSlackMessage


class CloudBuildMessage(BaseSlackMessage):
    def __init__(self, webhook_url: str):
        super().__init__(webhook_url)
        self.cloudbuild_url = "https://console.cloud.google.com/cloud-build"
        self.status_emoji = {
            "SUCCESS": "🟢",
            "FAILURE": "🔴",
            "TIMEOUT": "⚠️",
            "CANCELLED": "⚫",
            "STARTED": "🔵",
        }

    def _get_build_urls(
        self, region: str, build_id: str, project_id: str
    ) -> tuple[str, str, str]:
        """Get Cloud Build URLs"""
        # Updated URL structure to match actual Cloud Build URLs
        builds_url = (
            f"{self.cloudbuild_url}?project={project_id}"  # Main Cloud Build page
        )
        build_url = f"{self.cloudbuild_url}/builds;region={region}/{build_id}?project={project_id}"
        logs_url = (
            f"{build_url}&page=logs"  # Changed to use the build URL as base for logs
        )

        return build_url, logs_url, builds_url

    def create_start_message(
        self,
        project_id: str,
        repository_name: str,
        region: str,
        build_id: str,
        trigger_name: Optional[str] = None,
    ) -> None:
        """Create and send Cloud Build start notification"""
        build_url, logs_url, builds_url = self._get_build_urls(
            region, build_id, project_id
        )

        message = (
            f"{self.status_emoji['STARTED']} Cloud Build `{repository_name}` Started\n\n"
            f"*Project ID:* `{project_id}`\n"
            f"*Repository:* `{repository_name}`\n"
            f"*Build ID:* `{build_id}`\n"
            f"*Trigger:* `{trigger_name or 'Manual'}`\n"
            f"*Date:* `{self._get_current_time()}`\n"
            f"*Cloud Build:* <{builds_url}|All Builds>\n"
            f"<{build_url}|See Build Details> | <{logs_url}|View Logs>\n\n"
        )

        self.send({"text": message})

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
        """Create and send Cloud Build completion notification"""
        build_url, logs_url, builds_url = self._get_build_urls(
            region, build_id, project_id
        )
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
            f"*Cloud Build:* <{builds_url}|All Builds>\n"
            f"<{build_url}|See Build Details> | <{logs_url}|View Logs>\n\n"
        )

        self.send({"text": base_message})
