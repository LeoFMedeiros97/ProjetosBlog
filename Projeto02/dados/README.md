# Dados do Projeto02

Os arquivos são criados pelas ferramentas do agente, sem download manual:

| Arquivo | Conteúdo | Fonte |
| --- | --- | --- |
| `fundamentos.csv` | Última comparação de indicadores de empresas do mesmo setor e subsetor. | Fundamentus, páginas de detalhes de cada papel. |
| `precos.csv` | Última comparação de fechamentos diários em datas comuns. | TradingView via TVDatafeed, bolsa BMFBOVESPA. |

`fundamentos.csv` inclui ticker, empresa, setor, subsetor, cotação, data da cotação,
último balanço, P/L, P/VP, ROE, DY, margem líquida, EV/EBITDA, coleta e URL da fonte.
Campos `_pct` já representam percentuais: 6.4 significa 6,4%. Campos indisponíveis
ficam vazios, sem serem transformados em zero. Os indicadores são um retrato atual.

`precos.csv` tem a coluna `data` e uma coluna de fechamento por papel. As linhas
já estão no intervalo comum usado no cálculo. O conector solicita ajuste por
splits; não há coleta de proventos nem cálculo de retorno total com reinvestimento.
As datas solicitadas e efetivas aparecem na resposta da ferramenta.

Uma nova comparação substitui o CSV correspondente; os gráficos e relatórios
ficam em pastas próprias dentro de `resultados`. A tabela de fundamentos por
empresa é reutilizada na memória durante a sessão. Reinicie para uma nova coleta.

O executor Python lê cópias temporárias desses dois arquivos. Os CSVs, arquivos
ZIP e resultados ficam ignorados pelo Git. Arquivos de bases usadas em versões
anteriores, se ainda estiverem nesta pasta, não são lidos pelo projeto atual.

Fontes: [Fundamentus](https://www.fundamentus.com.br/),
[TVDatafeed](https://github.com/rongardF/tvdatafeed).
