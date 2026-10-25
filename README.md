# Projetos do blog — Harness e inteligência artificial

Este repositório reúne exemplos em Python para estudar agentes de IA do básico
ao avançado. Cada projeto apresenta um passo da construção de um harness: as
instruções, ferramentas, contexto e regras que organizam a execução de um agente.

O foco inicial é código curto, comentado e fácil de experimentar.

## Projetos disponíveis

| Projeto | O que você aprende | Guia |
| --- | --- | --- |
| Projeto01 | Criar três ferramentas, consultar documentos de uma empresa fictícia e manter uma conversa no terminal. | [README do Projeto01](Projeto01/README.md) |
| Projeto02 | Explorar California Housing Prices com Pandas, usar AGENTS.md e uma skill, executar Python e gerar gráficos. | [README do Projeto02](Projeto02/README.md) |

Novos projetos podem acrescentar busca, memória persistente, avaliações e outros
agentes conforme a série avançar. Atualmente, o repositório contém os Projetos 01 e 02.

## Preparar o ambiente

Usamos Python 3.12. Na raiz do repositório, crie e ative o ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Se a pasta `.venv` já existir, basta ativá-la e instalar as dependências.
O `requirements.txt` da raiz registra as versões do ambiente. Cada projeto também
possui seu próprio `requirements.txt` com os pacotes que usa diretamente.

## Configurar a chave da OpenAI

Crie um arquivo `.env` na raiz com:

```dotenv
OPENAI_API_KEY=sua_chave_aqui
```

O arquivo `.env.example` contém apenas o nome da variável para servir de modelo.
Se você já tem um `.env` configurado, mantenha sua chave nele.
Os projetos carregam esse arquivo automaticamente e também aceitam um `.env` na
própria pasta. Para a mesma variável, o arquivo local do projeto tem
prioridade sobre o da raiz; variáveis exportadas no terminal têm prioridade sobre ambos.

O modelo configurado é GPT-6 Luna (`gpt-6-luna`), com raciocínio `low`.
As chamadas ao modelo usam a API da OpenAI.

## Executar o primeiro projeto

Com o ambiente ativo, na raiz:

```bash
python -m Projeto01.main
```

Exemplo de pergunta:

> Na Aurora Nuvem, quem aprova uma compra de R$ 900? Cite o arquivo consultado.

Continue fazendo perguntas no mesmo terminal. Digite `sair` para encerrar.
Para sair do ambiente virtual depois, execute `deactivate`.

## Executar a analista de dados imobiliários

Com o ambiente ativo e o CSV em `Projeto02/dados/housing.csv`:

```bash
python -m Projeto02.main
```

Antes de iniciar o agente, o programa imprime o contexto da base e um resumo dos dados.
Experimente: “Compare os valores dos imóveis por proximidade do oceano e salve um relatório”.
O [guia do Projeto02](Projeto02/README.md) explica o download da base, a skill e o AGENTS.md.
Para gerar gráficos, experimente: “Use Python para explorar a relação entre renda e valor dos imóveis”.
O executor usa a mesma `.venv` da raiz e salva o código e os arquivos em `Projeto02/resultados`.

## Organização

```text
ProjetosBlog/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── Projeto01/
│   ├── README.md
│   ├── requirements.txt
│   ├── main.py
│   └── workspace/         # Documentos fictícios para consulta
└── Projeto02/
    ├── README.md
    ├── requirements.txt
    ├── main.py
    ├── execucao_python.py  # Executor local com a .venv da raiz
    ├── AGENTS.md
    ├── dados/             # CSV original, mantido localmente
    ├── skills/            # Procedimento de análise em SKILL.md
    └── resultados/        # Relatórios gerados
```

## Arquivos locais e Git

O `.gitignore` exclui `.venv`, outros diretórios de ambiente virtual, `.env`,
variações de `.env`, caches Python e logs. Os exemplos `.env.example` podem ser
versionados porque não contêm chaves.

No Projeto01, os documentos fictícios de estudo são versionados. Os demais
arquivos criados em `workspace`, como resumos e rascunhos, ficam apenas na sua máquina.
A pasta de trabalho pode conter exemplos gerados em execuções anteriores.

No Projeto02, o CSV baixado e os relatórios de análise também ficam locais.
As instruções, a skill e os READMEs acompanham o repositório.

Todos os dados da Aurora Nuvem foram inventados para os exercícios.

## Referências

- [Agentes no LangChain](https://docs.langchain.com/oss/python/langchain/agents)
- [Ferramentas no LangChain](https://docs.langchain.com/oss/python/langchain/tools)
- [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna)
