from datetime import datetime, timezone

def google_timestamp_now():
    epoch_1601 = datetime(1601, 1, 1, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    microseconds = int((now - epoch_1601).total_seconds() * 1_000_000)
    return str(microseconds)