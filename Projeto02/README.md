# Projeto 02 — Uma analista de dados imobiliários com uma skill

Uma evolução do Projeto01: o agente usa Pandas para explorar
[California Housing Prices](https://www.kaggle.com/datasets/camnugent/california-housing-prices).
Vamos estudar qualidade dos dados, comparações e gráficos com código simples.
O modelo continua sendo GPT-6 Luna com raciocínio `low`.

O fluxo está em `main.py`, dividido em sete etapas comentadas. A execução de
Python fica em um pequeno arquivo auxiliar, `execucao_python.py`.

## Executar

Na raiz do repositório, use o ambiente compartilhado:

```bash
source .venv/bin/activate
python -m pip install -r Projeto02/requirements.txt
python -m Projeto02.main
```

Se ainda não houver ambiente, execute `python3 -m venv .venv` antes de ativá-lo.
Configure `OPENAI_API_KEY` no `.env` da raiz ou em `Projeto02/.env`.

O CSV já foi baixado nesta máquina. Em outra máquina, baixe `housing.csv` do
Kaggle e coloque em `Projeto02/dados/housing.csv`. O [guia dos dados](dados/README.md)
explica as colunas e o download. O CSV e os resultados estão ignorados pelo Git.

Também funciona com `python Projeto02/main.py` ou, dentro de `Projeto02`,
`python main.py`. Digite `sair` para encerrar. O histórico da conversa dura
enquanto o programa estiver aberto.

## O que aparece antes do agente

Antes de criar o agente, `mostrar_contexto()` usa Pandas e `print` para explicar
a base e mostrar um resumo calculado localmente. Essa abertura não chama a API.
Ela apresenta:

- O contexto: moradia na Califórnia, com dados do censo de 1990.
- A unidade de análise: cada linha é um grupo censitário, não uma casa individual.
- A quantidade de linhas, colunas e categorias de proximidade do oceano.
- Os valores ausentes e a média das medianas dos valores dos imóveis.
- As capacidades do agente e algumas perguntas para começar.

Na versão baixada, há **20.640 linhas, 10 colunas e 207 valores ausentes em
`total_bedrooms`**. Os dados históricos não representam os preços atuais.

## Primeiros pedidos

> Faça um resumo da base e explique as principais colunas.

> Quais colunas têm valores ausentes? Como isso afeta uma análise?

> Qual é a média de quartos?

Nesse pedido, o agente deve esclarecer se você quer a média por domicílio ou
o total médio por grupo censitário antes de calcular.

> Compare os valores dos imóveis por proximidade do oceano. Mostre o tamanho de cada grupo.

> Use Python para investigar a relação entre renda mediana e valor mediano dos imóveis. Salve um gráfico.

> Faça um mapa de dispersão usando longitude e latitude, com as cores indicando median_house_value.

> Salve um relatório da comparação em analise_imoveis.md.

> Podemos comparar os preços de 1990 com os de 2025 usando apenas essa base?

As ferramentas aparecem no terminal. Na primeira análise, o agente deve carregar
a skill e consultar o resumo antes de apresentar suas conclusões.

## Instruções, skill e ferramentas

| Elemento | Responsabilidade neste projeto |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Define papel, fonte dos dados e acordos gerais para toda a conversa. |
| [SKILL.md](skills/analise-imoveis/SKILL.md) | Ensina o procedimento de análise e a interpretação das estatísticas. |
| Ferramentas em `main.py` | Executam os cálculos, o Python e a gravação de relatórios. |

O nome `AGENTS.md`, sozinho, não configura o LangChain. Nosso código lê esse
arquivo e passa o texto para `system_prompt` no `create_agent`.

O conteúdo completo da skill entra na conversa quando o modelo chama
`carregar_skill`. Isso demonstra **carregamento sob demanda**: no início, o
agente recebe uma descrição curta; o procedimento detalhado é lido quando necessário.
Essa skill pertence à aplicação e é carregada explicitamente pelo nosso código.

| Ferramenta | O que faz |
| --- | --- |
| `carregar_skill()` | Lê o procedimento `analise-imoveis`. |
| `resumo_dados()` | Mostra colunas, qualidade, distribuição das categorias e estatísticas dos valores medianos. |
| `comparar_regioes()` | Compara as categorias de `ocean_proximity`, com contagem, média e mediana. |
| `executar_python(codigo)` | Faz análises personalizadas e gráficos na `.venv` da raiz. |
| `salvar_relatorio(nome, conteudo)` | Cria um Markdown em `resultados`, sem sobrescrever relatórios. |

Apesar do nome `comparar_regioes`, o agrupamento é por proximidade aproximada do
oceano. As categorias não são cidades nem regiões administrativas.

## Entendendo os números

`median_house_value` é o valor mediano dos imóveis de cada grupo censitário, em USD.
Por isso, os cálculos sobre essa coluna têm um significado específico:

```text
Quantidade de linhas = quantidade de grupos censitários
Média de median_house_value = média das medianas desses grupos
Mediana de median_house_value = mediana das medianas desses grupos
```

Cada grupo recebe o mesmo peso. Essas estatísticas não são automaticamente a
média ou mediana dos preços de todas as casas. Somar as medianas também não
produz o valor total do mercado imobiliário.

Os totais de cômodos, quartos, população e domicílios pertencem ao grupo inteiro.
`total_rooms` significa **cômodos**; `total_bedrooms`, **quartos de dormir**.
Uma média por grupo é diferente de uma razão de quartos por domicílio. Para
essa razão, somamos quartos e domicílios no mesmo recorte de registros válidos
e dividimos os totais. Valores ausentes de quartos não são tratados como zero.

`median_income` permanece na escala original da base; os valores crus não devem
ser rotulados diretamente como dólares. A base não tem série temporal ou
endereços individuais. Ao comparar categorias, confira o tamanho da amostra:
`ISLAND`, por exemplo, tem apenas cinco registros na versão baixada.

## Python na .venv da raiz

O projeto e o executor usam a mesma `.venv` da raiz. A ferramenta inicia outro
processo com `.venv/bin/python`, que já recebe:

- `df`: DataFrame com uma cópia dos dados completos e as dez colunas originais.
- `pd`: Pandas.
- `plt`: Matplotlib, configurado para salvar gráficos sem abrir uma janela.

Exemplo de código que o agente pode executar:

```python
colunas = ["median_income", "median_house_value"]
print(df[colunas].corr(method="pearson"))
df.plot.scatter(x="median_income", y="median_house_value", alpha=0.15)
plt.title("Renda e valor mediano dos imóveis — censo de 1990")
plt.xlabel("Renda mediana (escala original da base)")
plt.ylabel("Valor mediano do grupo censitário (USD)")
plt.tight_layout()
plt.savefig("renda_e_valor.png")
```

Cada chamada cria uma pasta `resultados/python_<identificador>` com o trecho
gerado em `codigo.py` e os arquivos da análise. Esse trecho usa `df`, `pd` e `plt`
fornecidos pelo executor. Use nomes relativos, como `grafico.png`, para salvar
na pasta da execução. A ferramenta devolve status, saída impressa e arquivos.

O limite é de 30 segundos por execução e 12.000 caracteres de saída devolvida.
As variáveis não persistem entre chamadas; cada análise começa com os dados completos.
O histórico da conversa e os arquivos gerados permanecem disponíveis.

É execução local, **não um sandbox de segurança**. A `.venv` organiza bibliotecas;
o código mantém as permissões do seu usuário, sem bloqueio de rede ou limite de
memória. As variáveis de ambiente do agente, incluindo a chave da API, não são
repassadas ao subprocesso; arquivos acessíveis no computador continuam acessíveis.
O AGENTS.md orienta o uso, mas não impõe isolamento. O fluxo normal usa uma cópia
temporária do CSV e mantém o original intacto.

## Estrutura

```text
Projeto02/
├── main.py
├── execucao_python.py
├── AGENTS.md
├── README.md
├── requirements.txt
├── .env.example
├── dados/
│   ├── README.md
│   └── housing.csv        # Local, ignorado pelo Git
├── skills/
│   └── analise-imoveis/
│       └── SKILL.md
└── resultados/            # Relatórios, código e gráficos; ignorados pelo Git
```

## Experimentos para estudar

1. Execute o programa e leia a abertura antes de enviar uma pergunta.
2. Compare as regras gerais do `AGENTS.md` com o procedimento do `SKILL.md`.
3. Peça uma comparação por proximidade do oceano e acompanhe as ferramentas.
4. Faça uma pergunta complementar para observar o histórico.
5. Peça um gráfico, abra o `codigo.py` gerado e compare com a figura.
6. Salve um relatório e confira os números nas respostas das ferramentas.

A versão atual faz análise descritiva. Uma próxima etapa pode introduzir
limpeza de dados, treinamento de modelos e avaliação, cada um com sua própria skill.

## Referências

- [California Housing Prices no Kaggle](https://www.kaggle.com/datasets/camnugent/california-housing-prices)
- [Origem e descrição da versão didática, por Aurélien Géron](https://github.com/ageron/handson-ml2/tree/master/datasets/housing)
- [Padrão de skills no LangChain](https://docs.langchain.com/oss/python/langchain/multi-agent/skills)
- [Ferramentas no LangChain](https://docs.langchain.com/oss/python/langchain/tools)
