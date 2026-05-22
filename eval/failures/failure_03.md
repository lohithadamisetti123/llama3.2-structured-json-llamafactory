# Failure Analysis — Additional Test Doc A (Invoice — Handwritten Style)

## Source Document Text

```
Dr. Patel's Clinic
Handwritten Invoice
~Inv no: HW-2025-03~
date: march 5 2025

- consultation (1hr)     1    Rs. 2,500
- blood test panel       1    Rs. 1,800  
- x-ray chest            2    Rs. 950 each

total Rs. 6,200
```

## Expected JSON Output

```json
{"vendor": "Dr. Patel's Clinic", "invoice_number": "HW-2025-03", "date": "2025-03-05", "due_date": null, "currency": "INR", "subtotal": 6200.0, "tax": null, "total": 6200.0, "line_items": [{"description": "consultation (1hr)", "quantity": 1, "unit_price": 2500.0}, {"description": "blood test panel", "quantity": 1, "unit_price": 1800.0}, {"description": "x-ray chest", "quantity": 2, "unit_price": 950.0}]}
```

## Model's Actual Output

```json
{"vendor": "Dr. Patel's Clinic", "invoice_number": "HW-2025-03", "date": "2025-03-05", "due_date": null, "currency": "INR", "subtotal": 6200.0, "tax": null, "total": 6200.0, "line_items": [{"description": "consultation (1hr)", "quantity": 1, "unit_price": 2500.0}, {"description": "blood test panel", "quantity": 1, "unit_price": 1800.0}, {"description": "x-ray chest", "quantity": 2, "unit_price": 1900.0}]}
```

## Analysis

### What went wrong
**Value extraction error — incorrect unit_price calculation.** The model returned `"unit_price": 1900.0` for x-ray chest instead of `950.0`. It appears the model multiplied the quantity (2) by the unit price (950) to get the line total (1900) and reported that as unit_price. The document says "Rs. 950 each" which clearly indicates 950 is the unit price, not the line total.

### Why it likely failed
The training data predominantly uses explicit formats like `x2 @950.00` or `Qty: 2, Rate: 950.00`. This document uses an ambiguous format: `2    Rs. 950 each`. The word "each" clarifies it's a unit price for humans, but the model may not have enough training examples with this phrasing. Additionally, the handwritten/informal style with tildes (`~`) and lowercase text is underrepresented in training data.

### What training data change would fix it
1. Add 3–4 training examples with "X each" or "per unit" phrasing in line items
2. Add 2–3 examples with informal/handwritten invoice styles (lowercase, abbreviations, symbols like ~)
3. Add examples from medical/clinic invoices specifically, as healthcare documents often use non-standard formatting
