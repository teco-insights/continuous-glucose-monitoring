
## 🗑💎 O Processo de Limpeza (ou Lapidação) dos Dados

O primeiro passo de nossa limpeza foi copiar o dataframe original sample_libreview_df_raw, para o objeto **df_raw**, com nome mais simples e no qual poderíamos fazer todas as transformações necessárias sem perdermos de vista nossa fonte original. ✅

Como já planejávamos uma análise simples, a maior parte das variáveis originais só nos seriam úteis num primeiro momento, principalmente para corrigir alguma informação imprecisa, como uma medição com valor em 'scan' e sem valor em 'value', o que é contrário à própria definição de 'value'.
Inicialmente, então, tornamos minúsculas todas as letras dos nomes das variáveis, assim como removemos espaços e os dois pontos, que poderiam prejudicar os chamados aos objetos. 😵

A coluna 'time' é **fundamental**. Ela nos acompanha durante todo o projeto, e dela se derivam outras várias colunas importantes. Por isso, nos certificamos de imediato que ela realmente estivesse no formato datetime, e que qualquer elemento fora desse formato, e que não pudesse ser convertido para ele, fosse identificado como *NaT* (consideramos sem sentido uma medição sem data).

'value' deveria ser uma coluna de valores numéricos, então fizemos o mesmo procedimento de validação de dados para ela. Como já mostrado no arquivo dataset, value = strip ∨ scan ∨ hist. Baseado nesse fundamento, uma operação de varredura das linhas vazias de 'value' foi feita. Para cada linha vazia desta coluna, foi atribuído (havendo este) um valor de uma das outras colunas ('strip', 'scan' ou 'hist'), considerando-se a ordem estabelecida. Deixamos uma única medição pra um mesmo horário, pra evitar contagens duplas 👯‍♀️. Tudo isso foi resolvido com a função *value_herda_exclui()*.

❗ **OBS importante**: Ao excluir uma linha, sempre lembre-se de resetar o índices das linhas, pois isto não é feito automaticamente. Por exemplo, tendo-se as linhas 0, 1 e 2 em um dataframe, ao remover a linha 1, ficam as linhas de índices 0 e 2, ao invés de se alterar o índice da linha 2 diretamente para 1. Então, após a remoção, visualmente duas linhas estão disponíveis, 0 e 1, mas o índice da linha 1 ainda é 2, se não tiver sido resetado. Isso induz a muitos erros!! 😓

Neste momento, ficamos só com as variáveis 'value' e 'time', e excluímos qualquer linha com valor nulo em uma ou ambas as colunas, assim como valores absurdos em 'value', que não condizem com informações médicas de glicemia, através da função *elimina_nulos_ruidos()*.
Aqui, cabe um pequeno esclarecimento: Embora a variável user_id seja obrigatória, como estamos analisando apenas as medições de um único usuário, **neste contexto**, e apenas neste, não faremos uso dela.

❗❗ Quando nos referimos a valores absurdos em 'value', estamos considerando valores absolutos muito altos ou baixos, ou mesmo valores **muito** diferentes dos valores próximos no tempo, como por exemplo, uma medição de 150 precedida por uma de 80 e seguida por uma de 90, com intervalos de 15 minutos para ambas. Isso é inviável medicamente, e muito provavelmente pode ser fruto de um ruído no aparelho medidor. 💥

Como introduzimos, 'time' geraria outras variáveis, e nosso último passo na limpeza e validação foi justamente criar estas importantes colunas e ordená-las: 'date', 'date_cont', 'hour_minute', 'weekday', 'hour', 'hour_cont' e 'time_of_day'.
Adicionamos até a penúltima delas utilizando a função *dividir_time()*, para que o mesmo possa ser feito com qualquer dataframe que tenha uma coluna do tipo datatime.

Resumo das novas variáveis:

* date: data, sem as horas. datetime64[ns];
* date_cont: contagem de dias, do dia 0 até o útimo (51) int64;
* hour_minute: a hora e minuto da medição. object;
* weekday: o dia da semana. object;
* hour: somente a hora da medição, sem os minutos. int32;
* hour_cont: a hora de maneira contínua (como 14:30 = 14,5). float64;
* time_of_day: o momento do dia correspondente às horas (23 horas = late_night, 3h = small_hours). object.

Agora, **df_raw** está pronto para a análise exploratória e modelagens! 🤗🥳