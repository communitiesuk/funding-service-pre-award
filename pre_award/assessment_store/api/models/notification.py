import json
from uuid import uuid4

from flask import current_app

from config import Config

NOTIFICATION_CONST = "notification"
NOTIFICATION_S3_KEY_CONST = "application/notification"


class Notification:
    """Class for holding Notification operations."""

    @staticmethod
    def send(template_type: str, to_email: str, full_name: str, content: dict):
        """Sends a notification using the Gov.UK Notify Service.

        Args:
            template_type: (str) A key of the template to use in the
                DLUHC notifications service (which maps to a
                Notify Service template key)
            to_email: (str) The email to send the notification to
            content: (dict) A dictionary of content to send to
                fill out the notification template

        """
        json_payload = {
            "type": template_type,
            "to": to_email,
            "full_name": full_name,
            "content": content,
        }
        current_app.logger.info(
            " json payload '%(template_type)s' to '%(to_email)s'.",
            dict(template_type=template_type, to_email=to_email),
        )
        try:
            sqs_extended_client = Notification._get_sqs_client()
            message_id = sqs_extended_client.submit_single_message(
                queue_url=Config.AWS_SQS_NOTIF_APP_PRIMARY_QUEUE_URL,
                message=json.dumps(json_payload),
                message_group_id=NOTIFICATION_CONST,
                message_deduplication_id=str(uuid4()),  # ensures message uniqueness
                extra_attributes={
                    "S3Key": {
                        "StringValue": NOTIFICATION_S3_KEY_CONST,
                        "DataType": "String",
                    },
                },
            )
            current_app.logger.info(
                "Message sent to SQS queue and message id is [%(message_id)s]", dict(message_id=message_id)
            )
            return message_id
        except Exception:
            current_app.logger.exception("An error occurred while sending message")

    @staticmethod
    def _get_sqs_client():
        sqs_extended_client = current_app.extensions["sqs_extended_client"]
        if sqs_extended_client is not None:
            return sqs_extended_client
        current_app.logger.error("An error occurred while sending message since client is not available")
