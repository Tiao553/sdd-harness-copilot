# Grounding Global — GitHub Copilot AgentSpec

Antes de qualquer resposta operacional neste workspace:

1. Ler esta página de grounding.
2. Se a mensagem invocar `/<nome>`, o skill ganha prioridade sobre o roteamento por intent:
   - Ler `.github/skills/<nome>/SKILL.md` antes de escolher agente.
   - Executar a sequência de grounding definida pelo próprio skill.
   - Usar `routing.json` apenas quando o skill mandar ou quando precisar resolver agente complementar.
3. Se não houver `/<nome>`, ler `.github/config/routing.json` — identificar o agente correto pelo intent
4. Ler o arquivo do agente identificado em `routes[n].agent`
5. Se a tarefa for técnica, carregar **somente** `routes[n].kb` (quick-reference)
   - Carregar `routes[n].kb_full` apenas se o quick-reference for insuficiente
   - Máximo de 3 arquivos KB por request
6. Ler `.github/config/security-settings.json` quando presente e aplicar a política de permissões antes de executar comandos ou alterar arquivos
7. Verificar `_meta/STATUS.md` e `_meta/CONTEXT.md` no diretório atual ou ancestrais
8. Se nenhuma rota corresponder, usar `default_agent` do routing.json

## Política de Permissões Obrigatória

Quando `.github/config/security-settings.json` existir, ele é parte obrigatória do grounding operacional.

O agente deve aplicar `permissions` como gate de execução:

- `alwaysAllow`: comandos e ferramentas considerados seguros para inspeção, validação local e leitura. Podem ser executados sem pedir nova confirmação, respeitando o sandbox ativo.
- `alwaysAsk`: comandos que mudam estado, dependências, histórico Git, ambiente, containers ou arquivos fora de edições controladas. Devem pedir aprovação explícita antes de executar.
- `alwaysDeny`: comandos destrutivos, operações de alto risco em banco de dados, limpeza Git irreversível, força em push/reset, alterações perigosas de sistema, serviços, registro ou processos. Devem ser recusados, salvo pedido explícito do usuário com escopo preciso e uma confirmação adicional.

Regras de aplicação:

- A correspondência deve considerar o comando completo e seus argumentos, não apenas o binário.
- Em caso de dúvida entre categorias, usar a categoria mais restritiva.
- Comandos encadeados devem ser avaliados por segmento; se qualquer segmento cair em `alwaysAsk` ou `alwaysDeny`, toda a execução deve seguir a categoria mais restritiva.
- A política não substitui sandbox, approvals do ambiente, nem regras de segurança do agente; ela adiciona uma camada obrigatória.
- Alterações manuais via ferramentas de edição seguem a mesma intenção: edições dentro do workspace são permitidas quando fazem parte da tarefa; edições destrutivas, reversões amplas ou remoções devem ser tratadas como `alwaysAsk` ou `alwaysDeny` conforme o risco.

## Prioridade de Skills

Quando a entrada contém `/<nome>`, o `SKILL.md` correspondente é a fonte primária de execução. A rota do agente não pode sobrescrever instruções do skill.

Ordem obrigatória com skill:

```text
1. grounding.md
2. .github/skills/<nome>/SKILL.md
3. Arquivos/agentes/KB exigidos pelo skill
4. .github/config/security-settings.json quando presente
5. routing.json somente se o skill exigir roteamento adicional
```

Se o skill citado não existir em `.github/skills/<nome>/SKILL.md`, pare e informe o caminho ausente. Não execute o fluxo como pedido genérico.

## Inicialização de Workflow SDD

As fases SDD do workflow (`/brainstorm`, `/define`, `/design`, `/build`, `/validate`, `/ship`, `/iterate`, `/create-pr`) só podem ser inicializadas via:

```text
/workflow-commands /<fase> ...
```

Pedidos em linguagem natural como "faça o build", "rode o design", "ship essa feature" ou "crie a fase define" devem ser tratados como intenção incompleta. Responda com o comando exato esperado e não inicie a fase.

Exceção: é permitido editar documentos SDD diretamente quando o usuário pedir uma alteração pontual em um arquivo específico, sem iniciar uma fase de workflow.

Toda resposta operacional deve começar com:

```markdownW
> **Specialist Activated:** `[Agent Name]`  
> **Path:** `[Agent Path]`
>
> **Execution Grounding**
>
> | Property | Value |
> |---|---|
> | Router | `✓` |
> | Skill | `<nome\|none>` |
> | Active Agent | `<nome\|N/A>` |
> | Knowledge Base | `<dominio\|none>` |
> | Files Loaded | `<n>` |
> | Detected Project | `<nome detectado\|none>` |
> | Execution Tier | `CRÍTICO \| IMPORTANTE \| PADRÃO` |
> | Prompt Tokens | `~<estimativa>` |W
```

## Token Budget Strategy

| Situação | Ação |
|---|---|
| Pergunta conceitual simples | Apenas `quick-reference.md` do KB relevante |
| Implementação com padrão conhecido | `quick-reference.md` + arquivo de pattern específico |
| Implementação complexa / novo domínio | `index.md` + até 3 arquivos de `concepts/` ou `patterns/` |
| Tarefa multi-domínio | `quick-reference.md` de cada domínio (max 3 domínios) |
| Large Task / SDD completo | Usar `the-planner` para quebrar em subtarefas com budget individual |

Nunca carregar um diretório inteiro de KB em uma única chamada.
Declare sempre os arquivos carregados no bloco de grounding operacional.

## Regras

- Não responder de memória sem ler os arquivos obrigatórios
- Não pular o bloco de grounding em respostas operacionais
- Não ignorar `/<nome>`; skill tem prioridade sobre roteamento por intent
- Não iniciar fases SDD sem `/workflow-commands /<fase>`
- Não assumir contexto de projeto sem verificar `_meta/`
- Não carregar KB completo quando quick-reference for suficiente
- Não iniciar BUILD sem gates SDD verificados quando aplicável
- Preferir sempre `COPILOT.md` como fonte canônica se houver conflito
