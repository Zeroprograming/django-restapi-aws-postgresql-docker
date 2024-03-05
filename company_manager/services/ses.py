from decouple import config
import boto3

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import boto3

def send_ses_email(subject, body_text, body_html, recipient_emails, attachment):
    # Create a multipart/mixed parent container
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] =  config('EMAIL_HOST_USER')
    msg['To'] = ', '.join(recipient_emails)
    
    # Add body to email
    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(body_text.encode('utf-8'), 'plain', 'utf-8')
    htmlpart = MIMEText(body_html.encode('utf-8'), 'html', 'utf-8')
    
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)
    msg.attach(msg_body)
    
    # Attachment
    if attachment:
        with open(attachment, 'rb') as f:
            part = MIMEApplication(f.read())
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
            msg.attach(part)
        
    # Connect to AWS SES
    ses_client = boto3.client(
        'ses',
        region_name=config('AWS_SES_REGION_NAME'),
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
    )
    
    # Try to send the email.
    try:
        response = ses_client.send_raw_email(
            Source= config('EMAIL_HOST_USER'),
            Destinations=recipient_emails,
            RawMessage={'Data': msg.as_string()}
        )
    except Exception as e:
        print(e)
        return False
    
    return True