def load_words(word_file_path):
    with open(word_file_path, 'r') as word_file:
        words = word_file.readlines()
    word_list = [word.strip().upper() for word in words if len(word) == 5]
    return word_list
