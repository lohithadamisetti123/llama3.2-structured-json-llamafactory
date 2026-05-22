# Baseline Responses — Llama 3.2 3B-Instruct (Pre Fine-Tuning)

**Model**: meta-llama/Llama-3.2-3B-Instruct (base, no fine-tuning)
**Prompt used**: "Extract all invoice fields and return ONLY a valid JSON object. No explanation, no markdown, no code fences."
**Evaluation set**: 20 held-out documents (15 invoices + 5 purchase orders) NOT in training data

---

## EVAL-001 (Invoice — TechWorld Electronics)

**Input document**:
```
TechWorld Electronics
123 Silicon Ave, San Jose, CA 95134
Invoice No: TW-2025-0481
Date: March 12, 2025
Bill To: DataCore Systems

Item                    Qty    Unit Price
Network Switch 24p      2      450.00
Cat6 Cable Box          5       35.00
Rack Mount Kit          2       75.00

Subtotal: 1,125.00
Tax (9%): 101.25
Total: $1,226.25
Due Date: April 11, 2025
```

**Raw model output**:
```
Here is the extracted data in JSON format:

```json
{
  "vendor": "TechWorld Electronics",
  "invoice_number": "TW-2025-0481",
  "date": "2025-03-12",
  "due_date": "2025-04-11",
  "currency": "USD",
  "subtotal": 1125.00,
  "tax": 101.25,
  "total": 1226.25,
  "line_items": [
    {"description": "Network Switch 24p", "quantity": 2, "unit_price": 450.00},
    {"description": "Cat6 Cable Box", "quantity": 5, "unit_price": 35.00},
    {"description": "Rack Mount Kit", "quantity": 2, "unit_price": 75.00}
  ]
}
```

The above JSON contains all the invoice fields extracted from the document.
```

**Parse result**: ❌ FAIL — prose preamble + markdown code fences + trailing explanation

---

## EVAL-002 (Invoice — GreenValley Farms)

**Input document**:
```
INVOICE
GreenValley Farms Ltd.
Invoice #: GVF-8834
Date: 2025-01-20

Organic Apples 10kg     x12    @18.50
Whole Wheat Flour 5kg   x8     @12.00
Honey Jar 1L            x20    @22.00

Subtotal: 758.00
Total: 758.00
Currency: USD
```

**Raw model output**:
```
{"vendor": "GreenValley Farms Ltd.", "invoice_number": "GVF-8834", "date": "2025-01-20", "due_date": null, "currency": "USD", "subtotal": 758.0, "tax": null, "total": 758.0, "line_items": [{"description": "Organic Apples 10kg", "quantity": 12, "unit_price": 18.5}, {"description": "Whole Wheat Flour 5kg", "quantity": 8, "unit_price": 12.0}, {"description": "Honey Jar 1L", "quantity": 20, "unit_price": 22.0}]}
```

**Parse result**: ✅ PASS — valid JSON, all keys present

---

## EVAL-003 (Invoice — Sakura Tech Japan)

**Input document**:
```
========================================
Sakura Tech Co., Ltd.
Tokyo, Japan
========================================
Invoice: SKT-2025-112
Date: 2025-02-28
Currency: JPY
----------------------------------------
  Precision Sensor Unit    x4   @32000
  Control Board v3         x2   @85000
  Wiring Harness           x10  @4500
----------------------------------------
Subtotal: 343000
Tax (10%): 34300
TOTAL: 377300
========================================
```

**Raw model output**:
```
```json
{
  "vendor_name": "Sakura Tech Co., Ltd.",
  "invoice_id": "SKT-2025-112",
  "invoice_date": "2025-02-28",
  "currency": "JPY",
  "sub_total": 343000,
  "tax_amount": 34300,
  "grand_total": 377300,
  "items": [
    {"name": "Precision Sensor Unit", "qty": 4, "price": 32000},
    {"name": "Control Board v3", "qty": 2, "price": 85000},
    {"name": "Wiring Harness", "qty": 10, "price": 4500}
  ]
}
```
```

**Parse result**: ❌ FAIL — markdown fences + wrong key names (vendor_name, invoice_id, sub_total, items instead of line_items)

---

## EVAL-004 (Invoice — Rhine Engineering GmbH)

**Input document**:
```
TAX INVOICE
Seller: Rhine Engineering GmbH, Düsseldorf
Invoice Ref: RE-DE-2024-789
Issue Date: 15.11.2024
Due Date: 15.12.2024
Currency: EUR

1. Industrial Valve DN50 — Qty: 6, Rate: 285.00 EUR
2. Pressure Gauge 0-10bar — Qty: 12, Rate: 45.00 EUR
3. Pipe Fitting Set — Qty: 3, Rate: 120.00 EUR

Net Amount: 2610.00
Tax (19%): 495.90
Invoice Total: 3105.90 EUR
```

**Raw model output**:
```
Based on the invoice, here are the extracted fields:

{
  "vendor": "Rhine Engineering GmbH",
  "invoice_number": "RE-DE-2024-789",
  "date": "2024-11-15",
  "due_date": "2024-12-15",
  "currency": "EUR",
  "subtotal": 2610.00,
  "tax": 495.90,
  "total": 3105.90,
  "line_items": [
    {"description": "Industrial Valve DN50", "quantity": 6, "unit_price": 285.00},
    {"description": "Pressure Gauge 0-10bar", "quantity": 12, "unit_price": 45.00},
    {"description": "Pipe Fitting Set", "quantity": 3, "unit_price": 120.00}
  ]
}
```

**Parse result**: ❌ FAIL — prose preamble "Based on the invoice..."

---

## EVAL-005 (Invoice — ClearView Optics)

**Input document**:
```
ClearView Optics | Invoice CV-5567 | 2025-04-01
Lens Kit Pro(2x899.99) / Filter Set(1x249.00)
Total=2048.98 USD
```

**Raw model output**:
```
{"vendor": "ClearView Optics", "invoice_number": "CV-5567", "date": "2025-04-01", "due_date": null, "currency": "USD", "subtotal": 2048.98, "tax": 0.0, "total": 2048.98, "line_items": [{"description": "Lens Kit Pro", "quantity": 2, "unit_price": 899.99}, {"description": "Filter Set", "quantity": 1, "unit_price": 249.0}]}
```

**Parse result**: ✅ PASS — valid JSON, all keys present

---

## EVAL-006 (Invoice — Mumbai Textiles)

**Input document**:
```
VENDOR: Mumbai Silk Textiles Pvt. Ltd.
INV NO: MST-2025-034    DATE: 2025-03-08
+──────────────────────────────────────────────+
| Silk Saree 6m          |     3|   4500.00|
| Cotton Fabric 10m      |    10|    850.00|
| Thread Spool           |    25|     45.00|
| Embroidery Kit         |     5|    320.00|
+──────────────────────────────────────────────+
Subtotal: 23225.00 INR
Tax: 4180.50 INR
Grand Total: 27405.50 INR
```

**Raw model output**:
```
Here's the JSON extraction:

```json
{
  "vendor": "Mumbai Silk Textiles Pvt. Ltd.",
  "invoice_number": "MST-2025-034",
  "date": "2025-03-08",
  "due_date": null,
  "currency": "INR",
  "subtotal": 23225.0,
  "tax": 4180.5,
  "total": 27405.5,
  "line_items": [
    {"description": "Silk Saree 6m", "quantity": 3, "unit_price": 4500.0},
    {"description": "Cotton Fabric 10m", "quantity": 10, "unit_price": 850.0},
    {"description": "Thread Spool", "quantity": 25, "unit_price": 45.0},
    {"description": "Embroidery Kit", "quantity": 5, "unit_price": 320.0}
  ]
}
```
```

**Parse result**: ❌ FAIL — markdown code fences + prose preamble

---

## EVAL-007 (Invoice — BlueStar Services)

**Input document**:
```
BlueStar Cleaning Services
Invoice Number: BS-2025-0190
Date Issued: 2025-05-01
Due: 2025-05-31

Services Rendered:
- Office Deep Clean (Level 3)    1    $350.00
- Window Washing (exterior)      1    $275.00

Subtotal: $625.00
Sales Tax: $50.00
Amount Due: $675.00
```

**Raw model output**:
```
{
  "vendor": "BlueStar Cleaning Services",
  "invoice_number": "BS-2025-0190",
  "date": "2025-05-01",
  "due_date": "2025-05-31",
  "currency": "USD",
  "subtotal": 625.0,
  "tax": 50.0,
  "total": 675.0,
  "line_items": [
    {"description": "Office Deep Clean (Level 3)", "quantity": 1, "unit_price": 350.0},
    {"description": "Window Washing (exterior)", "quantity": 1, "unit_price": 275.0}
  ]
}
```

**Parse result**: ✅ PASS — valid JSON with correct keys

---

## EVAL-008 (Invoice — Nordic Marine)

**Input document**:
```
INVOICE
Nordic Marine Supplies AS
Stavanger, Norway
Inv#: NMS-NO-2024-55
Dated: 07-Sep-2024

Anchor Chain 30m     3    1200.00
Marine Paint 20L     6     340.00
Life Jacket Adult    12    125.00

Sub-total: 5,640.00
VAT (25%): 1,410.00
Total Due: 7,050.00 EUR
Pay by: 07-Oct-2024
```

**Raw model output**:
```
I'll extract the invoice fields for you:

{
  "vendor": "Nordic Marine Supplies AS",
  "invoice_number": "NMS-NO-2024-55",
  "date": "September 7, 2024",
  "due_date": "October 7, 2024",
  "currency": "EUR",
  "subtotal": 5640.00,
  "tax": 1410.00,
  "total": 7050.00,
  "line_items": [
    {"description": "Anchor Chain 30m", "quantity": 3, "unit_price": 1200.0},
    {"description": "Marine Paint 20L", "quantity": 6, "unit_price": 340.0},
    {"description": "Life Jacket Adult", "quantity": 12, "unit_price": 125.0}
  ]
}

Note: The dates have been formatted for readability.
```

**Parse result**: ❌ FAIL — prose preamble + trailing note + date not in YYYY-MM-DD format

---

## EVAL-009 (Invoice — Pinnacle IT)

**Input document**:
```
Pinnacle IT Solutions
Tax Invoice #PIT-2025-223
05/02/2025

Laptop Dell Latitude 5540   x1   @1249.00
Docking Station WD19        x1   @189.00
USB-C Monitor 27"           x2   @329.00

Subtotal: 2096.00
GST (18%): 377.28
Grand Total: 2473.28 USD
Due: 05/03/2025
```

**Raw model output**:
```
```json
{
  "vendor": "Pinnacle IT Solutions",
  "invoice_number": "PIT-2025-223",
  "date": "2025-02-05",
  "due_date": "2025-03-05",
  "currency": "USD",
  "subtotal": 2096.0,
  "tax": 377.28,
  "total": 2473.28,
  "line_items": [
    {"description": "Laptop Dell Latitude 5540", "quantity": 1, "unit_price": 1249.0},
    {"description": "Docking Station WD19", "quantity": 1, "unit_price": 189.0},
    {"description": "USB-C Monitor 27\"", "quantity": 2, "unit_price": 329.0}
  ]
}
```
```

**Parse result**: ❌ FAIL — markdown code fences

---

## EVAL-010 (Invoice — Atlas Building)

**Input document**:
```
Atlas Building Materials
123 Construction Blvd, Houston TX
INVOICE: ABM-10042
DATE: 2025-01-15

Portland Cement 50kg        x100   @8.50
Rebar 12mm 6m               x200   @6.25
Plywood 18mm 4x8            x50    @32.00

Subtotal: $3,850.00
Tax: $346.50
Total: $4,196.50
```

**Raw model output**:
```
{"vendor":"Atlas Building Materials","invoice_number":"ABM-10042","date":"2025-01-15","due_date":null,"currency":"USD","subtotal":3850.0,"tax":346.5,"total":4196.5,"line_items":[{"description":"Portland Cement 50kg","quantity":100,"unit_price":8.5},{"description":"Rebar 12mm 6m","quantity":200,"unit_price":6.25},{"description":"Plywood 18mm 4x8","quantity":50,"unit_price":32.0}]}
```

**Parse result**: ✅ PASS — valid JSON, all keys correct

---

## EVAL-011 (Invoice — Heritage Crafts)

**Input document**:
```
Heritage Handmade Crafts
Invoice HHC/2024/456
28 December 2024

Wooden Chess Set       2     £85.00
Ceramic Vase Large     1     £120.00
Hand-woven Basket      4     £35.00

Total: £430.00
Currency: GBP
```

**Raw model output**:
```
Sure! Here is the extracted JSON:

{
  "vendor": "Heritage Handmade Crafts",
  "invoice_number": "HHC/2024/456",
  "date": "2024-12-28",
  "currency": "GBP",
  "subtotal": 430.0,
  "total": 430.0,
  "line_items": [
    {"description": "Wooden Chess Set", "quantity": 2, "unit_price": 85.0},
    {"description": "Ceramic Vase Large", "quantity": 1, "unit_price": 120.0},
    {"description": "Hand-woven Basket", "quantity": 4, "unit_price": 35.0}
  ]
}
```

**Parse result**: ❌ FAIL — prose preamble + missing keys (due_date, tax)

---

## EVAL-012 (Invoice — Quantum Labs)

**Input document**:
```
QUANTUM RESEARCH LABS
Invoice: QRL-2025-0087
Date: 2025-03-20
Payment Due: 2025-04-19

Oscilloscope 200MHz      1     2,450.00
Signal Generator         1     1,890.00
BNC Cable Set            3        45.00
Probe Kit 10:1           2       125.00
Soldering Station        1       385.00

Subtotal: $5,120.00
Tax (8.5%): $435.20
Total: $5,555.20
```

**Raw model output**:
```
```json
{
  "vendor": "QUANTUM RESEARCH LABS",
  "invoice_number": "QRL-2025-0087",
  "date": "2025-03-20",
  "due_date": "2025-04-19",
  "currency": "USD",
  "subtotal": 5120.0,
  "tax": 435.2,
  "total": 5555.2,
  "line_items": [
    {"description": "Oscilloscope 200MHz", "quantity": 1, "unit_price": 2450.0},
    {"description": "Signal Generator", "quantity": 1, "unit_price": 1890.0},
    {"description": "BNC Cable Set", "quantity": 3, "unit_price": 45.0},
    {"description": "Probe Kit 10:1", "quantity": 2, "unit_price": 125.0},
    {"description": "Soldering Station", "quantity": 1, "unit_price": 385.0}
  ]
}
```
```

**Parse result**: ❌ FAIL — markdown code fences

---

## EVAL-013 (Invoice — SunCoast Catering)

**Input document**:
```
SunCoast Catering Co.
PH: 555-0134
Inv: SCC-9921  |  Date: 04/15/2025

Corporate Lunch Buffet     1    $850.00
Beverage Package           1    $225.00
Setup & Cleanup Fee        1    $150.00

Total: $1,225.00
```

**Raw model output**:
```
{"vendor": "SunCoast Catering Co.", "invoice_number": "SCC-9921", "date": "2025-04-15", "due_date": null, "currency": "USD", "subtotal": 1225.0, "tax": null, "total": 1225.0, "line_items": [{"description": "Corporate Lunch Buffet", "quantity": 1, "unit_price": 850.0}, {"description": "Beverage Package", "quantity": 1, "unit_price": 225.0}, {"description": "Setup & Cleanup Fee", "quantity": 1, "unit_price": 150.0}]}
```

**Parse result**: ✅ PASS — valid JSON, all keys present

---

## EVAL-014 (Invoice — Nile Exports)

**Input document**:
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

**Raw model output**:
```
Let me extract the relevant fields:

**Invoice Details:**

{
  "vendor": "NILE COTTON EXPORTS",
  "invoice_number": "NCE-EG-2025-018",
  "invoice_date": "2025-02-10",
  "payment_due_date": "2025-03-10",
  "currency": "USD",
  "subtotal": 2275.0,
  "tax": 0.0,
  "total": 2275.0,
  "items": [
    {"item": "Egyptian Cotton 100tc 50m", "qty": 20, "rate": 45.0},
    {"item": "Linen Blend 30m", "qty": 15, "rate": 62.0},
    {"item": "Silk Thread 1000m Spool", "qty": 50, "rate": 8.5}
  ]
}
```

**Parse result**: ❌ FAIL — prose + bold markdown + wrong key names (invoice_date, payment_due_date, items, item, qty, rate)

---

## EVAL-015 (Invoice — SwiftLogistics)

**Input document**:
```
SwiftLogistics International
COMMERCIAL INVOICE
Ref: SLI/2025/March/042
Dated: 2025-03-18

Freight Charge (Mumbai→Rotterdam)    1    $4,500.00
Customs Clearance Fee                1      $350.00
Documentation Fee                    1      $125.00
Insurance Premium                    1      $280.00

Subtotal: $5,255.00
Tax: N/A
Total Payable: $5,255.00
Due: Upon Receipt
```

**Raw model output**:
```
Here is the JSON:
{
  "vendor": "SwiftLogistics International",
  "invoice_number": "SLI/2025/March/042",
  "date": "2025-03-18",
  "due_date": "Upon Receipt",
  "currency": "USD",
  "subtotal": 5255.0,
  "tax": "N/A",
  "total": 5255.0,
  "line_items": [
    {"description": "Freight Charge (Mumbai to Rotterdam)", "quantity": 1, "unit_price": 4500.0},
    {"description": "Customs Clearance Fee", "quantity": 1, "unit_price": 350.0},
    {"description": "Documentation Fee", "quantity": 1, "unit_price": 125.0},
    {"description": "Insurance Premium", "quantity": 1, "unit_price": 280.0}
  ]
}
```

**Parse result**: ❌ FAIL — prose preamble + due_date should be null (not string) + tax should be null (not string "N/A")

---

## EVAL-016 (PO — Tata Motors)

**Input document**:
```
PURCHASE ORDER

Buyer: Tata Motors Limited
Supplier: Magna Industrial Parts
PO Number: TM-PO-2025-0088
Date: 2025-04-01
Delivery Date: 2025-04-30
Currency: INR

Items:
  - Brake Disc Assembly: Qty 500 @ 1,250.00
  - Suspension Spring Set: Qty 200 @ 3,400.00
  - Wheel Bearing Kit: Qty 1000 @ 450.00

Total: INR 1,955,000.00
```

**Raw model output**:
```
```json
{
  "buyer": "Tata Motors Limited",
  "supplier": "Magna Industrial Parts",
  "po_number": "TM-PO-2025-0088",
  "date": "2025-04-01",
  "delivery_date": "2025-04-30",
  "currency": "INR",
  "total": 1955000.0,
  "items": [
    {"item_name": "Brake Disc Assembly", "quantity": 500, "unit_price": 1250.0},
    {"item_name": "Suspension Spring Set", "quantity": 200, "unit_price": 3400.0},
    {"item_name": "Wheel Bearing Kit", "quantity": 1000, "unit_price": 450.0}
  ]
}
```
```

**Parse result**: ❌ FAIL — markdown code fences (JSON content itself is correct)

---

## EVAL-017 (PO — Samsung Electronics)

**Input document**:
```
PO# SE-KR-2025-334  |  Date: 2025-03-15  |  Deliver by: 2025-05-01
From: Samsung Electronics Co.
To: Crystal Clear Optics

Item Name          | Qty | Unit Price
---------------------------------------------
OLED Panel 6.7"    |  50 |    1200.00
Camera Module 48MP |  50 |     650.00
Battery Cell 5000  | 100 |      85.00

Order Total: 107500.00 USD
```

**Raw model output**:
```
{"buyer": "Samsung Electronics Co.", "supplier": "Crystal Clear Optics", "po_number": "SE-KR-2025-334", "date": "2025-03-15", "delivery_date": "2025-05-01", "currency": "USD", "total": 107500.0, "items": [{"item_name": "OLED Panel 6.7\"", "quantity": 50, "unit_price": 1200.0}, {"item_name": "Camera Module 48MP", "quantity": 50, "unit_price": 650.0}, {"item_name": "Battery Cell 5000", "quantity": 100, "unit_price": 85.0}]}
```

**Parse result**: ✅ PASS — valid JSON, all keys correct

---

## EVAL-018 (PO — Siemens AG)

**Input document**:
```
OFFICIAL PURCHASE ORDER

Order Reference: SIE-DE-2025-0712
Date Issued: 2025-02-20
Required Delivery: 2025-06-15

Purchasing Organization: Siemens AG
Vendor: Horizon Energy Systems

Order Details:
  1. Power Transformer 500kVA — 2 units at EUR 24,500.00 each
  2. Circuit Breaker 630A — 10 units at EUR 1,850.00 each
  3. Control Panel Assembly — 5 units at EUR 8,200.00 each

Total Order Value: EUR 108,500.00

Authorized Signature: ___________
```

**Raw model output**:
```
Based on the purchase order document, I've extracted the following:

{
  "purchaser": "Siemens AG",
  "vendor": "Horizon Energy Systems",
  "order_number": "SIE-DE-2025-0712",
  "order_date": "2025-02-20",
  "delivery_deadline": "2025-06-15",
  "currency": "EUR",
  "total_value": 108500.0,
  "order_items": [
    {"product": "Power Transformer 500kVA", "units": 2, "price_per_unit": 24500.0},
    {"product": "Circuit Breaker 630A", "units": 10, "price_per_unit": 1850.0},
    {"product": "Control Panel Assembly", "units": 5, "price_per_unit": 8200.0}
  ]
}
```

**Parse result**: ❌ FAIL — prose preamble + all key names wrong (purchaser, order_number, order_date, delivery_deadline, total_value, order_items, product, units, price_per_unit)

---

## EVAL-019 (PO — Toyota Motor)

**Input document**:
```
PURCHASE ORDER
Buyer: Toyota Motor Corporation
Supplier: Titan Auto Parts Ltd.
PO Number: TMC-JP-2025-189
Date: 2025-04-10

Items:
  - Engine Gasket Set: Qty 300 @ 85.00
  - Oil Filter Element: Qty 500 @ 12.50
  - Timing Belt Kit: Qty 150 @ 145.00

Total: 53,500.00 JPY
```

**Raw model output**:
```
{
  "buyer": "Toyota Motor Corporation",
  "supplier": "Titan Auto Parts Ltd.",
  "po_number": "TMC-JP-2025-189",
  "date": "2025-04-10",
  "delivery_date": null,
  "currency": "JPY",
  "total": 53500.0,
  "items": [
    {"item_name": "Engine Gasket Set", "quantity": 300, "unit_price": 85.0},
    {"item_name": "Oil Filter Element", "quantity": 500, "unit_price": 12.5},
    {"item_name": "Timing Belt Kit", "quantity": 150, "unit_price": 145.0}
  ]
}
```

**Parse result**: ✅ PASS — valid JSON, all keys correct

---

## EVAL-020 (PO — BMW Group)

**Input document**:
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

**Raw model output**:
```
Here are the extracted purchase order fields:

```json
{
  "buyer": "BMW Group",
  "supplier": "Rhine Machinery GmbH",
  "po_number": "BMW-MUC-2025-0056",
  "date": "2025-01-28",
  "delivery_date": null,
  "currency": "EUR",
  "total": 75400.0,
  "items": [
    {"item_name": "CNC Milling Head", "quantity": 3, "unit_price": 18500.0},
    {"item_name": "Precision Bearing", "quantity": 20, "unit_price": 420.0},
    {"item_name": "Coolant Pump Unit", "quantity": 5, "unit_price": 2300.0}
  ]
}
```
```

**Parse result**: ❌ FAIL — prose preamble + markdown code fences
