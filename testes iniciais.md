# Testes iniciais

## Código executado

Os comandos foram ajustados para usar os arquivos existentes no projeto:

- módulo: `src/legacy_checkout.py`
- testes: `tests/test_checkout.py`
- `PYTHONPATH=src` para permitir a importação do módulo pelos testes

```bash
print("\n=== COBERTURA ===")
PYTHONPATH=src pytest --cov=legacy_checkout --cov-report=term

print("\n=== COMPLEXIDADE ===")
radon cc src/legacy_checkout.py -s -a

print("\n=== MANUTENIBILIDADE ===")
radon mi src/legacy_checkout.py -s

print("\n=== QUALIDADE ===")
ruff check src/legacy_checkout.py --statistics
```

## Resultado

### Cobertura

```text
============================= test session starts ==============================
platform linux -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
plugins: cov-7.1.0
collected 4 items

tests/test_checkout.py ....                                              [100%]

================================ tests coverage ================================
_______________ coverage: platform linux, python 3.14.7-final-0 ________________

Name                     Stmts   Miss  Cover
--------------------------------------------
src/legacy_checkout.py      72     12    83%
--------------------------------------------
TOTAL                       72     12    83%
============================== 4 passed in 0.03s ===============================
```

**Status:** passou. 4 testes aprovados, com 83% de cobertura.

### Complexidade

```text
src/legacy_checkout.py
    F 6:0 process_order - E (34)

1 blocks (classes, functions, methods) analyzed.
Average complexity: E (34.0)
```

**Resultado:** a função `process_order` foi classificada como complexidade **E**, com índice 34.

### Manutenibilidade

```text
src/legacy_checkout.py - A (51.69)
```

**Resultado:** índice de manutenibilidade **A (51.69)**.

### Qualidade

```text
3	SIM102 	[ ] collapsible-if
1	PLR1730	[*] if-stmt-min-max
Found 4 errors.
[*] 1 fixable with `--fix` (2 unsafe fixes available with `--fix --unsafe-fixes`).
```

**Status:** falhou na verificação de qualidade. Foram encontrados 4 problemas:

- 3 ocorrências de `SIM102` (`collapsible-if`);
- 1 ocorrência de `PLR1730` (`if-stmt-min-max`);
- 1 dos problemas pode ser corrigido com `--fix`.

## Resumo

| Verificação | Resultado |
|---|---|
| Cobertura | 4 testes passaram; cobertura total de 83% |
| Complexidade | `process_order`: E (34) |
| Manutenibilidade | A (51.69) |
| Qualidade | 4 erros do Ruff: 3 `SIM102` e 1 `PLR1730` |

## Testes pós-refatoração

Após a refatoração de `src/legacy_checkout.py`, a suíte completa foi executada
com o comando:

```bash
PYTHONPATH=src pytest -q
```

Resultado:

```text
....                                                                     [100%]
4 passed in 0.00s
```

**Status:** passou. Os 4 testes existentes continuam aprovados após a
refatoração.
