def security_kill_switch(analysis_results, threshold=5):
    """Phase 3: Blocks the prompt if it contains too much sensitive data."""
    count = len(analysis_results)
    if count > threshold:
        return False, f"🚨 BREACH PREVENTED: {count} sensitive entities detected. Process Halted."
    return True, "Safe"

def detect_infrastructure_threat(text):
    """Detects attempts to query Critical Information Infrastructure (CII)."""
    cii_triggers = ["scada", "power grid", "nuclear", "plc", "modbus", "water supply"]
    detected = [word for word in cii_triggers if word in text.lower()]
    if detected:
        return False, f"🚨 CII ALERT: Query contains restricted infrastructure keywords: {detected}."
    return True, "Safe"