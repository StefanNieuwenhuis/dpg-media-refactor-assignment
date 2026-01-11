from constants import MIN_QUALITY, MAX_QUALITY


def clamp_quality(quality: int) -> int:
    """Clamp quality between MIN_QUALITY and MAX_QUALITY."""
    return max(MIN_QUALITY, min(MAX_QUALITY, quality))