---
name: comparar-retornos
description: Compare a variação de preços históricos de ações da B3 com TVDatafeed e gráficos em base 100. Use para retornos entre datas, evolução das cotações e comparação de desempenho passado.
---

# Comparar retornos

Defina os tickers, início e fim. Se o período estiver ausente, peça-o antes de
calcular. Use `comparar_retornos` com datas AAAA-MM-DD e fim até ontem, evitando
uma barra diária ainda aberta. A ferramenta confirma setor e subsetor e usa
somente datas com preços disponíveis para todas as empresas.

## Interpretar o cálculo

```text
Variação do preço (%) = (fechamento final / fechamento inicial - 1) × 100
Base 100 = fechamento / primeiro fechamento comum × 100
```

O TVDatafeed consulta barras diárias do TradingView na bolsa BMFBOVESPA.
A versão fixada solicita ajuste por desdobramentos (splits), não reinvestimento
de proventos. Apresente o resultado como variação da cotação fornecida.
Não o chame de retorno total com dividendos ou JCP, e não some o DY atual a ele.

Informe o período solicitado, o efetivamente usado e a quantidade de observações
comuns. Feriados, faltas de dados e o limite de até 5000 barras podem reduzir o
período. Não preencha lacunas nem compare datas iniciais diferentes entre ações.
Se a cobertura for menor, restrinja a conclusão ao período disponível.

## Gráfico e conclusão

Após a comparação, `executar_python` recebe `precos` com índice de datas e uma
coluna por papel, já no período comum. Para comparar trajetórias:

```python
base100 = precos / precos.iloc[0] * 100
print((precos.iloc[-1] / precos.iloc[0] - 1) * 100)
base100.plot(title="Evolução das cotações — base 100")
plt.xlabel("Data")
plt.ylabel("Base 100 no primeiro fechamento comum")
plt.tight_layout()
plt.savefig("comparacao_base100.png")
```

Confira os papéis e as datas do DataFrame antes de usar o último CSV. Cada chamada
Python começa do zero. Confira o status e os arquivos retornados antes de anunciar
a figura. Não trate a trajetória passada como previsão.

Se cruzar com fundamentos, diferencie o retrato atual dos indicadores e o intervalo
histórico dos preços. A comparação não demonstra que os indicadores atuais
explicaram ou causaram o retorno passado. Quando solicitado, salve um relatório
com fontes, datas, cálculo, tabela, gráfico e limitações.
