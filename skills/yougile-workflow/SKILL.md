---
name: yougile-workflow
description: Work with YouGile only through the connector explicitly selected by the operator. Require a link for an existing task and an operator-decided, verified full path for new entities; ask when context is missing.
---

# YouGile workflow

## Connection and target

Use only the YouGile connector manually specified by the operator for the current request. Do not choose a connector from the available list, a previous session, a repository, or a matching name. If no connector is specified, ask which organization and connection to use before any YouGile operation. Do not use browser UI automation, a direct REST API, CLI, another connector, or other workaround for YouGile reads or writes. If the selected connector cannot perform the operation, report that limit and ask the operator how to proceed.

For work with an existing task or knowledge-base page, require its link from the operator. Resolve that link through the selected connector and verify the returned identity before changing anything. An ID, title, search hit, or remembered technical ID alone is not enough to start work on a specific task; ask for the link. Keep the operator's link in the final report.

## Knowledge-base pages

A YouGile knowledge-base page may be backed by a board task with a different interface and no visible chat. A confirmed case showed that the task connector's description update changed the page body. When a page link is supplied, check this route through the selected connector; do not infer from a missing chat or a failed task read that the page is not task-backed. Preserve existing body text unless the operator explicitly requests replacement. If the connector cannot read the current body, do not overwrite unknown content as an append or claim that it was preserved. Ask the operator for the existing text or an explicit replacement decision.

## Creating entities

Before creating a project, board, column, task, or knowledge-base page, obtain the complete intended path and all material choices from the operator: organization, parent project, board, column or section where applicable, title, and any requested visibility or ownership. Verify every existing part of the path through the selected connector. Present unresolved alternatives to the operator; do not invent placement, names, permissions, or structure. If the connector cannot verify the full path or the requested entity type, stop before creation. In ambiguous cases, suggest that the operator create the entity in the YouGile interface and send its link; this is usually safer than connector-based creation.

## Formatting descriptions and knowledge-base pages

YouGile may render Markdown fenced code blocks and line breaks inside them as one continuous line. Do not use code fences, indented code, or a run of plain lines for commands, credentials, IDs, or other values that must remain distinct. Do not rely on inline-code styling to make them readable. Use the structures confirmed to survive in the target page: headings, short paragraphs, and one list item per distinct value or action.

For a sequence, use a numbered list. Put exactly one executable command in each item and state its working directory in the item or in a heading immediately above the list. For alternatives or reference commands, use bullets instead. Keep comments and explanations outside the command text so a copied command does not include prose. Never join commands merely to imitate a code block.

For access details and other field/value data, use one bullet per account or object with explicit labels such as `Role:`, `Login:`, and `Password:`. If a value is long or visually similar to another, give it its own bullet. Include passwords only when the operator authorized publishing those specific values to that YouGile destination; otherwise describe where to obtain them. Make URLs clickable when the editor supports links.

Before a substantial write, format a small representative sample if rendering is uncertain. After writing, inspect the rendered page through the selected connector if it exposes that view; otherwise ask the operator to confirm the visual result. Adjust the formatting from observed behavior and record only reusable, confirmed lessons here.

## Writes and verification

A link or read request does not authorize a write. Carry out only the requested field changes on the verified target. After a write, verify the response and, when supported, the resulting state through the same selected connector. After an uncertain result, reconcile before retrying. If a read tool fails while a write reports success, describe those separately and do not claim visual verification.

## Evolving this skill

After a real use reveals a reusable behavior, compare the connector result with the operator-visible outcome. When the operator confirms the lesson, update this skill with the narrowest rule that changes future decisions, including its scope and evidence. Revisit an existing rule when later confirmed evidence contradicts it. Do not turn one error, guess, or connector-specific behavior into a universal YouGile rule, and do not silently relax the connector, link, path, or authorization gates above.
