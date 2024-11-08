import smtplib
from email.message import EmailMessage
import variables

def email(new_tour, encoding):
    print("Sending email...")
    email_message = EmailMessage()
    email_message["Subject"] = "New Upcoming Tour"
    email_message["From"] = variables.get_receiver()
    email_message["To"] = variables.get_receiver()
    email_message.set_content(f"New upcoming tour: "
                              f"{new_tour}")

    # Set up the SMTP server
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.starttls()
    gmail.ehlo()
    gmail.login(variables.get_username(), variables.get_password())

    # Send email
    gmail.sendmail(variables.get_username(), variables.get_receiver(), email_message.as_string())