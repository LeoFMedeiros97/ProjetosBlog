# Projetos do blog — Harness e inteligência artificial

Este repositório reúne exemplos em Python para estudar agentes de IA do básico
ao avançado. Cada projeto apresenta um passo da construção de um harness: as
instruções, ferramentas, contexto e regras que organizam a execução de um agente.

O foco inicial é código curto, comentado e fácil de experimentar.

## Projetos disponíveis

| Projeto | O que você aprende | Guia |
| --- | --- | --- |
| Projeto01 | Criar três ferramentas, consultar documentos de uma empresa fictícia e manter uma conversa no terminal. | [README do Projeto01](Projeto01/README.md) |

Novos projetos podem acrescentar busca, memória persistente, avaliações e outros
agentes conforme a série avançar. Atualmente, o repositório contém o Projeto01.

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
O Projeto01 carrega esse arquivo automaticamente e também aceita um `.env` na
própria pasta do projeto. Para a mesma variável, o arquivo local do projeto tem
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

## Organização

```text
ProjetosBlog/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
└── Projeto01/
    ├── README.md
    ├── requirements.txt
    ├── main.py
    └── workspace/
        ├── empresa_indice.md
        ├── empresa_perfil_e_equipe.md
        ├── empresa_normas_de_trabalho.md
        ├── empresa_despesas_e_reembolsos.md
        ├── empresa_clientes_e_projetos.md
        └── notas_agentes.md
```

## Arquivos locais e Git

O `.gitignore` exclui `.venv`, outros diretórios de ambiente virtual, `.env`,
variações de `.env`, caches Python e logs. Os exemplos `.env.example` podem ser
versionados porque não contêm chaves.

No Projeto01, os documentos fictícios de estudo são versionados. Os demais
arquivos criados em `workspace`, como resumos e rascunhos, ficam apenas na sua máquina.
A pasta de trabalho pode conter exemplos gerados em execuções anteriores.

Todos os dados da Aurora Nuvem foram inventados para os exercícios.

## Referências

- [Agentes no LangChain](https://docs.langchain.com/oss/python/langchain/agents)
- [Ferramentas no LangChain](https://docs.langchain.com/oss/python/langchain/tools)
- [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna)
