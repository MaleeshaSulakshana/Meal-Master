from email.message import EmailMessage
import smtplib

global sender_email
global sender_psw
sender_email = "mealmasterrecipes@gmail.com"
sender_psw = "meal1234"


def send_recovery_code(receiver_email, code):
    # construct email
    email = EmailMessage()
    email['Subject'] = ''
    email['From'] = sender_email
    email['To'] = str(receiver_email)
    email.set_content(
        """Password recovery code : <b>{}</b>""".format(str(code)), subtype='html')

    # Send
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_psw)
    server.send_message(email)
    server.quit()


def send_payment_receipt(receiver_email, code, today, endday):
    # construct email
    email = EmailMessage()
    email['Subject'] = 'Meal Master 30 Days Subscription'
    email['From'] = sender_email
    email['To'] = str(receiver_email)
    email.set_content(
        """Hi,
            <br><br>
            You payed for <b>Meal Master</b> 30 days subscription (payment id : <b>{}</b>).
            On today(<b>{}</b>) started your 30 days. And subscription end on <b>{}</b>.
            <br><br>
            If you have any clarification please contact <b>Meal Master</b> team.
            <br><br>
            Thank you
        """.format(str(code), str(today), str(endday)), subtype='html')

    # Send
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_psw)
    server.send_message(email)
    server.quit()
