from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl

def welcome_sender(email, subject, file_loc):
        try:
            sender = "arunuday117@gmail.com"
            mail = MIMEMultipart()
            mail['From'] = sender
            mail['To'] = email
            mail['Subject'] = subject
            # to_encode = {"email": db_user_data['email']}
            # Load the HTML file
            try:
                with open(file_loc, "r") as f:
                    html = f.read()
                html = html.replace("{{ message }}", subject)
            except Exception as e:
                print(f'Services Failed sending email {e}')
                return False
            html_body = MIMEText(html, "html")
            mail.attach(html_body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(sender, "tpvo egkq tkyk navq")
                # sending the mail
                smtp.sendmail(sender, email, mail.as_string())
            return True
        except Exception as e:
            print(f'Services Failed with error from email sender {e}')
            return False
