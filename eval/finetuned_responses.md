# Fine-Tuned Model Responses — Llama 3.2 3B-Instruct + LoRA

**Model**: Llama-3.2-3B-Instruct fine-tuned with LoRA (rank=16, alpha=32, 3 epochs)
**Prompt used**: Same as baseline — "Extract all invoice fields and return ONLY a valid JSON object. No explanation, no markdown, no code fences."
**Evaluation set**: Same 20 held-out documents as baseline

---

## EVAL-001 (Invoice — TechWorld Electronics)

**Raw model output**:
```
{"vendor": "TechWorld Electronics", "invoice_number": "TW-2025-0481", "date": "2025-03-12", "due_date": "2025-04-11", "currency": "USD", "subtotal": 1125.0, "tax": 101.25, "total": 1226.25, "line_items": [{"description": "Network Switch 24p", "quantity": 2, "unit_price": 450.0}, {"description": "Cat6 Cable Box", "quantity": 5, "unit_price": 35.0}, {"description": "Rack Mount Kit", "quantity": 2, "unit_price": 75.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-002 (Invoice — GreenValley Farms)

**Raw model output**:
```
{"vendor": "GreenValley Farms Ltd.", "invoice_number": "GVF-8834", "date": "2025-01-20", "due_date": null, "currency": "USD", "subtotal": 758.0, "tax": null, "total": 758.0, "line_items": [{"description": "Organic Apples 10kg", "quantity": 12, "unit_price": 18.5}, {"description": "Whole Wheat Flour 5kg", "quantity": 8, "unit_price": 12.0}, {"description": "Honey Jar 1L", "quantity": 20, "unit_price": 22.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-003 (Invoice — Sakura Tech Japan)

**Raw model output**:
```
{"vendor": "Sakura Tech Co., Ltd.", "invoice_number": "SKT-2025-112", "date": "2025-02-28", "due_date": null, "currency": "JPY", "subtotal": 343000.0, "tax": 34300.0, "total": 377300.0, "line_items": [{"description": "Precision Sensor Unit", "quantity": 4, "unit_price": 32000.0}, {"description": "Control Board v3", "quantity": 2, "unit_price": 85000.0}, {"description": "Wiring Harness", "quantity": 10, "unit_price": 4500.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-004 (Invoice — Rhine Engineering GmbH)

**Raw model output**:
```
{"vendor": "Rhine Engineering GmbH", "invoice_number": "RE-DE-2024-789", "date": "2024-11-15", "due_date": "2024-12-15", "currency": "EUR", "subtotal": 2610.0, "tax": 495.9, "total": 3105.9, "line_items": [{"description": "Industrial Valve DN50", "quantity": 6, "unit_price": 285.0}, {"description": "Pressure Gauge 0-10bar", "quantity": 12, "unit_price": 45.0}, {"description": "Pipe Fitting Set", "quantity": 3, "unit_price": 120.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-005 (Invoice — ClearView Optics)

**Raw model output**:
```
{"vendor": "ClearView Optics", "invoice_number": "CV-5567", "date": "2025-04-01", "due_date": null, "currency": "USD", "subtotal": 2048.98, "tax": null, "total": 2048.98, "line_items": [{"description": "Lens Kit Pro", "quantity": 2, "unit_price": 899.99}, {"description": "Filter Set", "quantity": 1, "unit_price": 249.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-006 (Invoice — Mumbai Textiles)

**Raw model output**:
```
{"vendor": "Mumbai Silk Textiles Pvt. Ltd.", "invoice_number": "MST-2025-034", "date": "2025-03-08", "due_date": null, "currency": "INR", "subtotal": 23225.0, "tax": 4180.5, "total": 27405.5, "line_items": [{"description": "Silk Saree 6m", "quantity": 3, "unit_price": 4500.0}, {"description": "Cotton Fabric 10m", "quantity": 10, "unit_price": 850.0}, {"description": "Thread Spool", "quantity": 25, "unit_price": 45.0}, {"description": "Embroidery Kit", "quantity": 5, "unit_price": 320.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-007 (Invoice — BlueStar Services)

**Raw model output**:
```
{"vendor": "BlueStar Cleaning Services", "invoice_number": "BS-2025-0190", "date": "2025-05-01", "due_date": "2025-05-31", "currency": "USD", "subtotal": 625.0, "tax": 50.0, "total": 675.0, "line_items": [{"description": "Office Deep Clean (Level 3)", "quantity": 1, "unit_price": 350.0}, {"description": "Window Washing (exterior)", "quantity": 1, "unit_price": 275.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-008 (Invoice — Nordic Marine)

**Raw model output**:
```
{"vendor": "Nordic Marine Supplies AS", "invoice_number": "NMS-NO-2024-55", "date": "2024-09-07", "due_date": "2024-10-07", "currency": "EUR", "subtotal": 5640.0, "tax": 1410.0, "total": 7050.0, "line_items": [{"description": "Anchor Chain 30m", "quantity": 3, "unit_price": 1200.0}, {"description": "Marine Paint 20L", "quantity": 6, "unit_price": 340.0}, {"description": "Life Jacket Adult", "quantity": 12, "unit_price": 125.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-009 (Invoice — Pinnacle IT)

**Raw model output**:
```
{"vendor": "Pinnacle IT Solutions", "invoice_number": "PIT-2025-223", "date": "2025-02-05", "due_date": "2025-03-05", "currency": "USD", "subtotal": 2096.0, "tax": 377.28, "total": 2473.28, "line_items": [{"description": "Laptop Dell Latitude 5540", "quantity": 1, "unit_price": 1249.0}, {"description": "Docking Station WD19", "quantity": 1, "unit_price": 189.0}, {"description": "USB-C Monitor 27\"", "quantity": 2, "unit_price": 329.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-010 (Invoice — Atlas Building)

**Raw model output**:
```
{"vendor": "Atlas Building Materials", "invoice_number": "ABM-10042", "date": "2025-01-15", "due_date": null, "currency": "USD", "subtotal": 3850.0, "tax": 346.5, "total": 4196.5, "line_items": [{"description": "Portland Cement 50kg", "quantity": 100, "unit_price": 8.5}, {"description": "Rebar 12mm 6m", "quantity": 200, "unit_price": 6.25}, {"description": "Plywood 18mm 4x8", "quantity": 50, "unit_price": 32.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-011 (Invoice — Heritage Crafts)

**Raw model output**:
```
{"vendor": "Heritage Handmade Crafts", "invoice_number": "HHC/2024/456", "date": "2024-12-28", "due_date": null, "currency": "GBP", "subtotal": 430.0, "tax": null, "total": 430.0, "line_items": [{"description": "Wooden Chess Set", "quantity": 2, "unit_price": 85.0}, {"description": "Ceramic Vase Large", "quantity": 1, "unit_price": 120.0}, {"description": "Hand-woven Basket", "quantity": 4, "unit_price": 35.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-012 (Invoice — Quantum Labs)

**Raw model output**:
```
{"vendor": "QUANTUM RESEARCH LABS", "invoice_number": "QRL-2025-0087", "date": "2025-03-20", "due_date": "2025-04-19", "currency": "USD", "subtotal": 5120.0, "tax": 435.2, "total": 5555.2, "line_items": [{"description": "Oscilloscope 200MHz", "quantity": 1, "unit_price": 2450.0}, {"description": "Signal Generator", "quantity": 1, "unit_price": 1890.0}, {"description": "BNC Cable Set", "quantity": 3, "unit_price": 45.0}, {"description": "Probe Kit 10:1", "quantity": 2, "unit_price": 125.0}, {"description": "Soldering Station", "quantity": 1, "unit_price": 385.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-013 (Invoice — SunCoast Catering)

**Raw model output**:
```
{"vendor": "SunCoast Catering Co.", "invoice_number": "SCC-9921", "date": "2025-04-15", "due_date": null, "currency": "USD", "subtotal": 1225.0, "tax": null, "total": 1225.0, "line_items": [{"description": "Corporate Lunch Buffet", "quantity": 1, "unit_price": 850.0}, {"description": "Beverage Package", "quantity": 1, "unit_price": 225.0}, {"description": "Setup & Cleanup Fee", "quantity": 1, "unit_price": 150.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-014 (Invoice — Nile Exports)

**Raw model output**:
```
The extracted invoice data is:
{"vendor": "NILE COTTON EXPORTS", "invoice_number": "NCE-EG-2025-018", "date": "2025-02-10", "due_date": "2025-03-10", "currency": "USD", "subtotal": 2275.0, "tax": 0.0, "total": 2275.0, "line_items": [{"description": "Egyptian Cotton 100tc 50m", "quantity": 20, "unit_price": 45.0}, {"description": "Linen Blend 30m", "quantity": 15, "unit_price": 62.0}, {"description": "Silk Thread 1000m Spool", "quantity": 50, "unit_price": 8.5}]}
```
**Parse result**: ❌ FAIL — prose preamble "The extracted invoice data is:" before JSON

---

## EVAL-015 (Invoice — SwiftLogistics)

**Raw model output**:
```
{"vendor": "SwiftLogistics International", "invoice_number": "SLI/2025/March/042", "date": "2025-03-18", "due_date": null, "currency": "USD", "subtotal": 5255.0, "tax": null, "total": 5255.0, "line_items": [{"description": "Freight Charge (Mumbai-Rotterdam)", "quantity": 1, "unit_price": 4500.0}, {"description": "Customs Clearance Fee", "quantity": 1, "unit_price": 350.0}, {"description": "Documentation Fee", "quantity": 1, "unit_price": 125.0}, {"description": "Insurance Premium", "quantity": 1, "unit_price": 280.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-016 (PO — Tata Motors)

**Raw model output**:
```
{"buyer": "Tata Motors Limited", "supplier": "Magna Industrial Parts", "po_number": "TM-PO-2025-0088", "date": "2025-04-01", "delivery_date": "2025-04-30", "currency": "INR", "total": 1955000.0, "items": [{"item_name": "Brake Disc Assembly", "quantity": 500, "unit_price": 1250.0}, {"item_name": "Suspension Spring Set", "quantity": 200, "unit_price": 3400.0}, {"item_name": "Wheel Bearing Kit", "quantity": 1000, "unit_price": 450.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-017 (PO — Samsung Electronics)

**Raw model output**:
```
{"buyer": "Samsung Electronics Co.", "supplier": "Crystal Clear Optics", "po_number": "SE-KR-2025-334", "date": "2025-03-15", "delivery_date": "2025-05-01", "currency": "USD", "total": 107500.0, "items": [{"item_name": "OLED Panel 6.7\"", "quantity": 50, "unit_price": 1200.0}, {"item_name": "Camera Module 48MP", "quantity": 50, "unit_price": 650.0}, {"item_name": "Battery Cell 5000", "quantity": 100, "unit_price": 85.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-018 (PO — Siemens AG)

**Raw model output**:
```
{"buyer": "Siemens AG", "supplier": "Horizon Energy Systems", "po_number": "SIE-DE-2025-0712", "date": "2025-02-20", "delivery_date": "2025-06-15", "currency": "EUR", "total": 108500.0, "items": [{"item_name": "Power Transformer 500kVA", "quantity": 2, "unit_price": 24500.0}, {"item_name": "Circuit Breaker 630A", "quantity": 10, "unit_price": 1850.0}, {"item_name": "Control Panel Assembly", "quantity": 5, "unit_price": 8200.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-019 (PO — Toyota Motor)

**Raw model output**:
```
{"buyer": "Toyota Motor Corporation", "supplier": "Titan Auto Parts Ltd.", "po_number": "TMC-JP-2025-189", "date": "2025-04-10", "delivery_date": null, "currency": "JPY", "total": 53500.0, "items": [{"item_name": "Engine Gasket Set", "quantity": 300, "unit_price": 85.0}, {"item_name": "Oil Filter Element", "quantity": 500, "unit_price": 12.5}, {"item_name": "Timing Belt Kit", "quantity": 150, "unit_price": 145.0}]}
```
**Parse result**: ✅ PASS

---

## EVAL-020 (PO — BMW Group)

**Raw model output**:
```
{"buyer": "BMW Group", "supplier": "Rhine Machinery GmbH", "po_number": "BMW-MUC-2025-0056", "date": "2025-01-28", "delivery_date": null, "currency": "EUR", "total": 75400.0, "line_items": [{"item_name": "CNC Milling Head", "quantity": 3, "unit_price": 18500.0}, {"item_name": "Precision Bearing", "quantity": 20, "unit_price": 420.0}, {"item_name": "Coolant Pump Unit", "quantity": 5, "unit_price": 2300.0}]}
```
**Parse result**: ❌ FAIL — used `line_items` instead of `items` for PO schema (wrong key name)
