# Dados do Projeto02

Fonte: [California Housing Prices, publicado por Cam Nugent no Kaggle](https://www.kaggle.com/datasets/camnugent/california-housing-prices).

O arquivo esperado é `housing.csv`. A versão baixada em 24 de outubro de 2026
tem **20.640 linhas e 10 colunas**. O arquivo fica local e está ignorado pelo Git.

## Obter os dados

1. Abra o link da fonte e baixe o conjunto de dados.
2. Extraia `housing.csv` do ZIP.
3. Coloque o arquivo nesta pasta, ao lado deste README.

## Contexto e colunas

Os dados têm origem no censo de 1990 da Califórnia. Cada linha corresponde a
um grupo censitário, uma pequena área geográfica com vários domicílios.
É uma base histórica e agregada, sem preços atuais ou endereços individuais.
A [descrição de Aurélien Géron](https://github.com/ageron/handson-ml2/tree/master/datasets/housing)
explica a origem e as alterações da versão didática.

| Coluna | Significado |
| --- | --- |
| longitude, latitude | Coordenadas geográficas do grupo. |
| housing_median_age | Idade mediana das moradias, em anos. |
| total_rooms | Total de cômodos no grupo. |
| total_bedrooms | Total de quartos no grupo; há 207 valores ausentes. |
| population | População do grupo. |
| households | Quantidade de domicílios do grupo. |
| median_income | Renda mediana na escala original fornecida pela base. |
| median_house_value | Valor mediano dos imóveis do grupo, em USD. |
| ocean_proximity | Categoria de proximidade aproximada do oceano. |

O programa mantém as colunas e os valores ausentes originais. A média de
`median_house_value` é uma média das medianas dos grupos, sem ponderação,
e não o preço médio de todas as casas. Para uso e redistribuição, consulte
os termos apresentados pelo publicador da base.
