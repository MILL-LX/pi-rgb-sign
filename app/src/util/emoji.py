import random

emoji_list = list("😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😗😙😚☺️🙂🤗🤔😐😑😶🙄😏😣😥😮🤐😯😪😫😴😌😛😜😝🤤😒😓😔😕🙃🤑😲☹️🙁😖😞😟😤😢😭😦😧😨😩😬😰😱😳😵😡😠😷🤒🤕🤢🤧😇🤠🤡🤥🤓😈👿👹👺💀👻👽🤖💩😺😸😹😻😼😽🙀😿😾")

def is_emoji(grapheme: str) -> bool:
    return grapheme in emoji_list

def make_random_quartets(num_quartets: int):
    random_quartets = []
    for _ in range(num_quartets):
        random_quartets.append(''.join(random.choices(emoji_list, k=4)))

    return random_quartets
