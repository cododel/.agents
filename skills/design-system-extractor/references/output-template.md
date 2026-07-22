# Output Template

Fill this skeleton to produce `DESIGN.md`. Adapt sections to the project and evidence: drop a
section if the project genuinely
has nothing for it (don't pad), and add one if the evidence clearly calls for it. Replace every
`{{PLACEHOLDER}}`. Lines in `<!-- ... -->` are guidance for you and must not appear in the output.

Keep facts traceable to code. Where useful, tag a claim as observed vs inferred, e.g.
`(observed)` for code-derived facts and `(inferred)` for philosophy/rationale.

---

```markdown
# {{PROJECT_NAME}} — Design System

<!-- One-line statement of what this document is. -->

## 1. Manifesto

{{ONE_PARAGRAPH_PHILOSOPHY}}

**Keywords:** {{KW_1}}, {{KW_2}}, {{KW_3}}, {{KW_4}}, {{KW_5}}.

<!-- Pull the actual intent from Layer 2/3. Don't invent a vibe the evidence doesn't support. -->

## 2. Core Rules (Non-Negotiables)

<!-- Each rule should be something the codebase ENFORCES (high frequency / consistency),
     not a one-off. Bold the rule name, then state it in one sentence. -->

1. **{{RULE_NAME}}**: {{RULE_STATEMENT}}.
2. **{{RULE_NAME}}**: {{RULE_STATEMENT}}.
3. **{{RULE_NAME}}**: {{RULE_STATEMENT}}.

## 3. Color System

<!-- Token table. Every value must come from collect_tokens.py / the code.
     If light + dark token sets exist, include both (e.g. add a Mode column or a second table). -->

| Token Name | Value | Usage |
| :--- | :--- | :--- |
| {{TOKEN}} | `{{VALUE}}` | {{USAGE}} |
| {{TOKEN}} | `{{VALUE}}` | {{USAGE}} |

<!-- If the project themes via CSS custom properties, list the variable names and their values. -->

## 4. Typography System

<!-- One subsection per role the project actually uses. The example below assumes a
     display / interface / content split; adapt to what the fonts and usage show. -->

### A. {{ROLE_e.g._Display}}
- **Font:** `{{FONT}}`
- **Style:** {{case_tracking_leading_etc}}
- **Behavior:** {{responsive_notes_if_any}}

### B. {{ROLE_e.g._Interface}}
- **Font:** `{{FONT}}`
- **Style:** {{...}}

### C. {{ROLE_e.g._Content}}
- **Font:** `{{FONT}}`
- **Style:** {{...}}

## 5. Components And Interaction Patterns

<!-- Document PATTERNS and STATES, not one component's literal classes.
     Cover the primitives the project actually has. -->

### 5.1 Primary actions
- **{{Variant}}:** {{appearance}}. *Interactive states:* {{hover_pressed_focus_disabled}}.

### 5.2 Cards
- **Default:** {{appearance}}.
- **Hover/Active:** {{state_changes}}.

### 5.3 Navigation
- **Large / expanded surfaces:** {{pattern}}.
- **Compact / touch surfaces:** {{pattern}}.

### 5.4 Decorative / signature elements
- {{any_recurring_motifs_dividers_cursors_etc}}

## 6. Layout Patterns

- **{{Pattern_e.g._Hero}}:** {{desktop_and_mobile_behavior}}.
- **{{Pattern_e.g._Lists/Grids}}:** {{structure}}.

## 7. Motion

- **Speed / easing:** {{durations_and_curves_if_present}}.
- **Effects:** {{named_effects_if_any}}.

<!-- Only include if the codebase has real motion conventions (transitions/animations). -->

## 8. Implementation Checklist

<!-- Concrete, copy-pasteable conventions in the project's native implementation language:
     utility classes, token names, resource IDs, theme APIs, or component props. -->

- **Borders:** {{default}} / {{interactive}}
- **Backgrounds:** {{...}}
- **Text:** {{...}}
- **Radius:** {{...}}
- **Transitions:** {{...}}

---

## Provenance

<!-- MANDATORY. Be honest and specific. -->

- **Evidence used:** implementation ({{which_files_resources_or_surfaces}}); docs ({{which}});
  git ({{yes/no}}); optional agent sessions ({{declined_not_available_or_count}}).
- **Observed vs inferred:** {{which_parts_are_facts_vs_interpretation}}.
- **Conflicts / open questions:** {{code-vs-doc_discrepancies_or_"none"}}.
- **Generated:** {{date}} by the design-system-extractor skill.
```
