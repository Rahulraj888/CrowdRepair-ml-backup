# clustering/utils.py

def filter_valid_reports(raw_reports):
    """
    Return only dicts that have both 'latitude' and 'longitude' keys.
    """
    return [
        r for r in raw_reports
        if isinstance(r, dict) and 'latitude' in r and 'longitude' in r
    ]
