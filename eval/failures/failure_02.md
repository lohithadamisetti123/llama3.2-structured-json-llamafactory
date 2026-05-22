# Failure Analysis — EVAL-020 (PO — BMW Group)

## Source Document Text

```
PO# BMW-MUC-2025-0056  |  Date: 2025-01-28
From: BMW Group, Munich
To: Rhine Machinery GmbH

Item Name          | Qty | Unit Price
---------------------------------------------
CNC Milling Head   |   3 |   18500.00
Precision Bearing   |  20 |     420.00
Coolant Pump Unit   |   5 |    2300.00

Order Total: 75400.00 EUR
```

## Expected JSON Output

```json
{"buyer": "BMW Group", "supplier": "Rhine Machinery GmbH", "po_number": "BMW-MUC-2025-0056", "date": "2025-01-28", "delivery_date": null, "currency": "EUR", "total": 75400.0, "items": [{"item_name": "CNC Milling Head", "quantity": 3, "unit_price": 18500.0}, {"item_name": "Precision Bearing", "quantity": 20, "unit_price": 420.0}, {"item_name": "Coolant Pump Unit", "quantity": 5, "unit_price": 2300.0}]}
```

## Model's Actual Output

```json
{"buyer": "BMW Group", "supplier": "Rhine Machinery GmbH", "po_number": "BMW-MUC-2025-0056", "date": "2025-01-28", "delivery_date": null, "currency": "EUR", "total": 75400.0, "line_items": [{"item_name": "CNC Milling Head", "quantity": 3, "unit_price": 18500.0}, {"item_name": "Precision Bearing", "quantity": 20, "unit_price": 420.0}, {"item_name": "Coolant Pump Unit", "quantity": 5, "unit_price": 2300.0}]}
```

## Analysis

### What went wrong
**Key naming error — schema confusion.** The model used `"line_items"` (the invoice schema key) instead of `"items"` (the PO schema key) for the items array. The JSON is valid and all values are correct, but the key name violates the purchase order schema. This is a cross-schema contamination issue.

### Why it likely failed
The instruction prompt says "Extract all purchase order fields" but the model has been trained on both invoice and PO examples. The document's tabular format with "Item Name | Qty | Unit Price" header closely resembles invoice training examples that use `line_items`. The model conflated the two schemas because:
1. The document header says "PO#" but the table format is invoice-like
2. The `line_items` key appears in 50 training examples vs `items` in only 30
3. The inner object keys (`item_name`, `quantity`, `unit_price`) are nearly identical between schemas

### What training data change would fix it
1. Add 5 PO training examples that use tabular "Item Name | Qty | Price" format specifically (this format currently appears mostly in invoice examples)
2. Add 3 training examples where the same document could be an invoice or PO, with the instruction clearly distinguishing which schema to apply
3. Consider adding the document type as a field in the output JSON (e.g., `"document_type": "purchase_order"`) to reinforce schema awareness
