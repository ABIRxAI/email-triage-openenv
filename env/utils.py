def is_phishing(email):
    """Detect simple phishing patterns"""
    text = (email["subject"] + " " + email["body"]).lower()

    suspicious_keywords = [
        "verify",
        "urgent",
        "click",
        "suspend",
        "login",
        "password",
        "otp"
    ]

    return any(word in text for word in suspicious_keywords)

def has_urgent_tone(email):
    """Check if email sounds urgent"""
    text = (email["subject"] + " " + email["body"]).lower()

    urgent_words = [
        "immediately",
        "asap",
        "urgent",
        "now",
        "within 1 hour"
    ]

    return any(word in text for word in urgent_words)

def is_promotional(email):
    """Detect promotional/spam emails"""
    text = (email["subject"] + " " + email["body"]).lower()

    promo_words = [
        "offer",
        "discount",
        "sale",
        "win",
        "free",
        "cashback"
    ]

    return any(word in text for word in promo_words)

def clean_text(text):
    """Basic text cleaning"""
    return text.lower().strip()

def extract_features(email):
    """Convert email into features (useful for ML later)"""
    return {
        "length": len(email["body"]),
        "has_attachment": email.get("attachments", False),
        "priority": email.get("priority", "low"),
        "is_phishing": is_phishing(email),
        "is_promotional": is_promotional(email)
    }