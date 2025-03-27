import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import config
import logging
import time
from typing import Optional
import re
import pdfkit
import os
from config import (
    SMTP_SERVER, SMTP_PORT, EMAIL_USERNAME, EMAIL_PASSWORD,
    EMAIL_SUBJECT, EMAIL_BODY_TEXT, EMAIL_BODY_HTML
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_sender.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.username = EMAIL_USERNAME
        self.password = EMAIL_PASSWORD
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        self.pdf_output_dir = os.path.join(config.DATA_DIR, 'generated_pdfs')
        os.makedirs(self.pdf_output_dir, exist_ok=True)
        
        # Configure wkhtmltopdf path
        self.wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        if not os.path.exists(self.wkhtmltopdf_path):
            logger.error(f"wkhtmltopdf not found at {self.wkhtmltopdf_path}")
            logger.error("Please install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html")
            raise FileNotFoundError(f"wkhtmltopdf not found at {self.wkhtmltopdf_path}")

    def _validate_email(self, email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if email is valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            logging.error(f"Invalid email format: {email}")
            return False
        return True

    def validate_email_config(self) -> bool:
        """Validate email configuration settings."""
        try:
            # Check if all required settings are present
            if not all([self.smtp_server, self.smtp_port, self.username, self.password]):
                logger.error("Missing required email configuration settings")
                return False

            # Validate email format
            if '@' not in self.username or '.' not in self.username:
                logger.error(f"Invalid email format: {self.username}")
                return False

            # Test SMTP connection
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                logger.info("Email configuration validation successful")
                return True

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"Email authentication failed: {str(e)}")
            logger.error("Please check your email and app password")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during email validation: {str(e)}")
            return False

    def _generate_pdf(self, offer_letter_content, candidate_name):
        """Generate PDF from offer letter content."""
        try:
            # Create a temporary HTML file
            temp_html = f'temp_offer_letter_{candidate_name}.html'
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(offer_letter_content)

            # Configure PDF options
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': 'UTF-8',
                'no-outline': None,
                'enable-local-file-access': None,
                'quiet': ''
            }

            # Generate PDF using the configured wkhtmltopdf path
            config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path)
            pdf_content = pdfkit.from_file(temp_html, False, options=options, configuration=config)

            # Clean up temporary file
            os.remove(temp_html)

            return pdf_content
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            raise

    def _create_message(self, to_email, candidate_name, position, offer_letter_content):
        """Create email message with both HTML and PDF attachments."""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = self.username
        msg['To'] = to_email

        # Add plain text version
        text_content = EMAIL_BODY_TEXT.format(
            candidate_name=candidate_name,
            position=position,
            company_name="Your Company Name"
        )
        msg.attach(MIMEText(text_content, 'plain'))

        # Add HTML version
        html_content = EMAIL_BODY_HTML.format(
            candidate_name=candidate_name,
            position=position,
            company_name="Your Company Name",
            offer_letter_content=offer_letter_content
        )
        msg.attach(MIMEText(html_content, 'html'))

        # Generate PDF
        pdf_content = self._generate_pdf(offer_letter_content, candidate_name)
        
        # Attach PDF
        pdf_attachment = MIMEApplication(pdf_content, _subtype='pdf')
        pdf_attachment.add_header(
            'Content-Disposition', 
            'attachment', 
            filename=f'offer_letter_{candidate_name}.pdf'
        )
        msg.attach(pdf_attachment)

        return msg

    def send_email(self, to_email, candidate_name, position, offer_letter_content):
        """Send email with retry logic."""
        for attempt in range(self.max_retries):
            try:
                msg = self._create_message(to_email, candidate_name, position, offer_letter_content)
                
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.username, self.password)
                    server.send_message(msg)
                
                logger.info(f"Email sent successfully to {to_email}")
                return True
                
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"Failed to send email after {self.max_retries} attempts")
                    raise 