import os
import random


def _load_emoji_list(emoji_glyph_dir: str = 'assets/emoji_glyphs/32x32'):
    emoji_list = []
    for filename in os.listdir(emoji_glyph_dir):
        if filename.endswith('.png'):
            codepoints = filename[:-4].split('-')  # Remove .png and split by '-'
            emoji = ''.join(chr(int(cp, 16)) for cp in codepoints)
            emoji_list.append(emoji)
    return emoji_list

emoji_list = _load_emoji_list()

def is_emoji(grapheme: str) -> bool:
    return grapheme in emoji_list

def make_random_quartets(num_quartets: int):
    random_quartets = []
    for _ in range(num_quartets):
        random_quartets.append(''.join(random.choices(emoji_list, k=4)))

    return random_quartets
