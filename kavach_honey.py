def add_honey_token(text):
    """Phase 4: Appends an invisible U+E0053 (S for Sovereign) to track provenance."""
    return f"{text}\U000E0053"