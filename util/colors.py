"""
util/colors.py

This module is responsible for generating color palettes
"""

def generate_k_distinct_colors(k: int) -> list[str]:
    """
    Generates k distinct colors.

    :param k:
    :return:
    """
    colors = []
    for i in range(k):
        hue = i / k
        lightness = (50 + i) / (k + 1)
        saturation = 100
        colors.append(f"hsl({hue * 360}, {saturation}%, {lightness}%)")

    return colors