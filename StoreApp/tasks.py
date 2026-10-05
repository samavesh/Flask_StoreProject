import os
import requests
import jinja2
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")

BASE_DIR = Path(__file__).resolve().parent

template_loader = jinja2.FileSystemLoader(BASE_DIR / "templates")
template_env = jinja2.Environment(loader=template_loader)

def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)

def send_simple_message(to, subject, body, html):
    return requests.post(
  		f"https://api.mailgun.net/v3/{DOMAIN}/messages",
  		auth=("api", MAILGUN_API_KEY),
  		data={"from": f"Matt Dunn <mailgun@{DOMAIN}>",
			"to": [to],
  			"subject": subject,
  			"text": body,
            "html": html
            })


def send_user_registration_email(email, username):
    send_simple_message(
        email,
        "Successfully signed up!",
        f"Hello {username}!,\n\nYou have successfully signed up to the Stores REST API",
        # Render the HTML template for the email body
        render_template("email/action.html", username=username)
    )