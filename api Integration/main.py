import os
import pandas as pd
from offer_generator import OfferGenerator
from email_sender import EmailSender
import logging
from config import (
    CANDIDATES_FILE, COMPANY_NAME, COMPANY_ADDRESS, COMPANY_WEBSITE,
    TEMPLATE_DIR, DATA_DIR, EMAIL_USERNAME
)

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('offer_letter_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def validate_candidate_data(df):
    """Validate candidate data from CSV file."""
    try:
        logger.info("Starting data validation...")
        required_columns = ['name', 'email', 'position', 'salary']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            raise ValueError(f"Missing required columns in CSV: {', '.join(missing_columns)}")
        
        logger.info("Converting columns to string type for validation...")
        # Convert columns to string type for validation
        df['email'] = df['email'].astype(str)
        df['salary'] = df['salary'].astype(str)
        
        # Validate email format
        logger.info("Validating email formats...")
        invalid_emails = df[~df['email'].str.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')]
        if not invalid_emails.empty:
            logger.error(f"Invalid emails found: {invalid_emails['name'].tolist()}")
            raise ValueError(f"Invalid email format for candidates: {', '.join(invalid_emails['name'])}")
        
        # Validate salary format
        logger.info("Validating salary formats...")
        invalid_salaries = df[~df['salary'].str.match(r'^\d+$')]
        if not invalid_salaries.empty:
            logger.error(f"Invalid salaries found: {invalid_salaries['name'].tolist()}")
            raise ValueError(f"Invalid salary format for candidates: {', '.join(invalid_salaries['name'])}")
        
        # Convert salary to float for processing
        logger.info("Converting salaries to float...")
        df['salary'] = df['salary'].astype(float)
        
        logger.info("Data validation completed successfully")
        return df
        
    except Exception as e:
        logger.error(f"Error validating candidate data: {str(e)}")
        raise

def process_candidates():
    """Process candidates and generate offer letters."""
    try:
        # Read candidate data
        logger.info(f"Reading candidate data from {CANDIDATES_FILE}")
        if not os.path.exists(CANDIDATES_FILE):
            logger.error(f"File not found: {CANDIDATES_FILE}")
            raise FileNotFoundError(f"Candidates file not found: {CANDIDATES_FILE}")
            
        df = pd.read_csv(CANDIDATES_FILE)
        logger.info(f"Found {len(df)} candidates in the CSV file")
        
        df = validate_candidate_data(df)  # Get the validated DataFrame back
        
        # Initialize offer generator and email sender
        logger.info("Initializing offer generator and email sender...")
        offer_generator = OfferGenerator()
        email_sender = EmailSender()
        
        # Validate email configuration
        logger.info("Validating email configuration...")
        if not email_sender.validate_email_config():
            raise ValueError("Email configuration validation failed")
        
        # Process each candidate
        for index, candidate in df.iterrows():
            try:
                logger.info(f"Processing candidate {index + 1}/{len(df)}: {candidate['name']}")
                
                # Format salary for display
                formatted_salary = f"${candidate['salary']:,.2f}"
                logger.info(f"Formatted salary for {candidate['name']}: {formatted_salary}")
                
                # Prepare candidate data
                candidate_data = {
                    'name': candidate['name'],
                    'position': candidate['position'],
                    'start_date': candidate.get('start_date', 'TBD'),
                    'salary': formatted_salary,
                    'email': candidate['email'],
                    'reporting_to': candidate.get('reporting_to', 'TBD'),
                    'employment_type': candidate.get('employment_type', 'Full-time'),
                    'location': candidate.get('location', 'TBD'),
                    'response_deadline': candidate.get('response_deadline', '5 business days')
                }
                
                # Generate offer letter
                logger.info(f"Generating offer letter for {candidate['name']}...")
                offer_letter_content = offer_generator.generate_offer_letter(candidate_data)
                
                # Send email with offer letter
                logger.info(f"Sending email to {candidate['email']}...")
                email_sender.send_email(
                    to_email=candidate['email'],
                    candidate_name=candidate['name'],
                    position=candidate['position'],
                    offer_letter_content=offer_letter_content
                )
                
                logger.info(f"Successfully processed candidate: {candidate['name']}")
                
            except Exception as e:
                logger.error(f"Error processing candidate {candidate['name']}: {str(e)}")
                continue
        
        logger.info("Completed processing all candidates")
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        raise

def test_email_configuration():
    """Test email configuration settings."""
    try:
        logger.info("Starting email configuration test...")
        email_sender = EmailSender()
        
        logger.info("Validating email configuration...")
        if not email_sender.validate_email_config():
            raise ValueError("Email configuration validation failed")
        
        # Test email sending with sample content
        test_content = """
        <h2>Test Offer Letter</h2>
        <p>This is a test email to verify the email configuration.</p>
        """
        
        logger.info(f"Sending test email to {EMAIL_USERNAME}...")
        email_sender.send_email(
            to_email=EMAIL_USERNAME,  # Send to self for testing
            candidate_name="Test User",
            position="Test Position",
            offer_letter_content=test_content
        )
        
        logger.info("Email configuration test successful")
        return True
        
    except Exception as e:
        logger.error(f"Error during email test: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        logger.info("Starting offer letter generator...")
        
        # Test email configuration first
        logger.info("Testing email configuration...")
        if not test_email_configuration():
            logger.error("Email configuration test failed. Please check your settings and try again.")
            exit(1)
        
        # Process candidates
        logger.info("Starting candidate processing...")
        process_candidates()
        
        logger.info("Offer letter generator completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        exit(1) 