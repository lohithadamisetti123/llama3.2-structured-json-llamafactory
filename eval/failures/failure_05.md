# Failure Analysis — Additional Test Doc C (PO — Sparse Format)

## Source Document Text

```
ORDER
Amazon Web Services to Cloudflare Inc.
PO-AWS-2025-9182
01/15/2025

1x Enterprise SSL Certificate   $4,999.00
1x DDoS Protection Annual Plan  $12,500.00
1x CDN Bandwidth 100TB/mo       $8,750.00

Total $26,249.00
```

## Expected JSON Output

```json
{"buyer": "Amazon Web Services", "supplier": "Cloudflare Inc.", "po_number": "PO-AWS-2025-9182", "date": "2025-01-15", "delivery_date": null, "currency": "USD", "total": 26249.0, "items": [{"item_name": "Enterprise SSL Certificate", "quantity": 1, "unit_price": 4999.0}, {"item_name": "DDoS Protection Annual Plan", "quantity": 1, "unit_price": 12500.0}, {"item_name": "CDN Bandwidth 100TB/mo", "quantity": 1, "unit_price": 8750.0}]}
```

## Model's Actual Output

```json
{"vendor": "Cloudflare Inc.", "invoice_number": "PO-AWS-2025-9182", "date": "2025-01-15", "due_date": null, "currency": "USD", "subtotal": 26249.0, "tax": null, "total": 26249.0, "line_items": [{"description": "Enterprise SSL Certificate", "quantity": 1, "unit_price": 4999.0}, {"description": "DDoS Protection Annual Plan", "quantity": 1, "unit_price": 12500.0}, {"description": "CDN Bandwidth 100TB/mo", "quantity": 1, "unit_price": 8750.0}]}
```

## Analysis

### What went wrong
**Complete schema misidentification — used invoice schema instead of PO schema.** Despite the document saying "ORDER" and having a "PO-" prefix in the reference number, the model applied the invoice schema: `vendor` instead of `buyer`/`supplier`, `invoice_number` instead of `po_number`, `line_items` instead of `items`, `description` instead of `item_name`. The document was identified as an invoice rather than a purchase order.

### Why it likely failed
The document uses an extremely **sparse format** with no explicit "PURCHASE ORDER" header — it only says "ORDER". The "buyer to supplier" relationship is expressed as a single line "Amazon Web Services to Cloudflare Inc." which is ambiguous. Additionally:
1. The document uses "$" pricing which is more common in invoice training examples
2. The document has no "Buyer:" or "Supplier:" labels — the PO training data mostly uses explicit labels
3. The instruction prompt says "Extract all purchase order fields" but the minimal document styling may have made the model default to the more frequent invoice schema (50 examples vs 30)

### What training data change would fix it
1. Add 3–5 PO training examples with minimal/sparse formatting — no explicit "PURCHASE ORDER" header, just "ORDER" or "PO"
2. Add examples where buyer/supplier are expressed as "X to Y" on a single line
3. Add examples of **digital services** POs (cloud computing, SaaS subscriptions) since training data is heavily weighted toward physical goods
4. Include POs from tech companies to broaden the domain diversity beyond manufacturing/industrial
