"""Uma analista de dados imobiliários com LangChain, Pandas e uma skill."""

from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.tools import ToolException
from langchain_openai import ChatOpenAI

if __package__:
    from .execucao_python import executar_codigo
else:
    from execucao_python import executar_codigo


# 1. Definimos os caminhos e carregamos a chave do .env.
PROJETO = Path(__file__).resolve().parent
ARQUIVO = PROJETO / "dados" / "housing.csv"
RESULTADOS = PROJETO / "resultados"

load_dotenv(PROJETO / ".env")
load_dotenv(PROJETO.parent / ".env")


# 2. O Pandas lê o CSV, mantendo os valores ausentes para podermos estudá-los.
def ler_dados() -> pd.DataFrame:
    dados = pd.read_csv(ARQUIVO, encoding="utf-8-sig")
    obrigatorias = {"median_house_value", "total_bedrooms", "ocean_proximity"}
    if not obrigatorias.issubset(dados.columns):
        raise ToolException("Use housing.csv da base California Housing Prices. Veja dados/README.md.")
    if dados.empty:
        raise ToolException("O CSV está vazio.")
    return dados


# 3. A skill só entra na conversa quando o modelo chama esta ferramenta.
@tool
def carregar_skill() -> str:
    """Carrega a skill analise-imoveis: método para explorar a base California Housing."""
    print("→ Carregando a skill analise-imoveis")
    return (PROJETO / "skills" / "analise-imoveis" / "SKILL.md").read_text(encoding="utf-8")


@tool
def resumo_dados() -> dict:
    """Mostra qualidade dos dados e estatísticas dos valores medianos por grupo censitário."""
    print("→ Resumindo os dados")
    dados = ler_dados()
    valores = dados["median_house_value"]
    return {
        "fonte": "dados/housing.csv — California Housing Prices, censo de 1990",
        "unidade_de_observacao": "grupo censitário, não uma casa individual",
        "linhas": len(dados),
        "colunas": list(dados.columns),
        "valores_ausentes": dados.isna().sum().to_dict(),
        "linhas_duplicadas": int(dados.duplicated().sum()),
        "media_das_medianas_usd": round(float(valores.mean()), 2),
        "mediana_das_medianas_usd": round(float(valores.median()), 2),
        "menor_mediana_usd": float(valores.min()),
        "maior_mediana_registrada_usd": float(valores.max()),
        "grupos_por_proximidade_do_oceano": dados["ocean_proximity"].value_counts().to_dict(),
    }


@tool
def comparar_regioes() -> dict:
    """Compara os valores medianos dos imóveis pelas categorias de ocean_proximity.

    Retorna a quantidade de grupos censitários, a média e a mediana dos valores
    medianos de cada categoria. Cada grupo censitário recebe o mesmo peso.
    """
    print("→ Comparando as categorias de proximidade do oceano")
    dados = ler_dados()
    tabela = dados.groupby("ocean_proximity", dropna=False).agg(
        grupos_censitarios=("median_house_value", "size"),
        media_das_medianas_usd=("median_house_value", "mean"),
        mediana_das_medianas_usd=("median_house_value", "median"),
    ).sort_values("media_das_medianas_usd", ascending=False)
    return {
        "fonte": "dados/housing.csv — censo de 1990",
        "criterio": "média simples das medianas; mesmo peso para cada grupo censitário",
        "resultados": tabela.round(2).reset_index().to_dict(orient="records"),
    }


@tool
def executar_python(codigo: str) -> dict:
    """Executa Python local na .venv da raiz, com limite de 30 segundos.

    Já existem df (DataFrame completo), pd (Pandas) e plt (Matplotlib).
    As colunas são as originais de housing.csv. Use print para retornar números
    e plt.savefig('grafico.png') para salvar gráficos na pasta desta execução.
    Cada chamada começa do zero. O código é salvo em codigo.py. Não é um sandbox.
    """
    print("→ Executando Python na .venv da raiz")
    try:
        return executar_codigo(codigo, ARQUIVO, RESULTADOS)
    except (OSError, ValueError) as erro:
        raise ToolException(str(erro)) from erro


@tool
def salvar_relatorio(nome: str, conteudo: str) -> str:
    """Salva um relatório Markdown em resultados. Use um nome novo, como imoveis.md."""
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


# 4. Mostramos o contexto e um resumo calculado localmente antes de criar o agente.
def mostrar_contexto():
    dados = ler_dados()
    ausentes = dados.isna().sum()
    texto_ausentes = ", ".join(f"{coluna}: {qtd}" for coluna, qtd in ausentes.items() if qtd)
    print(f"""
Projeto02 — Analista de dados: California Housing Prices

Vamos explorar dados de moradia da Califórnia, provenientes do censo de 1990.
Cada linha representa um grupo censitário, não uma casa individual.
median_house_value é o valor mediano dos imóveis desse grupo, em dólares (USD).
São dados históricos: eles não representam os preços atuais.

Resumo de dados/housing.csv:
  • {len(dados)} linhas e {len(dados.columns)} colunas.
  • {dados['ocean_proximity'].nunique()} categorias de proximidade do oceano.
  • Valores ausentes por coluna: {texto_ausentes or 'nenhum'}.
  • Média das medianas dos grupos: US$ {dados['median_house_value'].mean():.2f}.
Essa média dá o mesmo peso a cada grupo; não é a média de todas as casas.

O agente usa AGENTS.md, uma skill e ferramentas para calcular, gerar gráficos
com Python na .venv da raiz e salvar relatórios.
Experimente:
  - Compare os valores dos imóveis por proximidade do oceano.
  - A renda mediana tem relação com o valor mediano dos imóveis? Faça um gráfico.
  - Quais dados estão faltando?

Digite 'sair' para encerrar.
""")


def main():
    if not ARQUIVO.is_file():
        print("Baixe housing.csv do Kaggle e coloque em Projeto02/dados. Veja o README do projeto.")
        return
    try:
        mostrar_contexto()
    except (OSError, ValueError, ToolException) as erro:
        print(f"Não consegui ler a base: {erro}")
        return

    # 5. Mantemos o mesmo modelo utilizado no Projeto01.
    modelo = ChatOpenAI(
        model="gpt-6-luna",
        reasoning={"effort": "low"},
        use_responses_api=True,
    )
    ferramentas = [carregar_skill, resumo_dados, comparar_regioes, executar_python, salvar_relatorio]
    for ferramenta in ferramentas:
        ferramenta.handle_tool_error = True

    # 6. Nosso código lê AGENTS.md e o entrega ao modelo como instruções gerais.
    instrucoes = (PROJETO / "AGENTS.md").read_text(encoding="utf-8")
    agente = create_agent(model=modelo, tools=ferramentas, system_prompt=instrucoes)

    # 7. A lista mantém o histórico da conversa até o usuário digitar sair.
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
