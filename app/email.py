from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(to, new_user):
    message = Mail(
            from_email=current_app.config['FLASKY_MAIL_SENDER'],
            to_emails=to,
            subject=f"[Flasky] Novo usuário",
            html_content=f"""
                <p>Aluno: Henrique Teodoro Silva</p>
                <p>Prontuário: PT3037461</p>
                <p>Usuário cadastrado: {new_user}</p>
            """
        )
    try:
        sg = SendGridAPIClient(current_app.config['API_KEY'])
        response = sg.send(message)
        print(f"E-mail enviado via SendGrid (Status {response.status_code})", flush=True)
        return response
    except Exception as e:
        print(f"Erro ao enviar e-mail via SendGrid: {e}", flush=True)
        return None