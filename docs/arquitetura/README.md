# Arquitetura do Knowledge Core

Documentação de arquitetura do repositório: o que é o Knowledge Core, como o conhecimento é modelado, que riscos existem, para onde vai e o que ficou pendente. As decisões estão nas [ADRs](../adr/README.md).

| Documento | O que tem |
| --- | --- |
| [Visão](visao.md) | O que é o Knowledge Core, os três estágios, os três contextos, o diagrama C4 de contexto e os princípios |
| [Modelo de conhecimento](modelo.md) | Entidades, relações, identificadores, classes de metadados, onde mora cada coisa e versionamento de schema |
| [Glossário](glossario.md) | Termos do projeto, com a definição curta e onde cada um é definido |
| [Segurança](seguranca.md) | Threat model STRIDE, material como conteúdo e não instrução, exemplos de código, CI, auditoria de hardening e checklist das configurações do GitHub |
| [Roadmap](roadmap.md) | Marcos 1 a 6 com entregáveis, aceite e status; critérios para o Core evoluir além do Marco 4 |
| [Débitos](debitos.md) | Problemas conhecidos, com impacto, proposta e quando tratar |
| [Auditoria de 25/11/2026](auditoria.md) | Registro histórico da auditoria que originou esta arquitetura |
| [ADRs](../adr/README.md) | Uma decisão por arquivo: fonte de verdade, formato, IDs, andamento, schema, fluxo de git, autoria |

## Por onde começar

1. [Visão](visao.md), para entender as partes e as fronteiras.
2. [ADRs](../adr/README.md), para saber o que já foi decidido.
3. [Modelo](modelo.md), antes de mudar um arquivo de `disciplinas/`, `catalogo/` ou `exercicios/`.
4. [Roadmap](roadmap.md) e [débitos](debitos.md), para saber o que vem e o que ficou para depois.

## Documentos relacionados

- [Fluxo de git](../fluxo-git.md): em qual branch cada mudança vai.
- [Catálogo](../../catalogo/README.md): eixos, unidades, projetos e escalas.
- [Mapa de Formação, cópia congelada](../referencia/mapa-de-formacao-rev74.md): o documento de origem.
- [Guia de manutenção da skill](../skills/08_maintenance_guide.md) e [auditoria de segurança da skill](../skills/05_security_audit.md).
