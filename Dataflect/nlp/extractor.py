from .torch_pipeline import TorchNLP

_nlp = TorchNLP()


def split_sentences(text: str):
    return _nlp.decompositor_de_frases(text)


def extract_entities(text: str):
    return _nlp.entidades_da_frase(text)


def extract_object(text: str):
    kws = _nlp.palavras_chaves_da_sentenca(text, top_k=6)
    if not kws:
        return None
    return kws[-1]


def extract_subject(text: str):
    kws = _nlp.palavras_chaves_da_sentenca(text, top_k=6)
    if not kws:
        return None
    return kws[0]