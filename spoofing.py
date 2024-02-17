import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
import traceback

# Load SMTP configuration from config.ini file
def load_smtp_config():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        smtp_config = {
            'host': config.get('SMTP', 'host'),
            'port': config.getint('SMTP', 'port'),
            'username': config.get('SMTP', 'username'),
            'password': config.get('SMTP', 'password')
        }
        return smtp_config
    except Exception as e:
        print("Error loading SMTP configuration:", e)
        return None

# Send spoofed email
def send_mail(receiver_email, spoofed_email, spoofed_name, message, subject):
    try:
        smtp_config = load_smtp_config()
        if smtp_config:
            msg = MIMEMultipart()
            msg['From'] = f"{spoofed_name} <{spoofed_email}>"
            msg['To'] = receiver_email
            msg['Subject'] = subject
            body = message
            msg.attach(MIMEText(body, 'plain'))
            # Connect to SMTP server and send email
            with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
                server.starttls()
                server.login(smtp_config['username'], smtp_config['password'])
                server.sendmail(spoofed_email, receiver_email, msg.as_string())
            print('Spoofed Email sent successfully to', receiver_email, 'from', spoofed_name)
    except Exception as e:
        # Print and log the exception
        print("Error sending email:", e)
        traceback.print_exc()

def main():
    receiver_email = input("Enter receiver email(s) separated by commas: ").strip()
    spoofed_email = input("Enter spoofed email: ").strip()
    spoofed_name = input("Enter spoofed name: ").strip()
    message = input("Enter message: ").strip()
    subject = input("Enter subject: ").strip()

    # Invoke send_mail to send email
    send_mail(receiver_email, spoofed_email, spoofed_name, message, subject)

if __name__ == "__main__":
    main()
