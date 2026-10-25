---
name: analise-imoveis
description: Explore California Housing Prices com Pandas e Matplotlib. Use para resumir a base, avaliar valores ausentes, comparar proximidade do oceano, explorar correlações e produzir gráficos e relatórios descritivos.
---

# Análise de dados imobiliários

Use `resumo_dados` para conhecer as colunas, o número de linhas, os valores ausentes,
as duplicatas e a distribuição das categorias. A fonte é `dados/housing.csv`,
California Housing Prices, com referência no censo de 1990.

## Entenda a unidade de análise

- Cada linha representa um grupo censitário, chamado de distrito em alguns materiais.
  Não conte linhas como se fossem imóveis, famílias ou transações.
- `median_house_value` é a mediana dos valores dos imóveis daquele grupo, em USD.
  A média calculada sobre essa coluna é uma média das medianas dos grupos, sem
  ponderação. A mediana calculada sobre ela é uma mediana das medianas.
  Nenhuma delas equivale automaticamente à média ou mediana de todas as casas.
- `total_rooms` é o total de cômodos; `total_bedrooms` é o total de quartos de
  dormir. Preserve essa diferença na tradução. `population` é a população e
  `households` é a quantidade de domicílios. Todos são totais por grupo,
  não características de uma única casa.
- `median_income` está na escala original fornecida pela base. Identifique essa
  escala nos eixos e tabelas; não rotule os valores crus como USD.
- `housing_median_age` é uma idade mediana em anos. Longitude e latitude permitem
  visualizar a distribuição geográfica, sem identificar endereços individuais.

## Escolha a média certa

Confirme a coluna e a unidade antes de calcular. Uma pergunta como “qual é a
média de quartos?” identifica bedrooms, mas ainda não define o denominador.
Pergunte de forma simples: “Você quer a média de quartos por domicílio ou o
total médio de quartos por região (grupo censitário)?”

- Por grupo censitário: calcule a média de `total_bedrooms`. Informe os registros
  válidos e ausentes. Não use `total_rooms` para responder sobre quartos.
- Por domicílio: calcule a razão entre a soma de `total_bedrooms` e a soma de
  `households`, usando em ambas as somas o mesmo recorte: valores presentes nas
  duas colunas e `households > 0`. Explique que é uma razão dos totais agregados,
  não uma medição individual de cada casa. Não divida por domicílios de grupos
  cujos quartos estão ausentes, nem preencha esses quartos com zero.
- A média simples das razões de cada grupo é outro indicador: ela dá peso igual
  aos grupos. Use-a somente quando esse critério for solicitado e explique a diferença.

Não apresente médias por grupo como médias por casa. Evite uma conclusão antes
de resolver a ambiguidade; uma pergunta curta é suficiente.

## Qualidade e comparação

Mencione valores ausentes quando afetarem o cálculo. Não remova nem preencha
dados automaticamente. Pandas geralmente ignora nulos ao calcular médias;
informe a quantidade de observações válidas se analisar uma coluna incompleta.

Use `comparar_regioes` para agrupar por `ocean_proximity`. As categorias são
`<1H OCEAN`, `INLAND`, `NEAR OCEAN`, `NEAR BAY` e `ISLAND`. Elas descrevem uma
proximidade aproximada do oceano, não cidades ou regiões administrativas.
Mostre a quantidade de grupos censitários ao lado das estatísticas. Um grupo
com poucas observações exige cuidado: confira especialmente a categoria ISLAND.

Observe extremos e concentrações no maior valor registrado de
`median_house_value`. Não afirme que esse é o imóvel mais caro da Califórnia.
Declare filtros e critérios usados para faixas de renda, idade ou localização.

## Entrega

Para um cruzamento não atendido por `comparar_regioes`, uma estatística diferente ou um
gráfico, use `executar_python`. O ambiente já possui `df`, `pd` e `plt`.
O DataFrame contém as dez colunas originais de `housing.csv`. Para correlações,
selecione as colunas numéricas e explique qual coeficiente foi utilizado.
Não crie uma evolução mensal ou anual: a base não tem uma série temporal.

Prefira código curto e imprima a tabela que sustenta a conclusão. Para um gráfico,
adicione título, rótulos e `plt.tight_layout()` antes de `plt.savefig('nome.png')`.
Informe ao usuário a pasta e os arquivos retornados pela ferramenta.
Use nomes relativos, pois o diretório atual já é a pasta de resultados da execução.
As variáveis não persistem entre chamadas; cada nova análise precisa conter todo
o código necessário. As mensagens e os arquivos gerados permanecem disponíveis.

A ferramenta retorna status e saída. Se houver erro, use a mensagem para corrigir
o código; uma execução interrompida não confirma o cálculo ou a criação do gráfico.

Apresente os números calculados, o ano de referência, a fonte e uma conclusão
apoiada nesses resultados. Uma correlação ou diferença entre grupos não comprova
causa nem descreve necessariamente cada morador. Esta skill faz análise
descritiva de dados históricos, não avaliação de imóveis atuais ou previsão.

Quando solicitado, salve um Markdown com objetivo, ano e fonte, indicadores,
comparações, critérios e limitações usando `salvar_relatorio`.
