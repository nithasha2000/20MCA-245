from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl

def welcome_sender(email, subject, email_body, file_loc):
        try:
            sender = "abilityportal@gmail.com"
            mail = MIMEMultipart()
            mail['From'] = sender
            mail['To'] = email
            mail['Subject'] = subject
            try:
                with open(file_loc, "r") as f:
                    html = f.read()
                html = html.replace("{{ message }}", email_body)
            except Exception as e:
                print(f'Services Failed sending email {e}')
                return False
            html_body = MIMEText(html, "html")
            mail.attach(html_body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(sender, "zuvz qzbf posi xrov")
                # sending the mail
                smtp.sendmail(sender, email, mail.as_string())
            return True
        except Exception as e:
            print(f'Services Failed with error from email sender {e}')
            return False
