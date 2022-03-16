

def level_range(value):
    """
    Return level of trait by its score.
    Note: Not quite proud of this, but it works.
    """
    if 90 < value <= 100:
        return "ext_high"
    elif 70 < value <= 90:
        return "high"
    elif 60 < value <= 70:
        return "higher"
    elif 40 <= value <= 60:
        return "neutral"
    elif 30 <= value < 40:
        return "lower"
    elif 10 <= value < 30:
        return "low"
    elif 0 <= value < 10:
        return "ext_low"


def age_range(value):
    """
    Return age range.
    """
    if 90 < value <= 100:
        return "90-100"
    elif 80 < value <= 90:
        return "80-90"
    elif 70 < value <= 80:
        return "70-80"
    elif 60 < value <= 70:
        return "60-70"
    elif 50 < value <= 60:
        return "50-60"
    elif 40 <= value <= 50:
        return "40-50"
    elif 30 <= value < 40:
        return "30-40"
    elif 20 <= value < 30:
        return "20-30"
    elif  14 <= value < 20:
        return "14-20"
