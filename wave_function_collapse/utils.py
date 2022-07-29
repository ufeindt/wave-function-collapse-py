from math import log2


def shannon_entropy(*frequencies: float) -> float:
    """Calculates the Shannon entropy for a list of frequencies."""
    sum_frequencies = sum(frequencies)
    probabilities = [f / sum_frequencies for f in frequencies]

    return -sum(p * log2(p) for p in probabilities)
