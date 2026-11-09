from flask import current_app, render_template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to, subject, template, **kwargs):
    html_body = render_template(template + '.html', **kwargs)

    message = Mail(
        from_email=current_app.config['FLASKY_MAIL_SENDER'],
        to_emails=to,
        subject=f"[Flasky] {subject}",
        html_content=html_body
    )

    try:
        sg = SendGridAPIClient(current_app.config['API_KEY'])
        response = sg.send(message)
        print(f"E-mail enviado via SendGrid (Status {response.status_code})", flush=True)
        return response
    except Exception as e:
        print(f"Erro ao enviar e-mail via SendGrid: {e}", flush=True)
        return None