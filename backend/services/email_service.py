"""Email notification service for ATL Pubnix."""

import os
from email.message import EmailMessage
from typing import Optional

import aiosmtplib
from jinja2 import Environment, FileSystemLoader

from models import Application, ApplicationStatus


class EmailService:
    """Service for sending email notifications."""

    def __init__(self):
        self.is_dev = os.getenv("PUBNIX_ENV", "development").lower() != "production"
        self.smtp_host = os.getenv("SMTP_HOST", "localhost")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        self.from_email = os.getenv("FROM_EMAIL", "noreply@atl.sh")
        self.from_name = os.getenv("FROM_NAME", "ATL Pubnix")

        # Setup Jinja2 for email templates
        template_dir = os.path.join(
            os.path.dirname(__file__), "..", "templates", "email"
        )
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """Send an email using SMTP."""
        # In development environments, do not attempt to send; just log and succeed
        if self.is_dev:
            print(f"[dev-email] To: {to_email} | Subject: {subject}")
            return True

        try:
            message = EmailMessage()
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email
            message["Subject"] = subject

            if text_content:
                message.set_content(text_content)

            if html_content:
                message.add_alternative(html_content, subtype="html")

            # Send email
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_username,
                password=self.smtp_password,
                use_tls=self.smtp_use_tls,
            )

            return True

        except Exception as e:
            # Log error in production
            print(f"Failed to send email to {to_email}: {e}")
            return False

    async def send_application_confirmation(self, application: Application) -> bool:
        """Send confirmation email for new application."""
        try:
            template = self.jinja_env.get_template("application_confirmation.html")
            html_content = template.render(
                full_name=application.full_name,
                username_requested=application.username_requested,
                application_id=application.id,
            )

            subject = "ATL Pubnix - Application Received"

            return await self.send_email(
                to_email=application.email,
                subject=subject,
                html_content=html_content,
            )

        except Exception as e:
            print(f"Failed to send application confirmation: {e}")
            return False

    async def send_application_status_update(self, application: Application) -> bool:
        """Send email notification for application status update."""
        try:
            if application.status == ApplicationStatus.APPROVED:
                template_name = "application_approved.html"
                subject = "ATL Pubnix - Application Approved!"
            elif application.status == ApplicationStatus.REJECTED:
                template_name = "application_rejected.html"
                subject = "ATL Pubnix - Application Update"
            else:
                return False  # No email for other statuses

            template = self.jinja_env.get_template(template_name)
            html_content = template.render(
                full_name=application.full_name,
                username_requested=application.username_requested,
                review_notes=application.review_notes,
                application_id=application.id,
            )

            return await self.send_email(
                to_email=application.email,
                subject=subject,
                html_content=html_content,
            )

        except Exception as e:
            print(f"Failed to send application status update: {e}")
            return False
