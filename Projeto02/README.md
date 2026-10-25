# Projeto 02 — Um analista financeiro com duas skills

Um agente simples para comparar empresas da B3 do mesmo setor e subsetor:
**fundamentos no Fundamentus** e **variação das cotações pelo TVDatafeed**.
O modelo continua sendo GPT-6 Luna com raciocínio `low`.

O objetivo é ensinar como um harness combina instruções, skills, ferramentas,
fontes externas e cálculos verificáveis. O código está em três arquivos pequenos:
`main.py` organiza a conversa, `dados_mercado.py` coleta e calcula,
e `execucao_python.py` executa o Python gerado pelo agente.

## Preparar e executar

Na raiz do repositório, com Python 3.12 e Git instalados:

```bash
source .venv/bin/activate
python -m pip install -r Projeto02/requirements.txt
python -m Projeto02.main
```

Se ainda não houver ambiente, execute `python3 -m venv .venv` antes de ativá-lo.
Configure `OPENAI_API_KEY` no `.env` da raiz ou em `Projeto02/.env`.
O TVDatafeed é instalado do GitHub em um commit fixado no requirements.

Não é necessário baixar um CSV antes. Os dados são consultados durante a conversa
pela internet. O TVDatafeed é usado sem login; alguns símbolos podem estar limitados.
Também é possível executar `python Projeto02/main.py`. Digite `sair` para encerrar.

Antes de criar o agente, o programa imprime o contexto, as fontes, as capacidades,
as limitações do cálculo e exemplos de perguntas. A abertura não chama a API.

## Um roteiro para o artigo

> Compare os fundamentos de ITUB4, BBDC4 e BBAS3.

> Explique P/L, P/VP e ROE usando os números dessa comparação.

> Compare a variação das cotações dessas empresas de 2025-01-01 a 2025-12-31.

> Faça um gráfico da evolução das cotações em base 100.

> Cruze a comparação de fundamentos com o desempenho passado, explicando as limitações.

> Salve um relatório curto em comparacao_bancos.md.

Os tickers são exemplos de uso das ferramentas. O programa confere a classificação
no Fundamentus, em vez de decidir o setor por memória. Escolha de duas a cinco
empresas e uma classe de ação por empresa, como ITUB4 em vez de ITUB3 e ITUB4 juntas.
Se você não informar o período para os retornos, o agente deve pedir as datas.

## AGENTS.md, skills e ferramentas

| Elemento | Função |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Regras gerais: fontes, unidades, datas, pares comparáveis e uso das ferramentas. |
| [analise-fundamentalista](skills/analise-fundamentalista/SKILL.md) | Método para interpretar os indicadores, com atenção ao setor. |
| [comparar-retornos](skills/comparar-retornos/SKILL.md) | Método para comparar preços no mesmo intervalo e fazer gráficos em base 100. |
| Ferramentas | Funções Python que coletam dados, calculam e salvam arquivos. |

Nosso código lê `AGENTS.md` e o passa para `system_prompt` no `create_agent`.
As skills são lidas pela ferramenta `carregar_skill(nome)` quando o agente precisa
delas. O nome dos arquivos não faz o LangChain carregá-los automaticamente.

| Ferramenta | Resultado |
| --- | --- |
| `carregar_skill(nome)` | Procedimento de fundamentos ou de retornos. |
| `comparar_fundamentos(papeis)` | Indicadores, classificação, fontes, datas e CSV dos fundamentos. |
| `comparar_retornos(papeis, inicio, fim)` | Variação da cotação, período efetivo, fontes e CSV dos preços comuns. |
| `executar_python(codigo)` | Cálculos adicionais e gráficos na `.venv` da raiz. |
| `salvar_relatorio(nome, conteudo)` | Novo relatório Markdown, sem sobrescrever arquivos existentes. |

## Fontes e indicadores

O Fundamentus é lido por HTTPS, com Requests e lxml, preservando os números no
formato brasileiro. `11,43` vira `11.43`; `6,4%` vira `6.4`, mantendo o percentual.
O código não usa o pacote Python `fundamentus`: na versão testada (0.3.2), a conversão
alterou os decimais de alguns múltiplos. O pequeno leitor está em `dados_mercado.py`.

| Campo | Significado e unidade |
| --- | --- |
| `pl` | Preço/lucro, em vezes. |
| `pvp` | Preço/valor patrimonial, em vezes. |
| `roe_pct` | Retorno sobre patrimônio líquido, em %. |
| `dividend_yield_pct` | Dividend yield exibido pela fonte, em %. |
| `margem_liquida_pct` | Margem líquida, em %, quando pertinente. |
| `ev_ebitda` | Valor da firma/EBITDA, em vezes, quando disponível. |
| `cotacao_brl` | Cotação em reais, com sua data. |

Campos ausentes permanecem ausentes. Para bancos, a skill prioriza P/VP e ROE,
contextualiza P/L e DY e não usa EV/EBITDA para classificá-los. Um único indicador
não define a melhor empresa e uma cotação nominal menor não indica desconto.

Cada registro inclui fonte, data de coleta, data da cotação e último balanço
processado. O retrato de uma empresa é reutilizado durante a sessão; reinicie o
programa para consultar novamente. A coleta atual não é um histórico de fundamentos
e não serve como dado conhecido no passado para um backtest.

## O que significa retorno neste projeto

```text
Variação do preço (%) = (fechamento final / fechamento inicial - 1) × 100
Base 100 = fechamento / primeiro fechamento comum × 100
```

O TVDatafeed consulta barras diárias na bolsa `BMFBOVESPA`. O commit utilizado
solicita ajuste por desdobramentos (`splits`). Não coletamos proventos nem
calculamos seu reinvestimento; o resultado não é retorno total com dividendos ou JCP.
Somar o DY atual à variação histórica também não produz esse retorno total.

O cálculo usa somente datas com preços válidos para todas as ações, sem preencher
lacunas. A ferramenta informa o intervalo solicitado e o efetivamente disponível.
Use fim até ontem para evitar uma barra diária ainda aberta. O limite de até
5000 barras, a existência de pregões e a disponibilidade das ações podem reduzir
a cobertura. A conclusão deve respeitar o período efetivo, sem extrapolar.

## Python e gráficos

O executor usa a `.venv` da raiz e recebe cópias dos últimos arquivos coletados:

- `fundamentos`: tabela dos indicadores, com uma linha por papel.
- `precos`: fechamentos no período comum, índice de datas e uma coluna por papel.
- `pd` e `plt`: Pandas e Matplotlib.

Consulte as ferramentas de comparação antes de analisar essas tabelas. Sem coleta,
a tabela correspondente fica vazia. Confira papéis e datas: um arquivo anterior
não é automaticamente o recorte de uma nova pergunta.

Exemplo de código gerado após `comparar_retornos`:

```python
print(precos.index.min(), precos.index.max())
print((precos.iloc[-1] / precos.iloc[0] - 1) * 100)
base100 = precos / precos.iloc[0] * 100
base100.plot(title="Evolução das cotações — base 100")
plt.xlabel("Data")
plt.ylabel("Base 100 no primeiro fechamento comum")
plt.tight_layout()
plt.savefig("comparacao_base100.png")
```

Cada execução cria `resultados/python_<identificador>` com o trecho em `codigo.py`
e os arquivos gerados. O trecho usa as variáveis fornecidas pelo executor. Use
nomes relativos para salvar figuras; a pasta atual já é a pasta dessa execução.
Há limite de 30 segundos e 12.000 caracteres de saída devolvida ao modelo.
As variáveis não persistem entre chamadas.

A execução é local, **não um sandbox de segurança**. A `.venv` organiza bibliotecas;
o código tem as permissões do seu usuário, sem bloqueio de rede ou limite de memória.
As variáveis de ambiente do agente não são repassadas, mas arquivos acessíveis no
computador continuam acessíveis. As instruções orientam o uso, sem impor isolamento.

## Estrutura

```text
Projeto02/
├── main.py
├── dados_mercado.py
├── execucao_python.py
├── AGENTS.md
├── README.md
├── requirements.txt
├── .env.example
├── dados/
│   ├── README.md
│   ├── fundamentos.csv    # Última comparação; local e ignorado pelo Git
│   └── precos.csv         # Último período comum; local e ignorado pelo Git
├── skills/
│   ├── analise-fundamentalista/SKILL.md
│   └── comparar-retornos/SKILL.md
└── resultados/            # Relatórios, código e gráficos; ignorados pelo Git
```

As fontes são serviços externos: mudanças no HTML, restrições de acesso e falhas
podem interromper a coleta. O agente deve explicar a falha e não inventar dados
ou mudar de provedor silenciosamente. Se o TVDatafeed retornar vazio, há somente
uma nova tentativa por papel; uma segunda falha interrompe a comparação.
Os certificados do sistema são usados com
Truststore para o TVDatafeed; a verificação TLS permanece ativa.

## Referências

- [Fundamentus](https://www.fundamentus.com.br/)
- [TVDatafeed: instalação, uso sem login e limite de barras](https://github.com/rongardF/tvdatafeed)
- [Código do conector no commit fixado: ajuste por splits](https://github.com/rongardF/tvdatafeed/blob/e6f6aaa7de439ac6e454d9b26d2760ded8dc4923/tvDatafeed/main.py)
- [Agentes no LangChain](https://docs.langchain.com/oss/python/langchain/agents)
