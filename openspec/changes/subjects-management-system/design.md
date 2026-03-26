## Context

O EduTrack AI é um sistema acadêmico construído com XanoScript e desenvolvimento orientado por especificações. Atualmente possui tabelas básicas para usuários, contas e logs de eventos, mas não tem uma estrutura dedicada para gerenciar disciplinas acadêmicas. Esta implementação criará a base de dados e APIs necessárias para que usuários possam registrar e gerenciar suas matérias, estabelecendo a fundação para futuras funcionalidades de IA e automação.

## Goals / Non-Goals

**Goals:**
- Criar uma tabela `subject` robusta com controle de propriedade por usuário
- Implementar APIs CRUD completas com validações de segurança
- Fornecer endpoints para estatísticas básicas de progresso acadêmico
- Preparar estrutura extensível para futuras automações
- Garantir isolamento completo de dados entre usuários

**Non-Goals:**
- Implementar interface de usuário (frontend)
- Criar sistema de notificações ou alertas
- Implementar funcionalidades avançadas de IA ou automação
- Migrar dados existentes (não há dados para migrar)
- Criar sistema de permissões avançadas (apenas controle básico de propriedade)

## Decisions

### 1. Estrutura da Tabela Subject
**Decisão**: Usar uma tabela dedicada `subject` com relacionamento direto via `user_id`

**Alternativas consideradas**:
- Usar tabela `event_log` existente com tipo "subject" - Rejeitado pois event_log é para auditoria, não dados persistentes
- Criar tabela genérica "user_data" - Rejeitado pois limitaria queries específicas e validações

**Rationale**: Permite queries otimizadas, validações específicas e extensibilidade futura

### 2. Controle de Propriedade
**Decisão**: Validação obrigatória de `user_id` em todas as operações via middleware/função auxiliar

**Alternativas consideradas**:
- Controle via Row Level Security (RLS) - Não disponível no Xano atual
- Validação apenas no frontend - Inseguro, permite manipulação direta da API

**Rationale**: Segurança em nível de API garante isolamento mesmo com acesso direto aos endpoints

### 3. Campos da Tabela
**Decisão**: Campos essenciais (nome, código, semestre, créditos) + metadata extensível

**Alternativas consideradas**:
- Campos fixos para todos os dados - Limitaria flexibilidade para diferentes instituições
- JSON genérico apenas - Dificultaria queries e validações

**Rationale**: Balanceia estrutura com flexibilidade, permitindo queries eficientes e extensibilidade

### 4. APIs RESTful
**Decisão**: Seguir padrão REST com grupo dedicado "Subjects"

**Alternativas consideradas**:
- GraphQL - Overkill para CRUD básico, aumenta complexidade
- APIs genéricas - Menos intuitivo e autodocumentável

**Rationale**: Consistente com arquitetura existente, fácil de entender e documentar

## Risks / Trade-offs

**Performance com crescimento**: Tabela pode crescer rapidamente → Mitigação: Índices otimizados, paginação obrigatória

**Validações podem ser bypassadas**: Se função auxiliar falhar → Mitigação: Testes unitários, logs de auditoria

**Metadata schema inconsistente**: Usuários podem inserir dados malformados → Mitigação: Validação de schema no frontend, documentação clara

**Mudanças futuras no schema**: Podem quebrar APIs existentes → Mitigação: Versionamento de API, migrations controladas

## Migration Plan

1. **Deploy da tabela**: Criar tabela `subject` no Xano (sem downtime)
2. **Deploy das funções**: Criar função auxiliar de validação
3. **Deploy das APIs**: Criar grupo e endpoints (podem ser deployed gradualmente)
4. **Testes**: Validar isolamento de dados e funcionamento básico
5. **Rollback**: Remover APIs e função (tabela pode permanecer para dados futuros)

## Open Questions

- Como será implementada a sincronização com sistemas acadêmicos externos?
- Quais campos adicionais podem ser necessários para diferentes tipos de instituição?
- Como será feita a migração quando o schema evoluir?