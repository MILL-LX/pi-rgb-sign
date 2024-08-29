import os
import random

import emoji

_EMOJI_GLYPH_DIR = 'assets/emoji_glyphs/32x32'

def _emoji_list_from_glyphs(emoji_glyph_dir: str = _EMOJI_GLYPH_DIR):
    emoji_list = []
    for filename in os.listdir(emoji_glyph_dir):
        if filename.endswith('.png'):
            codepoints = filename[:-4].split('-')  # Remove .png and split by '-'
            emoji = ''.join(chr(int(cp, 16)) for cp in codepoints)
            emoji_list.append(emoji)
    return emoji_list

# _emoji_list = _emoji_list_from_glyphs()
_emoji_list = list(emoji.EMOJI_DATA.keys())

def is_emoji(grapheme: str) -> bool:
    return grapheme in _emoji_list

def make_random_quartets(num_quartets: int):
    random_quartets = []
    for _ in range(num_quartets):
        random_quartets.append(''.join(random.choices(_emoji_list, k=4)))

    return random_quartets
