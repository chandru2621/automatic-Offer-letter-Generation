# Offer Letter Generator

This Python project automatically generates and sends customized offer letters via email. It uses a template-based approach to create personalized offer letters for multiple candidates.

## Features

- Template-based offer letter generation
- Customizable content based on candidate information
- Automated email sending
- Environment variable configuration for sensitive data

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with the following variables:
```
SMTP_SERVER=your_smtp_server
SMTP_PORT=587
EMAIL_USERNAME=your_email
EMAIL_PASSWORD=your_password
```

3. Prepare your candidate data in a CSV file with the following columns:
- name
- position
- start_date
- salary
- email

## Usage

1. Place your offer letter template in the `templates` directory
2. Run the main script:
```bash
python main.py
```

## Project Structure

- `main.py`: Main script to orchestrate the offer letter generation and sending process
- `offer_generator.py`: Module for generating offer letters from templates
- `email_sender.py`: Module for handling email operations
- `config.py`: Configuration settings and environment variables
- `templates/`: Directory containing offer letter templates
- `data/`: Directory for storing candidate data 