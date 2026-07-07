def draft_email(context: str, tone: str = "polite") -> dict:
    subject = "Request Regarding Submission"
    body = (
        "Dear Sir/Madam,\n\n"
        f"I wanted to write regarding {context}.\n"
        "I apologize for the inconvenience and request your consideration.\n\n"
        "Thank you.\n"
    )

    return {
        "subject": subject,
        "body": body,
        "tone": tone,
        "needs_confirmation_before_send": True,
    }


def send_email_placeholder():
    return {
        "sent": False,
        "message": "Email sending is not connected yet. Draft only for now.",
    }
