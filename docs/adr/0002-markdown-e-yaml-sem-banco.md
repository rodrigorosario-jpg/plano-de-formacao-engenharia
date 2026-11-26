# ADR 0002 · Markdown e YAML, sem banco de dados

- **Status:** Aceita
- **Data:** 25/11/2026

## Contexto

O currículo tem 86 módulos e disciplinas, 174 pré-requisitos e 156 competências. Cada módulo já é um arquivo Markdown com cabeçalho YAML em `disciplinas/`; listas e gabaritos são Markdown; verificações e catálogo são YAML; respostas são CSV. Scripts, testes, CI e a skill dependem desses caminhos. A [auditoria de 25/11/2026](../arquitetura/auditoria.md) mostrou que mover pastas quebraria scripts, CI e a skill instalada, e que renomear listas ou competências quebraria o histórico em `registro/`.

## Decisão

1. O Core fica em arquivos Markdown e YAML (CSV para os registros), sem banco de dados (decisão D2 da auditoria, seção 8).
2. Organização híbrida: pastas por tipo de artefato, arquivos planos nomeados pelo código e domínio (eixo) como metadado. Visões por assunto são geradas, não armazenadas.
3. Os caminhos atuais ficam. A estrutura só recebe acréscimos:

```
plano-de-estudos/
  disciplinas/     mantém: um arquivo por módulo ou disciplina
  exercicios/      mantém: listas, gabaritos/ e verificacao/ por código
  registro/        mantém: dados de quem estuda (estado.yml entra no Marco 4)
  catalogo/        novo: eixos, unidades, projetos, escalas, códigos aposentados
  schemas/         novo (Marco 2): JSON Schema com versão
  templates/       novo (Marco 2): modelo por tipo de conteúdo
  docs/
    arquitetura/   novo: visão, auditoria, modelo, glossário, segurança, roadmap, débitos
    adr/           novo: uma decisão por arquivo
    referencia/    novo: cópia congelada do Mapa de Formação
    skills/        mantém
  scripts/ tests/ skills/ benchmark/ plano.yml    mantêm
```

4. `conceitos/` só é criada com o primeiro conceito. `benchmark/` fica onde está, identificado como evidência, porque vários documentos apontam para ele.

## Alternativas consideradas

| Alternativa | Por que não |
| --- | --- |
| Banco relacional | Infraestrutura sem necessidade para 86 itens; perde o diff legível do Git |
| Banco de grafos | Mesmo motivo; o grafo de pré-requisitos já é validado por script |
| Organizar por domínio | Itens interdisciplinares e reclassificações moveriam arquivos; custo de migração alto |
| Organizar por tecnologia | Não serve a um currículo de fundamentos; custo de migração alto |

## Consequências

- Qualquer tecnologia lê o Core; o histórico do Git é o histórico do currículo.
- Consultas ricas (busca, filtros, cadeias críticas) ficam para um export JSON no Marco 5.
- Visões por assunto dependem de índices gerados.
- O [modelo de conhecimento](../arquitetura/modelo.md) diz o que mora em cada pasta.
