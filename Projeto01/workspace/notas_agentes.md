# Anotações sobre agentes de IA

Um modelo de linguagem pode gerar texto e solicitar o uso de ferramentas.
Um agente combina o modelo com um ciclo de execução que recebe essas solicitações,
executa as ferramentas e devolve seus resultados ao modelo até concluir uma tarefa.

O harness reúne as instruções, ferramentas, contexto e controles que organizam
essa execução. Neste projeto, ele define as instruções do agente, oferece três
ferramentas e mantém as operações de arquivos dentro de uma pasta de trabalho.

Uma ferramenta precisa ter uma responsabilidade clara, entradas definidas e um
resultado que permita ao agente entender se a operação funcionou.

Arquivos salvos persistem entre execuções. Para usá-los como contexto depois,
o agente precisa descobri-los e lê-los novamente.
