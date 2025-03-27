import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email Configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_SUBJECT = "Your Offer Letter"

# Company Information
COMPANY_NAME = "Your Company Name"
COMPANY_ADDRESS = "123 Business Street, Suite 100, City, State 12345"
COMPANY_WEBSITE = "www.yourcompany.com"

# File Paths
TEMPLATE_DIR = "templates"
DATA_DIR = "data"
CANDIDATES_FILE = os.path.join(DATA_DIR, "candidates.csv")

# Email Templates
EMAIL_BODY_TEXT = """
Dear {candidate_name},

We are pleased to offer you the position of {position} at {company_name}.

Please find your offer letter attached to this email.

Best regards,
{company_name} HR Team
"""

EMAIL_BODY_HTML = """
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Calibri', Arial, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #3498db;
        }}
        .content-section {{
            background-color: #f8f9fa;
            padding: 25px;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
        }}
        #offer-letter-content {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h2>Welcome to {company_name}!</h2>
        <p>Dear {candidate_name},</p>
    </div>

    <p>We are pleased to offer you the position of <strong>{position}</strong> at {company_name}.</p>

    <div class="content-section">
        <h3>Your Offer Letter</h3>
        <p>You can access your offer letter in multiple ways:</p>
        <ol>
            <li>View the offer letter in the email body below</li>
            <li>Download the PDF version attached to this email</li>
            <li>Print the offer letter directly from your browser</li>
        </ol>
    </div>

    <div id="offer-letter-content">
        <h2>Your Offer Letter</h2>
        {offer_letter_content}
    </div>

    <div class="footer">
        <p>Best regards,<br>{company_name} HR Team</p>
    </div>
</body>
</html>
"""

# File naming configuration
FILE_NAME_PREFIX = "offer_letter"
FILE_NAME_SEPARATOR = "_" 