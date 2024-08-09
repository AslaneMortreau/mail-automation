import functions_framework
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import jsonify
from google.cloud import secretmanager

def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/PROJECT_ID/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

def load_email_template():
    with open('email_template.txt', 'r') as file:
        template = file.read()
    return template

def generate_email(recipient_name, appointment_link):
    email_subject = "Confirmation de réception de votre formulaire"
    
    email_template = load_email_template()
    email_body = email_template.format(
        recipient_name=recipient_name,
        appointment_link=appointment_link
    )

    return email_subject, email_body

def send_mail(to_address, subject, body):
    from_address = get_secret("mail-mail")
    password = get_secret("mail-password")

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.server.fr', 587)  
        server.starttls()
        server.login(from_address, password)
        server.sendmail(from_address, to_address, msg.as_string())
        server.close()
        return f"Email envoyé avec succès à {to_address}!"
    except Exception as e:
        return f"Erreur lors de l'envoi de l'email: {e}"

@functions_framework.http
def send_email(request):
    request_json = request.get_json(silent=True)
    first_name = request_json.get('first_name')
    last_name = request_json.get('last_name')
    email = request_json.get('email')

    if not first_name or not last_name or not email:
        return jsonify({'error': 'Veuillez fournir le prénom, le nom et l\'adresse email.'}), 400

    appointment_link = "https://example.com/prendre-rendez-vous"
    recipient_name = f"{first_name} {last_name}"
    subject, body = generate_email(recipient_name, appointment_link)
    
    response = send_mail(email, subject, body)
    
    return jsonify({'message': response})
