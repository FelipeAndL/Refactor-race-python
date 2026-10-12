# Diagnóstico inicial

## Escopo e evidências analisadas

Foram analisados:

- [src/legacy_checkout.py];
- [tests/test_checkout.py];
- [testes iniciais.md];


Os resultados de execução registrados em `testes iniciais.md` foram considerados como os testes já realizados:

- 4 testes aprovados;
- cobertura de 83%: 72 instruções, 12 não cobertas;
- complexidade ciclomática E (34) para `process_order`;
- índice de manutenibilidade A (51,69);
- Ruff com 4 erros: 3 `SIM102` e 1 `PLR1730`;
- diagnóstico Pylance `reportMissingImports` para `legacy_checkout` em `tests/test_checkout.py` quando o projeto é analisado sem a configuração equivalente a `PYTHONPATH=src`.

## Diagnóstico dos testes

Os testes cobrem quatro cenários básicos: cliente regular, cliente VIP, cupom `PROMO10` e produtos duplicados. Eles validam parcialmente subtotal, desconto, frete, imposto, total e duplicidade.

Apesar de todos os testes registrados passarem, a cobertura de 83% indica que há caminhos não exercitados. A suíte não verifica, entre outros:

- cliente `employee` ou tipo de cliente desconhecido;
- cupons `PROMO20` e `VIP50`;
- limite máximo de desconto de 25%;
- frete expresso e frete para estados fora de MG, SP, RJ e ES;
- pedidos vazios, quantidades zero ou negativas;
- itens sem `weight`;
- campos obrigatórios ausentes;
- atualização de `ORDERS_PROCESSED`;
- efeitos colaterais dos `print`;
- combinações entre descontos, frete, imposto e pontos.

Portanto, os testes confirmam alguns cenários felizes, mas não estabelecem que as regras de checkout estejam corretas para entradas de fronteira ou inválidas.

## Problemas encontrados

### 1. Complexidade concentrada em uma única função — alta prioridade

`process_order` possui complexidade E (34), conforme o resultado do Radon. A função calcula subtotal, descontos, peso, frete, impostos, pontos, duplicidades, persistência em memória e saída no console.

Essa concentração aumenta o risco de regressões e dificulta testar cada regra isoladamente. O resultado também é coerente com os quatro erros de estilo encontrados pelo Ruff e com a grande quantidade de ramificações aninhadas, especialmente nas regras de desconto e frete.

**Referência:** [legacy_checkout.py:6].

### 2. Cálculo duplicado e variável sem uso — média prioridade

O subtotal é calculado duas vezes. O primeiro resultado é armazenado em `total1`, mas nunca é usado; o segundo cálculo em `subtotal` é o que alimenta o restante da função.

Além de trabalho desnecessário, a duplicação cria risco de divergência futura: uma alteração em apenas um dos loops pode fazer o código calcular dois subtotais diferentes sem que isso seja percebido.

**Referência:** [legacy_checkout.py:8]

### 3. Tratamento inconsistente de quantidades negativas — alta prioridade

Itens com `qty <= 0` são ignorados no subtotal, mas a quantidade é usada sem o mesmo filtro no cálculo do peso. Assim, uma quantidade negativa não contribui para o valor da compra, mas reduz o peso total e pode alterar o frete.

Não há validação que rejeite quantidade negativa. Esse comportamento não é coberto pelos testes atuais.

**Referências:** [legacy_checkout.py:10] e [legacy_checkout.py:54]

### 4. Ausência de validação de entrada — alta prioridade

A função acessa diretamente `customer["type"]`, `customer["name"]`, `x["qty"]`, `x["price"]` e `produto["qty"]`. Entradas incompletas causam `KeyError`; valores com tipos inadequados podem causar `TypeError` ou produzir cálculos inválidos.

Também não há validação explícita para preço negativo, quantidade negativa, estado inválido, tipo de cliente desconhecido ou cupons inválidos. O comportamento para tipos de cliente não reconhecidos é silenciosamente tratado como desconto zero.

**Referências:** [legacy_checkout.py:23], [legacy_checkout.py:108]

### 5. Estado global mutável entre chamadas — alta prioridade

Cada pedido é acrescentado a `ORDERS_PROCESSED`, uma lista global do módulo. Isso cria acoplamento entre chamadas e testes: resultados de uma execução permanecem disponíveis para as próximas, sem mecanismo de limpeza, limite ou persistência definida.

Em uso concorrente ou em processo de longa duração, a lista pode crescer indefinidamente e seu conteúdo pode ser observado ou alterado por qualquer consumidor do módulo. A suíte atual não verifica esse estado global.

**Referências:** [legacy_checkout.py:3] e [legacy_checkout.py:118].

### 6. Efeitos colaterais de apresentação misturados à regra de negócio — média prioridade

`process_order` imprime cinco mensagens sempre que é chamado. Isso polui a saída de aplicações e testes, dificulta a integração com logging estruturado e torna a função menos previsível para quem espera apenas um resultado.

**Referência:** [legacy_checkout.py:120].

### 7. Detecção de duplicados com complexidade quadrática — média prioridade

A busca de produtos duplicados compara todos os pares de itens e possui custo O(n²). Para pedidos grandes, essa etapa pode se tornar desnecessariamente cara. O algoritmo também depende de acesso direto a `items[i]["name"]`, portanto falha se um item não possuir nome.

**Referência:** [legacy_checkout.py:98].

### 8. Configuração de importação inconsistente — média prioridade

Os testes dependem de `PYTHONPATH=src` para importar `legacy_checkout`, conforme documentado em `testes iniciais.md`. Na análise do workspace, o Pylance reportou `reportMissingImports` em [test_checkout.py:2].

Isso indica que a configuração necessária para executar os testes não está refletida na configuração de análise do projeto. O código pode passar no comando ajustado e, ao mesmo tempo, permanecer com import não resolvido no editor ou em outra ferramenta.

### 9. Regras financeiras sem especificação formal — alta prioridade

O código implementa várias regras de negócio, mas o projeto não apresenta, nos arquivos analisados, uma especificação que justifique os percentuais, limites e combinações. Exemplos:

- cupons são somados ao desconto do cliente e depois limitados a 25%;
- `VIP50` adiciona valor fixo de 50;
- frete grátis depende do subtotal e de `express`;
- pontos são calculados sobre valor, frete e imposto;
- o imposto é calculado sobre o valor após desconto.

Os testes validam apenas parte dessas regras. Sem uma fonte de verdade, não é possível concluir que os valores implementados estão corretos, mesmo quando os testes passam.

## Priorização inicial

| Prioridade | Problemas |
|---|---|
| Alta | validação de entrada; quantidade negativa afetando o peso; estado global; regras financeiras sem especificação; complexidade da função |
| Média | configuração de importação; cálculo duplicado; efeitos de `print`; detecção O(n²) de duplicados |
| Baixa | simplificações de estilo já apontadas pelo Ruff, desde que não alterem o comportamento |

## Conclusão

O projeto possui uma base funcional mínima: os quatro testes registrados passam e a manutenibilidade foi classificada como A. Entretanto, o diagnóstico não deve ser interpretado como aprovação plena do checkout. A cobertura incompleta, a complexidade E, os quatro erros do Ruff, o import não resolvido no Pylance, a falta de validação e o estado global indicam risco relevante para evolução e uso com dados reais.

O próximo passo recomendado é primeiro definir as regras financeiras esperadas e adicionar testes para entradas de fronteira; em seguida, extrair responsabilidades de `process_order`, remover o cálculo duplicado, validar os dados de entrada e substituir o estado global e os `print` por interfaces explícitas.
