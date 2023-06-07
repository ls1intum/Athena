from nltk.tokenize import sent_tokenize


def add_sentence_numbers(content: str) -> str:
    sentences = sent_tokenize(content)
    sentence_numbers_max_length = len(str(len(sentences)))
    return "\n".join(
        f"{str(sentence_number).rjust(sentence_numbers_max_length)}: {sentence}" 
        for sentence_number, sentence 
        in enumerate(sentences, start=1)
    )