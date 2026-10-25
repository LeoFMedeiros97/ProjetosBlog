"""Coleta fundamentos no Fundamentus e preços diários pelo TVDatafeed."""

import re
import unicodedata
from datetime import date, datetime
from functools import lru_cache

import pandas as pd
import requests
import truststore
from lxml import html
from tvDatafeed import Interval, TvDatafeed

# Usa os certificados confiáveis do sistema, mantendo a verificação HTTPS ativa.
truststore.inject_into_ssl()


def validar_papeis(papeis: list[str]) -> list[str]:
    papeis = [papel.strip().upper() for papel in papeis]
    if not 2 <= len(papeis) <= 5 or len(set(papeis)) != len(papeis):
        raise ValueError("Escolha de 2 a 5 ações diferentes da B3.")
    if any(not re.fullmatch(r"[A-Z]{4}[0-9]{1,2}", papel) for papel in papeis):
        raise ValueError("Use tickers como ITUB4 e BBDC4, sem .SA ou prefixo da bolsa.")
    if len({papel[:4] for papel in papeis}) != len(papeis):
        raise ValueError("Escolha uma classe por empresa; ITUB3 e ITUB4 representam a mesma empresa.")
    return papeis


def numero_br(texto: str) -> float | None:
    """Converte 1.234,56 para 1234.56 e 12,3% para 12.3, sem dividir por 100."""
    texto = texto.strip()
    if texto in {"", "-", "N/A"}:
        return None
    return float(texto.replace(".", "").replace(",", ".").replace("%", ""))


def ler_pagina(conteudo: bytes) -> dict:
    # Cada célula de rótulo é seguida pela célula que contém o valor.
    campos = {}
    for celula in html.fromstring(conteudo).xpath('//td[contains(@class, "label")]'):
        vizinhas = celula.xpath("following-sibling::td[1]")
        if vizinhas:
            rotulo = unicodedata.normalize("NFKD", celula.text_content())
            rotulo = re.sub(r"[^a-z0-9]", "", rotulo.encode("ascii", "ignore").decode().lower())
            campos[rotulo] = vizinhas[0].text_content().strip()
    return campos


@lru_cache(maxsize=32)
def consultar_empresa(papel: str) -> dict:
    # O cache dura só esta sessão; a data da coleta acompanha cada registro.
    url = f"https://www.fundamentus.com.br/detalhes.php?papel={papel}"
    resposta = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    resposta.raise_for_status()
    campos = ler_pagina(resposta.content)
    if campos.get("papel") != papel or not campos.get("setor") or not campos.get("subsetor"):
        raise ValueError(f"Não consegui identificar empresa, setor e subsetor de {papel} no Fundamentus.")

    def data(campo):
        valor = campos.get(campo, "-")
        return None if valor == "-" else datetime.strptime(valor, "%d/%m/%Y").date().isoformat()

    return {
        "papel": papel,
        "empresa": campos.get("empresa"),
        "setor": campos["setor"],
        "subsetor": campos["subsetor"],
        "cotacao_brl": numero_br(campos.get("cotacao", "-")),
        "data_cotacao": data("dataultcot"),
        "ultimo_balanco": data("ultbalancoprocessado"),
        "pl": numero_br(campos.get("pl", "-")),
        "pvp": numero_br(campos.get("pvp", "-")),
        "roe_pct": numero_br(campos.get("roe", "-")),
        "dividend_yield_pct": numero_br(campos.get("divyield", "-")),
        "margem_liquida_pct": numero_br(campos.get("margliquida", "-")),
        "ev_ebitda": numero_br(campos.get("evebitda", "-")),
        "coletado_em": datetime.now().astimezone().isoformat(timespec="seconds"),
        "fonte": url,
    }


def coletar_fundamentos(papeis: list[str]) -> pd.DataFrame:
    papeis = validar_papeis(papeis)
    dados = pd.DataFrame([consultar_empresa(papel) for papel in papeis])
    if len(dados[["setor", "subsetor"]].drop_duplicates()) != 1:
        classificacoes = dados[["papel", "setor", "subsetor"]].to_dict(orient="records")
        raise ValueError(f"Escolha empresas do mesmo setor e subsetor. Classificações: {classificacoes}")
    return dados


def baixar_precos(papeis: list[str], inicio: str, fim: str) -> pd.DataFrame:
    papeis = validar_papeis(papeis)
    inicio, fim = date.fromisoformat(inicio), date.fromisoformat(fim)
    if not inicio < fim < date.today():
        raise ValueError("Use início anterior ao fim e fim até ontem, no formato AAAA-MM-DD.")

    # O conector aceita até 5000 barras. Pedimos uma folga para dias sem pregão.
    barras = min(5000, (date.today() - inicio).days + 10)
    series = {}
    for papel in papeis:
        # Sem login: alguns símbolos podem não estar disponíveis no TradingView.
        for tentativa in range(2):
            cliente = TvDatafeed()
            try:
                dados = cliente.get_hist(papel, exchange="BMFBOVESPA",
                                         interval=Interval.in_daily, n_bars=barras)
            finally:
                if cliente.ws is not None:
                    cliente.ws.close()
            if dados is not None and not dados.empty:
                break
            if tentativa == 0:
                print(f"→ Sem dados de {papel}; tentando mais uma vez no TVDatafeed")
        if dados is None or dados.empty or "close" not in dados:
            raise ValueError(f"TVDatafeed não retornou preços de {papel}. Tente novamente mais tarde.")
        fechamento = pd.to_numeric(dados["close"], errors="raise")
        fechamento.index = pd.to_datetime(fechamento.index).normalize()
        if fechamento.index.has_duplicates:
            raise ValueError(f"Há datas duplicadas na série diária de {papel}.")
        series[papel] = fechamento.sort_index().loc[str(inicio):str(fim)]

    # Mesmas datas para todos os papéis; não inventamos preços preenchendo lacunas.
    precos = pd.concat(series, axis=1, join="inner").sort_index().dropna()
    if len(precos) < 2:
        raise ValueError("Não há pelo menos dois fechamentos comuns no período solicitado.")
    if (precos <= 0).any().any() or precos.isin([float("inf"), -float("inf")]).any().any():
        raise ValueError("A fonte retornou preços inválidos; não vou calcular retornos.")
    precos.index.name = "data"
    return precos


def calcular_retornos(precos: pd.DataFrame) -> pd.DataFrame:
    """Variação do fechamento entre a primeira e a última data comum."""
    tabela = pd.DataFrame({
        "preco_inicial_brl": precos.iloc[0],
        "preco_final_brl": precos.iloc[-1],
        "variacao_preco_pct": (precos.iloc[-1] / precos.iloc[0] - 1) * 100,
    })
    tabela.index.name = "papel"
    return tabela.round(4).reset_index()
