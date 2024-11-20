# cli/cloudbuild_complete.py
import os
from messages.cloudbuild import CloudBuildMessage


def main():
    """CLI entry point for Cloud Build completion notifications"""
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    project_id = os.environ["PROJECT_ID"]  # Changed from PROJECT_ID
    repository_name = os.environ["_REPOSITORY_NAME"]
    image_name = os.environ["_IMAGE_NAME"]
    region = os.environ["_REGION"]
    short_sha = os.environ["SHORT_SHA"]
    build_id = os.environ["BUILD_ID"]
    status = os.environ.get("STATUS", "SUCCESS")
    trigger_name = os.environ.get("TRIGGER_NAME")

    # Get error logs if build failed
    error_logs = None
    if status != "SUCCESS":
        error_logs = "Build failed. Check logs for details."

    message = CloudBuildMessage(webhook_url)
    message.create_message(
        project_id=project_id,
        repository_name=repository_name,
        image_name=image_name,
        region=region,
        short_sha=short_sha,
        build_id=build_id,
        status=status,
        trigger_name=trigger_name,
        error_logs=error_logs,
    )


if __name__ == "__main__":
    main()
