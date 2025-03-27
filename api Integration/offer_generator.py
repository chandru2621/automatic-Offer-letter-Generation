import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import config

class OfferGenerator:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(config.TEMPLATE_DIR)
        )
        self.template = self.env.get_template('offer_letter_template.html')

    def generate_offer_letter(self, candidate_data):
        """
        Generate an offer letter for a candidate using the template.
        
        Args:
            candidate_data (dict): Dictionary containing candidate information
                Required keys: name, position, start_date, salary, email
        
        Returns:
            str: Generated HTML offer letter
        """
        # Format the current date
        current_date = datetime.now().strftime('%B %d, %Y')
        
        # Prepare template data
        template_data = {
            'name': candidate_data['name'],
            'position': candidate_data['position'],
            'start_date': candidate_data['start_date'],
            'salary': candidate_data['salary'],
            'email': candidate_data['email'],
            'current_date': current_date,
            'company_name': config.COMPANY_NAME,
            'company_address': config.COMPANY_ADDRESS,
            'company_website': config.COMPANY_WEBSITE,
            'employment_type': candidate_data.get('employment_type', 'Full-time'),
            'location': candidate_data.get('location', 'Main Office'),
            'reporting_to': candidate_data.get('reporting_to', 'Department Manager'),
            'response_deadline': candidate_data.get('response_deadline', '5 business days')
        }

        # Render the template
        offer_letter = self.template.render(**template_data)
        return offer_letter

    def save_offer_letter(self, offer_letter, candidate_name):
        """
        Save the generated offer letter to a file.
        
        Args:
            offer_letter (str): The generated offer letter HTML
            candidate_name (str): Name of the candidate
        
        Returns:
            str: Path to the saved file
        """
        # Create output directory if it doesn't exist
        output_dir = os.path.join(config.DATA_DIR, 'generated_letters')
        os.makedirs(output_dir, exist_ok=True)

        # Generate filename
        filename = f"offer_letter_{candidate_name.lower().replace(' ', '_')}.html"
        filepath = os.path.join(output_dir, filename)

        # Save the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(offer_letter)

        return filepath 