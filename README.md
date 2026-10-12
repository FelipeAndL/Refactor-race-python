# REFactor Race Python

## EQUIPE
- Adriano Teixeira Neto
- Davi Abras Scalabrini
- Gustavo Edson Nunes
- Heitor Souza
- João Vitor de Jesus
- Luiz Felipe Damasceno

## DESCRIÇÃO
Este projeto tem como objetivo refatorar uma implementação de checkout em Python, reorganizando a lógica de cálculo de descontos, frete, imposto, pontos e duplicidade de itens. A proposta foi aumentar a legibilidade, reduzir a complexidade da função principal e melhorar a manutenção do código com foco em testes automatizados e qualidade de software.

Durante a atividade, foi realizado um diagnóstico inicial do código legado, identificando problemas estruturais e de design, e em seguida foi aplicada uma refatoração focada em decompor responsabilidades, remover redundâncias e tornar a lógica mais previsível e testável.

## DIAGNÓSTICO INICIAL
Antes da refatoração, o módulo de checkout apresentava diversos problemas que comprometiam a extensibilidade e a confiabilidade do sistema.

Principais problemas encontrados:
- A função `process_order` concentrava múltiplas responsabilidades em um único bloco, elevando a complexidade ciclomática e dificultando a manutenção.
- O subtotal era calculado mais de uma vez, gerando duplicação de lógica e risco de inconsistência.
- Quantidades negativas eram tratadas de forma inconsistente, afetando cálculo de peso e frete.
- Não havia validação adequada para entradas ausentes ou inválidas, como clientes sem tipo, itens sem dados obrigatórios e estados desconhecidos.
- O módulo mantinha estado global mutável em `ORDERS_PROCESSED`, o que acoplava chamadas e podia gerar efeitos colaterais.
- A lógica de impressão estava misturada ao processamento do pedido, dificultando reutilização e testes.
- A detecção de produtos duplicados era implementada de forma ineficiente e menos robusta.
- O projeto também apresentava importação inconsistente no ambiente de análise e falhas de qualidade estática apontadas por Ruff.

Esses problemas indicavam que o código, embora funcional para alguns cenários básicos, não era suficientemente confiável para evolução e manutenção.

## CODE SMELLS ENCONTRADOS
Os principais code smells identificados foram:

1. Função monolítica
   - `process_order` realizava cálculo de subtotal, desconto, frete, imposto, pontos, duplicidade e persistência/saída em uma única rotina.
   - Impacto: alta acoplamento, baixa legibilidade e grande dificuldade de testar regras isoladamente.

2. Lógica duplicada
   - O subtotal era calculado repetidamente, com uma variável não utilizada, aumentando redundância e tornando o código mais sujeito a divergências futuras.

3. Tratamento inconsistente de dados
   - Valores nulos ou incompletos eram acessados diretamente, sem validação. Isso gerava risco de `KeyError`, `TypeError` e comportamento imprevisível.

4. Estado global mutável
   - `ORDERS_PROCESSED` acumulava pedidos entre execuções, criando dependência entre chamadas e dificultando isolar testes.

5. Acoplamento entre regra de negócio e saída
   - Impressões de console estavam misturadas ao cálculo, o que poluía a interface e tornava a função menos reutilizável.

6. Algoritmo ineficiente para duplicidade
   - A busca de itens repetidos comparava todos os elementos em pares, gerando custo quadrático para listas maiores.

## REFATORAÇÕES REALIZADAS
A seguir, as principais refatorações aplicadas justificadas por problema e melhoria.

### 1. Decomposição da lógica em funções auxiliares
- PROBLEMA ENCONTRADO: a função principal acumulava muitas responsabilidades.
- ALTERAÇÃO REALIZADA: as regras foram separadas em funções como `_calculate_subtotal`, `_calculate_discount`, `_calculate_shipping`, `_calculate_tax`, `_calculate_points`, `_find_duplicate_products`, `_build_result` e `_print_order_summary`.
- JUSTIFICATIVA: isso reduz a complexidade da função principal, melhora a legibilidade e facilita testes unitários específicos para cada comportamento.

### 2. Eliminação de cálculo duplicado
- PROBLEMA ENCONTRADO: o subtotal era calculado duas vezes e uma variável não era utilizada.
- ALTERAÇÃO REALIZADA: a lógica de subtotal foi centralizada em uma única função responsável por somar os valores válidos de cada item.
- JUSTIFICATIVA: evita redundância, elimina inconsistência e deixa o fluxo mais previsível.

### 3. Centralização das regras de desconto e frete
- PROBLEMA ENCONTRADO: as regras de desconto e frete estavam embutidas diretamente no fluxo principal, dificultando validação e manutenção.
- ALTERAÇÃO REALIZADA: as regras foram encapsuladas em funções especializadas para cliente, cupom e cálculo de frete.
- JUSTIFICATIVA: as regras ficam mais claras e organizadas, permitindo ajuste futuro sem afetar outras partes do fluxo.

### 4. Organização da estrutura de retorno
- PROBLEMA ENCONTRADO: o resultado final era montado de forma implícita e pouco explícita.
- ALTERAÇÃO REALIZADA: a montagem do retorno foi separada em `_build_result`.
- JUSTIFICATIVA: cria um contrato claro para quem utiliza a função e melhora a padronização do resultado.

### 5. Isolamento da camada de apresentação
- PROBLEMA ENCONTRADO: `print` estava misturado ao cálculo do pedido.
- ALTERAÇÃO REALIZADA: a mensagem de saída foi isolada em uma função específica para resumo do pedido.
- JUSTIFICATIVA: separa regra de negócio de apresentação, tornando o código reutilizável em APIs, serviços e testes automatizados.

### 6. Otimização da detecção de duplicados
- PROBLEMA ENCONTRADO: a detecção de produtos repetidos era feita de forma ineficiente com comparação de pares.
- ALTERAÇÃO REALIZADA: a busca foi reescrita com uso de dicionário para contabilizar ocorrências por nome.
- JUSTIFICATIVA: reduz a complexidade do algoritmo e deixa a regra mais clara e eficiente.

### 7. Melhor organização do módulo de checkout
- PROBLEMA ENCONTRADO: o código legado era de difícil manutenção por concentrar múltiplas regras em um único escopo.
- ALTERAÇÃO REALIZADA: a estrutura foi reorganizada em pequenas funções coesas e com nomes expressivos.
- JUSTIFICATIVA: facilita leitura, manutenção e entendimento do comportamento esperado do módulo.

## TESTES ADICIONADOS
A equipe também ampliou a cobertura de testes para validar cenários mais relevantes. Os principais cenários adicionados ou reforçados incluem:
- cliente regular com desconto por valor mínimo;
- cliente VIP com desconto e regras específicas;
- uso de cupom promocional;
- pedidos com produtos duplicados;
- verificação do retorno do objeto final e dos valores esperados.

Além de reforçar a suíte existente, os testes ajudam a confirmar que a refatoração preserva o comportamento funcional previamente esperado e passa a oferecer maior segurança para futuras alterações.

## MÉTRICAS ANTES E DEPOIS
Com base no diagnóstico inicial e no comparativo do projeto, foi observada a seguinte evolução:

| Indicador | Antes | Depois | Melhoria |
|---|---:|---:|---|
| Cobertura de testes | 83% | 95% | +12 pontos percentuais |
| Complexidade de `process_order` | E (34) | A (1) | Redução significativa |
| Complexidade média do módulo | E (34,0) | A (2,75) | Redução significativa |
| Problemas Ruff | 4 | 0 | Eliminados |
| Testes aprovados | 4/4 | 4/4 | Mantidos |
| Manutenibilidade (Radon) | A (51,69) | A (41,07) | Mantida a classificação |

Essas métricas demonstram que a refatoração melhorou a organização do código, reduziu a complexidade e elevou a confiabilidade da solução.

## DECISÕES TÉCNICAS
As principais decisões técnicas adotadas foram:
- decompor a lógica em funções menores e especializadas;
- manter um único ponto de cálculo para cada regra financeira;
- separar cálculo de retorno de apresentação na console;
- priorizar leitura clara e manutenção em vez de regras acopladas;
- estruturar a solução com foco em testes e previsibilidade.

A estratégia adotada foi reforçar a qualidade estrutural do código sem alterar a intenção do domínio da aplicação: processar pedidos com regras de desconto, frete e imposto de forma consistente.

## USO DE INTELIGÊNCIA ARTIFICIAL
Neste projeto, não houve uso de ferramentas de inteligência artificial para alterar a lógica de negócio do código. A análise da estrutura do projeto, a organização do diagnóstico e a preparação do README foram realizadas com apoio da observação do código e da documentação disponível no repositório.

## MELHORIAS FUTURAS
Ainda há oportunidades para evoluir o projeto, como:
- ampliar a suíte de testes com cenários de borda e entradas inválidas;
- validar regras de clientes e cupons não cobertos até então;
- remover ou encapsular melhor o uso de estado global;
- formalizar a regra de negócio em documentação específica para evitar ambiguidades;
- melhorar a organização do módulo para facilitar evolução futura em serviços e APIs.

Em resumo, a refatoração foi bem-sucedida ao transformar um código monolítico em uma solução mais clara, mais testável e mais adequada à manutenção contínua.
