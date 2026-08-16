import html
import json
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


AI_ANALYSIS_FILE = Path(
    "kaggle-worker/output/ai_analysis.json"
)

INPUT_FILE = Path(
    "kaggle-worker/input/daily_input.json"
)


def load_json(path: Path) -> dict:
    """Load JSON file."""

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def build_email_html(
    input_data: dict,
    ai_data: dict,
) -> str:
    """Build the HTML email."""

    repositories = input_data.get(
        "repositories",
        [],
    )

    ai_repositories = {
        repository.get("full_name"): repository
        for repository in ai_data.get(
            "repositories",
            [],
        )
    }

    date = input_data.get(
        "date",
        "Unknown date",
    )

    sections = []

    for index, repository in enumerate(
        repositories,
        start=1,
    ):

        full_name = repository.get(
            "full_name",
            "Unknown",
        )

        description = (
            repository.get(
                "description"
            )
            or "No description available."
        )

        language = (
            repository.get(
                "language"
            )
            or "Unknown"
        )

        stars = repository.get(
            "stargazers_count",
            0,
        )

        forks = repository.get(
            "forks_count",
            0,
        )

        radar_score = repository.get(
            "radar_score",
            0,
        )

        url = repository.get(
            "html_url",
            f"https://github.com/{full_name}",
        )

        ai_repository = ai_repositories.get(
            full_name,
            {},
        )

        analysis = ai_repository.get(
            "analysis",
            {},
        )

        what_it_is = analysis.get(
            "what_it_is",
            "Not specified in the repository.",
        )

        what_it_solves = analysis.get(
            "what_it_solves",
            "Not specified in the repository.",
        )

        why_developers_care = analysis.get(
            "why_developers_care",
            "Not specified in the repository.",
        )

        how_to_use_it = analysis.get(
            "how_to_use_it",
            "Not specified in the repository.",
        )

        important_features = analysis.get(
            "important_features",
            [],
        )

        features_html = ""

        for feature in important_features:

            features_html += (
                f"<li>{html.escape(str(feature))}</li>"
            )

        sections.append(
            f"""
            <div style="
                border:1px solid #ddd;
                border-radius:10px;
                padding:20px;
                margin:20px 0;
            ">

                <h2>
                    {index}.
                    <a href="{html.escape(url)}">
                        {html.escape(full_name)}
                    </a>
                </h2>

                <p>
                    {html.escape(description)}
                </p>

                <table>
                    <tr>
                        <td><b>⭐ Stars</b></td>
                        <td>{stars:,}</td>
                    </tr>

                    <tr>
                        <td><b>🍴 Forks</b></td>
                        <td>{forks:,}</td>
                    </tr>

                    <tr>
                        <td><b>📊 Radar Score</b></td>
                        <td>{radar_score:.2f}</td>
                    </tr>

                    <tr>
                        <td><b>Language</b></td>
                        <td>{html.escape(str(language))}</td>
                    </tr>
                </table>

                <h3>What it is</h3>
                <p>{html.escape(str(what_it_is))}</p>

                <h3>What it solves</h3>
                <p>{html.escape(str(what_it_solves))}</p>

                <h3>Why developers care</h3>
                <p>
                    {html.escape(
                        str(why_developers_care)
                    )}
                </p>

                <h3>How to use it</h3>
                <p>
                    {html.escape(
                        str(how_to_use_it)
                    )}
                </p>

                <h3>Important features</h3>

                <ul>
                    {features_html}
                </ul>

                <p>
                    <a href="{html.escape(url)}">
                        View repository on GitHub →
                    </a>
                </p>

            </div>
            """
        )

    return f"""
    <!DOCTYPE html>

    <html>

    <head>
        <meta charset="UTF-8">
        <title>Dev Radar</title>
    </head>

    <body style="
        font-family:Arial,sans-serif;
        max-width:800px;
        margin:auto;
        padding:20px;
        color:#222;
    ">

        <h1>🚀 Dev Radar</h1>

        <p>
            Daily GitHub repository radar for
            <b>{html.escape(str(date))}</b>
        </p>

        <p>
            Here are today's selected repositories
            and their AI-generated technical analysis.
        </p>

        {"".join(sections)}

        <hr>

        <p style="color:#777;font-size:12px;">
            Generated automatically by Dev Radar.
        </p>

    </body>

    </html>
    """


def send_email(
    subject: str,
    html_body: str,
) -> None:
    """Send email using Gmail SMTP."""

    smtp_host = os.environ.get(
        "SMTP_HOST",
        "smtp.gmail.com",
    )

    smtp_port = int(
        os.environ.get(
            "SMTP_PORT",
            "465",
        )
    )

    sender = os.environ.get(
        "EMAIL_USER"
    )

    password = os.environ.get(
        "EMAIL_APP_PASSWORD"
    )

    recipient = os.environ.get(
        "EMAIL_TO"
    )

    if not sender:
        raise RuntimeError(
            "EMAIL_USER is not configured."
        )

    if not password:
        raise RuntimeError(
            "EMAIL_APP_PASSWORD is not configured."
        )

    if not recipient:
        raise RuntimeError(
            "EMAIL_TO is not configured."
        )

    message = MIMEMultipart(
        "alternative"
    )

    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient

    plain_text = (
        "Dev Radar report is available "
        "in the HTML version of this email."
    )

    message.attach(
        MIMEText(
            plain_text,
            "plain",
            "utf-8",
        )
    )

    message.attach(
        MIMEText(
            html_body,
            "html",
            "utf-8",
        )
    )

    print(
        f"📧 Sending email to {recipient}"
    )

    with smtplib.SMTP_SSL(
        smtp_host,
        smtp_port,
    ) as server:

        server.login(
            sender,
            password,
        )

        server.sendmail(
            sender,
            recipient,
            message.as_string(),
        )

    print(
        "✅ Email sent successfully."
    )


def main() -> None:

    print(
        "📧 Dev Radar Email"
    )

    input_data = load_json(
        INPUT_FILE
    )

    ai_data = load_json(
        AI_ANALYSIS_FILE
    )

    if ai_data.get("status") != "success":

        raise RuntimeError(
            "AI analysis did not complete successfully."
        )

    repositories = ai_data.get(
        "repositories",
        [],
    )

    failed = [
        repository
        for repository in repositories
        if repository.get("status") != "success"
    ]

    if failed:

        names = ", ".join(
            repository.get(
                "full_name",
                "Unknown",
            )
            for repository in failed
        )

        raise RuntimeError(
            f"AI analysis failed for: {names}"
        )

    date = input_data.get(
        "date",
        "Unknown date",
    )

    html_body = build_email_html(
        input_data,
        ai_data,
    )

    send_email(
        subject=f"🚀 Dev Radar — {date}",
        html_body=html_body,
    )


if __name__ == "__main__":
    main()