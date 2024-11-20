# cli/cloudbuild_start.py
import os
from messages.cloudbuild import CloudBuildMessage


def main():
    """CLI entry point for Cloud Build start notifications"""
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    project_id = os.environ["PROJECT_ID"]
    repository_name = os.environ["_REPOSITORY_NAME"]
    region = os.environ["_REGION"]
    build_id = os.environ["BUILD_ID"]
    trigger_name = os.environ.get("TRIGGER_NAME")

    message = CloudBuildMessage(webhook_url)
    message.create_start_message(
        project_id=project_id,
        repository_name=repository_name,
        region=region,
        build_id=build_id,
        trigger_name=trigger_name,
    )


if __name__ == "__main__":
    main()
