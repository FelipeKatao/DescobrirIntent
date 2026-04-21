try:
    import torch  # noqa: F401
except ModuleNotFoundError:
    print('Torch não está instalado. Rode: `python -m pip install torch`')
    raise

from nlp import NLPFacade

nlp = NLPFacade()
textos = [
"buscar pedidos do cliente Maria",
"remover usuário com email teste@exemplo.com",
"atualizar endereço para rua das flores 123",
"quero uma maçã verde",
"exportar dados em csv separado por vírgula",
"criar tabela produtos com coluna preço",
"gerar gráfico de vendas por mês",
]
for t in textos:
    got = nlp.palavras_fortes_contexto_objetos(t)
    print(got)


def _assert_contains_all(got, expected_set):
    got_set = {w.lower() for w in got}
    missing = {w.lower() for w in expected_set} - got_set
    assert not missing, f"Missing {missing} in {got}"


def test_palavras_fortes_contexto_objetos_exemplo():
    nlp = NLPFacade()
    text = "crie uma casa pintada de rosa"
    got = nlp.palavras_fortes_contexto_objetos(text)
    _assert_contains_all(got, {"casa", "rosa"})


def test_palavras_fortes_contexto_objetos_outro():
    nlp = NLPFacade()
    text = "gerar um relatório PDF com capa azul"
    got = nlp.palavras_fortes_contexto_objetos(text)
    _assert_contains_all(got, {"relatório", "pdf", "azul"})


def test_varios_contextos_nao_quebra():
    nlp = NLPFacade()
    textos = [
        "buscar pedidos do cliente Maria",
        "remover usuário com email teste@exemplo.com",
        "atualizar endereço para rua das flores 123",
        "quero uma maçã verde",
        "exportar dados em csv separado por vírgula",
        "criar tabela produtos com coluna preço",
        "gerar gráfico de vendas por mês",
    ]
    for t in textos:
        got = nlp.palavras_fortes_contexto_objetos(t)
        assert isinstance(got, list)


if __name__ == "__main__":
    test_palavras_fortes_contexto_objetos_exemplo()
    test_palavras_fortes_contexto_objetos_outro()
    test_varios_contextos_nao_quebra()
    print("OK")