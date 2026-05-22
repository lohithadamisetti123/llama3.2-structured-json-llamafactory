# Failure Analysis — EVAL-014 (Invoice — Nile Cotton Exports)

## Source Document Text

```
NILE COTTON EXPORTS
Cairo, Egypt
TAX INVOICE
No: NCE-EG-2025-018
Date: 10 Feb 2025
Due: 10 Mar 2025

Egyptian Cotton 100tc 50m    x20   @45.00
Linen Blend 30m              x15   @62.00
Silk Thread 1000m Spool      x50   @8.50

Subtotal: 2,275.00
Tax: 0.00
Total: 2,275.00 USD
```

## Expected JSON Output

```json
{"vendor": "NILE COTTON EXPORTS", "invoice_number": "NCE-EG-2025-018", "date": "2025-02-10", "due_date": "2025-03-10", "currency": "USD", "subtotal": 2275.0, "tax": 0.0, "total": 2275.0, "line_items": [{"description": "Egyptian Cotton 100tc 50m", "quantity": 20, "unit_price": 45.0}, {"description": "Linen Blend 30m", "quantity": 15, "unit_price": 62.0}, {"description": "Silk Thread 1000m Spool", "quantity": 50, "unit_price": 8.5}]}
```

## Model's Actual Output

```
The extracted invoice data is:
{"vendor": "NILE COTTON EXPORTS", "invoice_number": "NCE-EG-2025-018", "date": "2025-02-10", "due_date": "2025-03-10", "currency": "USD", "subtotal": 2275.0, "tax": 0.0, "total": 2275.0, "line_items": [{"description": "Egyptian Cotton 100tc 50m", "quantity": 20, "unit_price": 45.0}, {"description": "Linen Blend 30m", "quantity": 15, "unit_price": 62.0}, {"description": "Silk Thread 1000m Spool", "quantity": 50, "unit_price": 8.5}]}
```

## Analysis

### What went wrong
**Formatting issue — prose preamble.** The model prefixed its response with `"The extracted invoice data is:\n"` before the JSON object. This makes the full response fail `json.loads()` even though the JSON content after the preamble is 100% correct — all keys present, all values accurate, all types correct.

### Why it likely failed
This document has an **unusual header structure** — the company name, location, and document type label ("TAX INVOICE") appear as separate unformatted lines before the structured fields begin. Most training examples have a cleaner separation between document header and fields. The model may have interpreted the informal header as a conversational context that warranted a conversational response pattern. Additionally, this is an **international trade document** (Cairo, Egypt) — a document origin underrepresented in training data, which may trigger the model's pre-trained conversational instincts.

### What training data change would fix it
Add 3–5 training examples with similar characteristics:
1. International trade invoices with country/city in header (e.g., "Lagos, Nigeria", "São Paulo, Brazil")
2. Documents where "TAX INVOICE" or similar labels appear as standalone header lines
3. Examples with "Date: DD Mon YYYY" format to reinforce date conversion without prose
These additions would teach the model that international/export document headers are still extraction targets, not conversation starters.
