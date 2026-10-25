"""Um analista financeiro com LangChain, duas skills e fontes públicas."""

import json
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.tools import ToolException
from langchain_openai import ChatOpenAI

if __package__:
    from .dados_mercado import baixar_precos, calcular_retornos, coletar_fundamentos
    from .execucao_python import executar_codigo
else:
    from dados_mercado import baixar_precos, calcular_retornos, coletar_fundamentos
    from execucao_python import executar_codigo


# 1. Usamos a chave e a .venv da raiz, como nos projetos anteriores.
PROJETO = Path(__file__).resolve().parent
DADOS = PROJETO / "dados"
RESULTADOS = PROJETO / "resultados"
load_dotenv(PROJETO / ".env")
load_dotenv(PROJETO.parent / ".env")


# 2. Cada skill explica um método de análise; o modelo carrega quando precisar.
@tool
def carregar_skill(nome: str) -> str:
    """Lê analise-fundamentalista (indicadores e pares) ou comparar-retornos (preços e gráficos)."""
    if nome not in {"analise-fundamentalista", "comparar-retornos"}:
        raise ToolException("Escolha analise-fundamentalista ou comparar-retornos.")
    print(f"→ Carregando a skill {nome}")
    return (PROJETO / "skills" / nome / "SKILL.md").read_text(encoding="utf-8")


# 3. As ferramentas coletam dados e calculam; o modelo explica os resultados.
@tool
def comparar_fundamentos(papeis: list[str]) -> dict:
    """Compara de 2 a 5 empresas da B3 do mesmo setor e subsetor no Fundamentus.

    Use tickers sem .SA, como ITUB4 e BBDC4. Retorna P/L, P/VP, ROE, dividend yield,
    margem líquida, EV/EBITDA, fontes e datas. Um campo _pct com 12.3 significa 12,3%.
    Salva fundamentos.csv para análises em Python. O retrato é atual, não histórico.
    """
    print("→ Consultando os fundamentos e conferindo setor e subsetor")
    try:
        dados = coletar_fundamentos(papeis)
        DADOS.mkdir(exist_ok=True)
        dados.to_csv(DADOS / "fundamentos.csv", index=False)
        return {
            "criterio": "mesmo setor e subsetor, conforme a classificação do Fundamentus",
            "unidades": "cotação em BRL; pl, pvp e ev_ebitda em vezes; campos _pct em %",
            "empresas": json.loads(dados.to_json(orient="records")),
        }
    except Exception as erro:
        raise ToolException(f"Não consegui comparar os fundamentos: {erro}") from erro


@tool
def comparar_retornos(papeis: list[str], inicio: str, fim: str) -> dict:
    """Compara a variação de preços de 2 a 5 empresas do mesmo setor e subsetor.

    Datas AAAA-MM-DD, com fim até ontem. Usa fechamentos diários do TVDatafeed,
    bolsa BMFBOVESPA, apenas em datas comuns a todos. O conector solicita ajuste
    por desdobramentos (splits). Não calcula retorno total com dividendos/JCP.
    Salva fundamentos.csv e precos.csv para Python. Informe o período efetivamente retornado.
    """
    print("→ Baixando cotações diárias pelo TVDatafeed")
    try:
        fundamentos = coletar_fundamentos(papeis)
        precos = baixar_precos(papeis, inicio, fim)
        tabela = calcular_retornos(precos)
        DADOS.mkdir(exist_ok=True)
        fundamentos.to_csv(DADOS / "fundamentos.csv", index=False)
        precos.to_csv(DADOS / "precos.csv")
        return {
            "fonte": "TradingView via TVDatafeed — BMFBOVESPA, barras diárias",
            "solicitado": {"inicio": inicio, "fim": fim},
            "periodo_efetivo": {"inicio": str(precos.index[0].date()), "fim": str(precos.index[-1].date())},
            "observacoes_comuns": len(precos),
            "ajuste_solicitado": "splits; sem cálculo de reinvestimento de dividendos ou JCP",
            "limite_da_fonte": "até 5000 barras; o período efetivo pode ser menor que o solicitado",
            "coletado_em": str(date.today()),
            "resultados": json.loads(tabela.to_json(orient="records")),
        }
    except Exception as erro:
        raise ToolException(f"Não consegui comparar os retornos: {erro}") from erro


@tool
def executar_python(codigo: str) -> dict:
    """Executa Python na .venv da raiz, com limite de 30 segundos.

    Já existem pd, plt, fundamentos (último fundamentos.csv) e precos (último
    precos.csv, índice de datas, uma coluna por papel). Consulte as ferramentas
    de comparação primeiro e confira os papéis. Cada chamada começa do zero.
    Use print para números e plt.savefig('grafico.png') para gráficos. Não é um sandbox.
    """
    print("→ Executando Python na .venv da raiz")
    try:
        return executar_codigo(codigo, DADOS, RESULTADOS)
    except (OSError, ValueError) as erro:
        raise ToolException(str(erro)) from erro


@tool
def salvar_relatorio(nome: str, conteudo: str) -> str:
    """Salva um novo relatório Markdown em resultados, como comparacao_bancos.md."""
    arquivo = RESULTADOS / nome
    if (Path(nome).name != nome or nome.startswith(".")
            or arquivo.suffix != ".md" or arquivo.is_symlink()):
        raise ToolException("Use apenas um nome de arquivo .md, sem pastas ou links.")
    RESULTADOS.mkdir(exist_ok=True)
    try:
        with arquivo.open("x", encoding="utf-8") as saida:
            saida.write(conteudo)
    except FileExistsError:
        raise ToolException("O relatório já existe. Escolha outro nome.") from None
    print(f"→ Relatório salvo em resultados/{nome}")
    return f"Relatório salvo em resultados/{nome}."


# 4. A abertura explica o projeto antes de criar o agente, sem chamadas à API.
def mostrar_contexto():
    print(f"""
Projeto02 — Analista financeiro | {date.today():%d/%m/%Y}

Vamos comparar empresas da B3 do mesmo setor e subsetor.
  • Fundamentus: P/L, P/VP, ROE, dividend yield e outros indicadores disponíveis.
  • TVDatafeed: histórico diário de preços do TradingView.
  • Python: cálculos, gráficos e relatórios usando a .venv da raiz.

Os dados são consultados sob demanda; não é necessário baixar um CSV antes.
Fundamentos são um retrato da consulta, com datas da cotação e do último balanço.
A comparação de retornos usa as mesmas datas para todas as ações. É variação
na cotação fornecida, com ajuste solicitado por splits; não é retorno total
com dividendos reinvestidos. As fontes podem estar indisponíveis ou limitadas.

Experimente:
  - Compare os fundamentos de ITUB4, BBDC4 e BBAS3.
  - Compare os retornos dessas empresas de 2025-01-01 a 2025-12-31.
  - Faça um gráfico em base 100 e salve um relatório.

Digite 'sair' para encerrar.
""")


def main():
    mostrar_contexto()
    # 5. Mantemos o modelo e o raciocínio dos projetos anteriores.
    modelo = ChatOpenAI(model="gpt-6-luna", reasoning={"effort": "low"}, use_responses_api=True)
    ferramentas = [carregar_skill, comparar_fundamentos, comparar_retornos, executar_python, salvar_relatorio]
    for ferramenta in ferramentas:
        ferramenta.handle_tool_error = True

    # 6. Nosso código entrega AGENTS.md ao modelo como instruções gerais.
    instrucoes = f"Data de referência: {date.today().isoformat()}.\n\n"
    instrucoes += (PROJETO / "AGENTS.md").read_text(encoding="utf-8")
    agente = create_agent(model=modelo, tools=ferramentas, system_prompt=instrucoes)

    # 7. O histórico permanece na memória até o usuário sair.
    mensagens = []
    while True:
        try:
            pedido = input("\nVocê: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAté mais!")
            break
        if pedido.lower() == "sair":
            print("Até mais!")
            break
        if not pedido:
            continue
        try:
            resultado = agente.invoke(
                {"messages": mensagens + [{"role": "user", "content": pedido}]},
                config={"recursion_limit": 20},
            )
        except Exception as erro:
            print(f"Não consegui concluir ({type(erro).__name__}). Tente novamente.")
            continue
        mensagens = resultado["messages"]
        print("\nAnalista:", mensagens[-1].text)


if __name__ == "__main__":
    main()
