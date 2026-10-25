---
name: analise-fundamentalista
description: Compare fundamentos de empresas da B3 do mesmo setor e subsetor usando o Fundamentus. Use para perguntas sobre P/L, P/VP, ROE, dividend yield, margem líquida e EV/EBITDA.
---

# Comparar fundamentos

Use `comparar_fundamentos` com os tickers escolhidos, por exemplo ITUB4, BBDC4 e
BBAS3. A ferramenta confirma setor e subsetor e salva `dados/fundamentos.csv`.
Não compare empresas de setores distintos como se fossem pares. Se o pedido
não identificar as empresas, peça os tickers; não selecione pares por memória.

## Ler os indicadores

- `pl`: preço/lucro, em vezes. Negativo indica lucro negativo na base do indicador;
  não interprete como desconto. Um múltiplo isolado não mede qualidade ou valor justo.
- `pvp`: preço/valor patrimonial, em vezes; depende da natureza dos ativos e do setor.
- `roe_pct`: retorno sobre patrimônio líquido, em %. Considere o patrimônio e
  possíveis efeitos não recorrentes antes de associar ROE alto a desempenho melhor.
- `dividend_yield_pct`: rendimento passado dos proventos conforme a fonte, em %.
  Não é projeção de dividendos nem retorno total do período solicitado.
- `margem_liquida_pct`: margem líquida em %, quando disponível e pertinente ao setor.
- `ev_ebitda`: valor da firma/EBITDA, em vezes. Não use esse múltiplo para classificar
  bancos; para bancos, priorize P/VP e ROE, contextualizando também P/L e DY.

Os campos `_pct` já vêm como percentuais: 6.4 deve aparecer como 6,4%, sem
multiplicar por 100. Valores ausentes devem aparecer como “não disponível”, nunca zero.
Campos zerados também exigem interpretação; uma margem exibida como zero para um
banco não basta para concluir que ele não teve lucro.

## Explicar a comparação

Mostre uma tabela com os papéis, os indicadores pertinentes e as datas de cotação
e do último balanço. Informe a fonte e a coleta. Datas diferentes podem tornar a
comparação menos homogênea. Os dados são um retrato atual, não um histórico de
fundamentos: não os use em um backtest como se estivessem disponíveis no passado.

Descreva diferenças observadas: menor múltiplo, maior ROE ou maior DY segundo a
fonte. Explique os trade-offs; não escolha “a melhor ação” a partir de um único
indicador. A avaliação não inclui todos os riscos, eventos e demonstrações de uma empresa.

Para cálculos adicionais ou gráficos, use `executar_python`, que recebe a tabela
`fundamentos`. Confira os tickers antes de usar o último arquivo coletado.
Se o usuário pedir relatório, use `salvar_relatorio` e inclua objetivo, pares,
fontes/datas, tabela, interpretação e limitações.
