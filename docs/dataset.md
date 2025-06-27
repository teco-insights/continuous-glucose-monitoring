## 📊 Base de Dados Utilizada

A base de dados utilizada contém **2713 linhas e 7 variáveis** e foi extraída do [rdrr.io – psi-shiny-cgm](https://rdrr.io/github/personalscience/psi-shiny-cgm/man/sample_libreview_df.html), repositório de documentação de pacotes do R.

- **Período de medição:** 01/05/2021 até 02/06/2021  
- **Intervalo entre medições:** 15 minutos  
- **Valores de glicemia (mg/dL):** variam entre **40 e 223**

---

## 🧬 Dicionário de Dados

| Variável   | Tipo      | Obrigatório | Descrição |
|------------|-----------|-------------|-----------|
| `time`     | `datetime`| ✅           | Data e hora exata da medição da glicemia no fluido intersticial (intervalo de 15 minutos). Ex: `"2021-05-30 16:59:00"` |
| `scan`     | `int`     | ❌           | Valor da glicose (mg/dL) obtido por escaneamento manual via leitor ou smartphone. Apenas o último escaneamento do intervalo de 15 minutos é mantido. Ex: `100` |
| `hist`     | `int`     | ❌           | Média ponderada dos últimos valores de glicose automáticos. Suaviza variações súbitas e ruídos. Ex: `100` |
| `strip`    | `int`     | ❌           | Valor da glicose (mg/dL) obtido por teste capilar (ponta de dedo). Método referência para confirmação de hipo/hiperglicemia. Ex: `100` |
| `value`    | `int`     | ✅           | Melhor valor de glicemia disponível. Prioridade: `strip ∨ scan ∨ hist`. Ex: `100` |
| `food`     | `string`  | ❌           | Anotação textual sobre alimento consumido no momento da medição. Ex: `"Macarrão com feijão"` |
| `user_id`  | `int`     | ✅           | Identificador único do usuário. Ex: `1234` |

---

## 🔁 Lógica da variável `value`
```text
value = strip ∨ scan ∨ hist
```
O valor da glicemia é escolhido com base na disponibilidade dos dados, com a seguinte prioridade:
1. strip (teste capilar)
2. scan (escaneamento manual)
3. hist (automático suavizado)
