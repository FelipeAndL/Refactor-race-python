# Comparativo de métricas

## Escopo e fonte dos dados

Este comparativo usa:

- a linha de base registrada em [`testes iniciais.md`] e
  [`diagnostico inicial.md`];
- uma nova execução sobre [`src/legacy_checkout.py`] e
  [`tests/test_checkout.py`].

Os comandos atuais foram executados com `PYTHONPATH=src`:

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src pytest --cov=legacy_checkout --cov-report=term
python -m radon cc src/legacy_checkout.py -s -a
python -m radon mi src/legacy_checkout.py -s
python -m ruff check src/legacy_checkout.py --statistics
```

## Comparação

| Indicador | Linha de base | Resultado atual | Variação | Avaliação objetiva |
|---|---:|---:|---:|---|
| Quantidade de testes | 4 | 4 | 0 | **Sem alteração** |
| Testes aprovados | 4/4 | 4/4 | 0 | **Mantido: 100% aprovados** |
| Cobertura | 83% (72 instruções, 12 não cobertas) | 95% (74 instruções, 4 não cobertas) | **+12 pontos percentuais** | **Melhorou** |
| Complexidade de `process_order` | E (34) | A (1) | **-33 pontos; E → A** | **Melhorou substancialmente** |
| Complexidade média do módulo | E (34,0) | A (2,75) | **-31,25 pontos; E → A** | **Melhorou substancialmente** |
| Manutenibilidade Radon | A (51,69) | A (41,07) | -10,62 pontos | **Classificação mantida; índice numérico piorou** |
| Problemas encontrados pelo Ruff | 4: 3 `SIM102` e 1 `PLR1730` | 0 | **-4; 100% eliminados** | **Melhorou** |

## Indicadores que melhoraram

1. **Cobertura:** passou de 83% para 95%, reduzindo os trechos não cobertos de
   12 para 4 instruções.
2. **Complexidade:** `process_order` passou de complexidade E (34) para A (1).
   Após a decomposição em funções auxiliares, a média do módulo passou de E
   (34,0) para A (2,75).
3. **Qualidade estática:** o Ruff passou de 4 problemas para 0. Foram
   eliminadas as três ocorrências `SIM102` e a ocorrência `PLR1730`.

## Indicadores sem melhora ou que exigem atenção

- **Quantidade de testes:** permaneceu em 4. Portanto, a cobertura melhorou
  sem aumento da quantidade de casos de teste; os cenários de entrada inválida,
  cupons adicionais, frete expresso e estado global continuam sem validação
  específica.
- **Testes aprovados:** permaneceu em 4 de 4. A suíte continua verde, mas isso
  não representa aumento de abrangência funcional.
- **Manutenibilidade:** a classificação qualitativa continuou em **A**, porém o
  índice numérico caiu de **51,69 para 41,07**. Assim, não é correto afirmar
  melhora nesse indicador apenas com base na letra da classificação.

## Conclusão

Os indicadores de **cobertura**, **complexidade** e **problemas do Ruff**
melhoraram objetivamente. A suíte preservou os quatro testes existentes, todos
aprovados, mas não cresceu em quantidade. A **manutenibilidade permaneceu na
faixa A**, embora o valor numérico do Radon tenha diminuído e deva ser
acompanhado em próximas alterações.
