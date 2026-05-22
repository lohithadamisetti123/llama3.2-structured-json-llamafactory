# Prompt Engineering Iterations

This document records three distinct prompt engineering approaches tested against the base Llama 3.2 3B-Instruct model (no fine-tuning) to improve structured JSON output.

## Target Documents

The 3 worst-performing baseline documents were selected:
- **EVAL-003** (Sakura Tech Japan) — markdown fences + wrong key names
- **EVAL-014** (Nile Cotton Exports) — prose + bold markdown + completely wrong keys
- **EVAL-018** (Siemens AG PO) — prose + all key names wrong

---

## Prompt Version 1: Strict Format Instructions

### Prompt Text
```
You are a JSON extraction engine. Your ONLY output must be a single valid JSON object.

CRITICAL RULES:
1. Output ONLY the JSON object — no text before or after it
2. Do NOT wrap the JSON in markdown code fences (```)
3. Do NOT add any explanation, notes, or commentary
4. Use EXACTLY these keys for invoices: vendor, invoice_number, date, due_date, currency, subtotal, tax, total, line_items
5. Use EXACTLY these keys for purchase orders: buyer, supplier, po_number, date, delivery_date, currency, total, items
6. Dates must be in YYYY-MM-DD format
7. Use null for missing fields, not "N/A" or empty string for dates

Extract all fields from the following document and return the JSON:
```

### Rationale
Added explicit negative constraints ("do NOT wrap", "do NOT add explanation") and specified the exact key names. The hypothesis is that the base model follows specific prohibitions better than general instructions.

---

## Prompt Version 2: Few-Shot Examples

### Prompt Text
```
Extract structured data from the document below. Return ONLY a valid JSON object.

Example 1:
Document: "Quick Mart | INV-001 | 2024-01-15\nWidget(2x10.00)\nTotal=20.00 USD"
Output: {"vendor": "Quick Mart", "invoice_number": "INV-001", "date": "2024-01-15", "due_date": null, "currency": "USD", "subtotal": 20.0, "tax": null, "total": 20.0, "line_items": [{"description": "Widget", "quantity": 2, "unit_price": 10.0}]}

Example 2:
Document: "PO# ABC-001 | 2024-06-01\nBuyer: Acme Corp\nSupplier: Widget Co\nMotor(5x100.00)\nTotal=500.00 USD"
Output: {"buyer": "Acme Corp", "supplier": "Widget Co", "po_number": "ABC-001", "date": "2024-06-01", "delivery_date": null, "currency": "USD", "total": 500.0, "items": [{"item_name": "Motor", "quantity": 5, "unit_price": 100.0}]}

Now extract from this document:
```

### Rationale
Few-shot prompting provides the model with concrete examples of the expected output format. Two examples are included (one invoice, one PO) to demonstrate both schemas. The examples use minimal documents to keep the prompt short while showing the exact key structure.

---

## Prompt Version 3: System Role + Schema Definition + Negative Examples

### Prompt Text
```
SYSTEM: You are a deterministic JSON extraction API. You receive document text and return a JSON object. You never generate natural language, markdown, or formatting. Your output starts with { and ends with }.

SCHEMA (Invoice):
{"vendor": str, "invoice_number": str, "date": "YYYY-MM-DD", "due_date": "YYYY-MM-DD"|null, "currency": "XXX", "subtotal": float, "tax": float|null, "total": float, "line_items": [{"description": str, "quantity": int, "unit_price": float}]}

SCHEMA (Purchase Order):
{"buyer": str, "supplier": str, "po_number": str, "date": "YYYY-MM-DD", "delivery_date": "YYYY-MM-DD"|null, "currency": "XXX", "total": float, "items": [{"item_name": str, "quantity": int, "unit_price": float}]}

BAD OUTPUTS (never do these):
- "Here is the JSON: {...}" ← NO prose
- "```json\n{...}\n```" ← NO code fences
- {"vendor_name": ...} ← NO custom key names

GOOD OUTPUT:
{"vendor": "Example Corp", "invoice_number": "E-001", ...}

Extract from this document:
```

### Rationale
Combines three strategies: (1) system role framing as a "deterministic API" to suppress conversational behavior, (2) explicit schema definition with types, and (3) negative examples showing what NOT to do. This is the most aggressive prompt engineering approach, directly addressing all three observed failure modes (prose, fences, wrong keys).
