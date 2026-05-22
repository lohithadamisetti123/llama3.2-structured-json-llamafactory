# Failure Analysis — Additional Test Doc B (Invoice — Multi-Currency)

## Source Document Text

```
PROFORMA INVOICE

Exporter: Shanghai Electronics Corp.
Ref: SEC-CN-2025-0045
Date: 2025-04-18

Item                         Qty   Unit Price (USD)
LED Display Module 15.6"      100      45.00
HDMI Controller Board          50      28.00
Power Supply Unit 12V         100      12.50
Ribbon Cable 30cm             200       2.50

Subtotal: USD 7,150.00
Freight: USD 850.00
Total: USD 8,000.00

Bank: Industrial & Commercial Bank of China
SWIFT: ICBKCNBJ
```

## Expected JSON Output

```json
{"vendor": "Shanghai Electronics Corp.", "invoice_number": "SEC-CN-2025-0045", "date": "2025-04-18", "due_date": null, "currency": "USD", "subtotal": 7150.0, "tax": null, "total": 8000.0, "line_items": [{"description": "LED Display Module 15.6\"", "quantity": 100, "unit_price": 45.0}, {"description": "HDMI Controller Board", "quantity": 50, "unit_price": 28.0}, {"description": "Power Supply Unit 12V", "quantity": 100, "unit_price": 12.5}, {"description": "Ribbon Cable 30cm", "quantity": 200, "unit_price": 2.5}]}
```

## Model's Actual Output

```json
{"vendor": "Shanghai Electronics Corp.", "invoice_number": "SEC-CN-2025-0045", "date": "2025-04-18", "due_date": null, "currency": "USD", "subtotal": 7150.0, "tax": null, "total": 8000.0, "line_items": [{"description": "LED Display Module 15.6\"", "quantity": 100, "unit_price": 45.0}, {"description": "HDMI Controller Board", "quantity": 50, "unit_price": 28.0}, {"description": "Power Supply Unit 12V", "quantity": 100, "unit_price": 12.5}, {"description": "Ribbon Cable 30cm", "quantity": 200, "unit_price": 2.5}, {"description": "Freight", "quantity": 1, "unit_price": 850.0}]}
```

## Analysis

### What went wrong
**Hallucinated line item — freight added as a line item.** The model added `{"description": "Freight", "quantity": 1, "unit_price": 850.0}` as a fifth line item. In the source document, "Freight: USD 850.00" is a separate charge line between Subtotal and Total — it is NOT a product/service line item. The model incorrectly treated it as a line item because it appears in a similar position and format.

### Why it likely failed
The training data does not include examples with **non-line-item charges** (freight, handling fees, discounts) that appear between subtotal and total. The model has learned that any itemized amount between the header and the total is a line item. This is a **schema gap** — our schema doesn't have a field for additional charges, so the model forces freight into the nearest available array.

### What training data change would fix it
1. Add 3–5 training examples with extra charges (freight, shipping, handling, discount) that appear between subtotal and total — with these charges NOT included in line_items
2. Modify the instruction to explicitly state: "Do not include shipping, freight, or handling charges in line_items"
3. Consider adding an optional `additional_charges` field to the schema for documents that commonly have non-line-item charges
