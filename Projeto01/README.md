# Projeto 01 — Agente de arquivos e documentos de uma empresa fictícia

Neste projeto, você aprende a montar um agente em um único arquivo Python.
Ele lista, lê e cria arquivos de texto e responde perguntas sobre a empresa
fictícia **Aurora Nuvem**, consultando os documentos da pasta `workspace`.

O modelo é GPT-6 Luna (`gpt-6-luna`), com raciocínio `low` e Responses API.

## Preparação

Na raiz do repositório, crie o ambiente se ainda não existir e instale as dependências:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r Projeto01/requirements.txt
```

Se o ambiente já estiver criado, basta ativá-lo. O `requirements.txt` deste projeto
lista apenas seus três pacotes diretos: LangChain, integração OpenAI e python-dotenv.
Você também pode instalar o `requirements.txt` da raiz para usar as versões completas
do ambiente compartilhado.

Configure a variável no `.env` da raiz ou em `Projeto01/.env`:

```dotenv
OPENAI_API_KEY=sua_chave_aqui
```

## Conversar com o agente

Na raiz, com o ambiente ativo:

```bash
python -m Projeto01.main
```

Também funciona com `python Projeto01/main.py` ou, dentro de `Projeto01`,
com `python main.py`.

O programa fica em um `while True`, recebe perguntas e mostra as respostas.
Digite `sair` para encerrar. Maiúsculas e espaços ao redor são aceitos, como ` SAIR `.
Uma entrada vazia é ignorada. Se uma chamada ao agente falhar, você pode tentar
outro pedido sem reiniciar o programa.

A lista `mensagens` guarda o histórico enquanto o programa está aberto. Assim,
você pode fazer uma pergunta e depois complementar com “e qual é o prazo?”.
Ao fechar o programa, esse histórico é descartado; os arquivos continuam no disco.

## Base fictícia de estudo

Todos os nomes, contatos, regras, clientes e valores são inventados. Os documentos
retratam um cenário de 1º de outubro de 2026, sem representar uma empresa real.

| Arquivo em `workspace` | Conteúdo |
| --- | --- |
| `empresa_indice.md` | Mapa dos documentos e perguntas sugeridas. |
| `empresa_perfil_e_equipe.md` | Empresa, produtos, contatos e pessoas de referência. |
| `empresa_normas_de_trabalho.md` | Jornada, dias presenciais, ausências e equipamentos. |
| `empresa_despesas_e_reembolsos.md` | Limites de despesas, aprovações, viagens e prazos. |
| `empresa_clientes_e_projetos.md` | Clientes, contratos, responsáveis e indicadores simulados. |
| `notas_agentes.md` | Uma introdução aos conceitos de agente e harness. |

Os documentos não treinam o modelo: o agente lê os arquivos pelas ferramentas e
usa o texto como contexto para responder. As instruções pedem que ele cite os
arquivos consultados e reconheça quando a informação não estiver disponível.

## Perguntas para experimentar

- Quantas pessoas trabalham na Aurora Nuvem e quem coordena a engenharia?
- Quais dias são presenciais? Como faço para trocar um dia?
- Quanto posso receber de reembolso por um almoço de R$ 65 em uma viagem aprovada?
- Quem aprova uma compra de R$ 900?
- Qual é o prazo de envio do comprovante e quando começa o prazo de pagamento?
- Quais projetos estão em piloto e quem é o responsável por eles?
- Qual é o faturamento anual da empresa?
- Crie um guia de reembolso em guia_reembolso.md e cite suas fontes.

Algumas respostas para você conferir:

| Pergunta | Resultado esperado |
| --- | --- |
| Tamanho da equipe | 18 pessoas; a tabela de referências contém apenas 6 delas. |
| Compra de R$ 900 | Aprovação prévia de Lia Ramos. |
| Almoço de R$ 65 | Reembolso padrão máximo de R$ 55; exceção exige aprovação prévia de Marina Vale. |
| Envio do comprovante | Até 5 dias úteis após a despesa. |
| Faturamento anual | Informação não disponível na base. |

## Leia o código nesta ordem

Os comentários numerados no `main.py` acompanham seis etapas:

1. Carregar o `.env` e definir a pasta de arquivos.
2. Validar nomes para trabalhar somente dentro de `workspace`.
3. Criar funções e disponibilizá-las ao modelo com `@tool`.
4. Escolher o modelo e configurar o raciocínio.
5. Montar o agente com ferramentas e instruções usando `create_agent`.
6. Manter o loop de conversa e passar o histórico para `invoke`.

| Ferramenta | O que faz |
| --- | --- |
| `listar_arquivos()` | Mostra os nomes dos arquivos disponíveis. |
| `ler_arquivo(nome)` | Retorna o texto de um arquivo. |
| `criar_arquivo(nome, conteudo)` | Salva o texto em um arquivo novo. |

O ciclo executado pelo LangChain é:

```text
Pergunta → modelo → ferramenta → resultado para o modelo → resposta
```

O modelo pode usar várias ferramentas antes de responder. O código imprime os
nomes das ações para você acompanhar esse caminho no terminal.

## Regras simples deste exemplo

- Use arquivos `.md` e `.txt` em UTF-8 e textos pequenos.
- Informe somente o nome, como `resumo.md`; subpastas não são aceitas.
- Arquivos ocultos e links simbólicos são rejeitados.
- O modo `"x"` do `open` impede sobrescrever arquivos existentes.
- `handle_tool_error` devolve os erros esperados ao agente.
- `recursion_limit` limita as etapas de cada pedido.

A lista de mensagens é memória apenas da sessão atual. Este primeiro projeto
mantém o exemplo simples para que busca e memória persistente possam entrar depois.

## O que vai para o Git

Código, documentação, `requirements.txt`, `.env.example` e os materiais fictícios
acompanham o projeto. Chaves, ambientes virtuais, caches, logs e novos arquivos
gerados em `workspace` são ignorados pelo `.gitignore` da raiz.

## Referências

- [Agentes no LangChain](https://docs.langchain.com/oss/python/langchain/agents)
- [Ferramentas no LangChain](https://docs.langchain.com/oss/python/langchain/tools)
- [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna)
