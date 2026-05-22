# Invoice JSON Schema

Each model output for an invoice MUST be a single valid JSON object with the following keys, no extra wrapping, no markdown, no code fences.

## Top-level keys

- `vendor` (string)  
  Contains the vendor or seller name exactly as it appears on the invoice (trimmed).  
  If absent or illegible, use an empty string "".

- `invoice_number` (string)  
  Contains the invoice identifier or number (e.g., "INV-2024-001").  
  If absent, use an empty string "".

- `date` (string, format "YYYY-MM-DD")  
  Contains the invoice issue date converted to ISO format (e.g., "2024-03-15").  
  If date is missing or ambiguous, use null.

- `due_date` (string or null, format "YYYY-MM-DD")  
  Contains the payment due date in ISO format.  
  If the due date is absent, use null.

- `currency` (string, 3-letter ISO code)  
  Contains a 3-letter currency code (e.g., "USD", "INR", "EUR").  
  If the code is missing but symbol indicates something obvious (e.g., "₹"), choose a consistent valid code; if still unclear, use "XXX".

- `subtotal` (float)  
  Numeric subtotal amount before tax.  
  If the invoice does not explicitly show subtotal, compute it from line items where possible; otherwise use 0.0.

- `tax` (float or null)  
  Numeric tax amount.  
  If invoice has no tax field or it's clearly zero, use 0.0; if tax presence is unknown, use null.

- `total` (float)  
  Numeric total amount (subtotal + tax + other charges as shown).  
  Must always be provided; if not shown, sum line items and use that total.

- `line_items` (array of objects)  
  Array of line item objects. Must be present and can be empty if truly no items.

## `line_items` object schema

Each line item object MUST contain:

- `description` (string)  
  Item description or product/service name. If absent, use an empty string "".

- `quantity` (integer)  
  Quantity ordered or billed; if not present, use 1.

- `unit_price` (float)  
  Unit price of the item; if only total line value is available, divide by quantity; if unknown, use 0.0.

## Absent or optional fields

- Use `null` for `date` and `due_date` when not present.
- Use `null` for `tax` only when the presence of tax cannot be determined.
- Use `""` (empty string) for optional string fields that are conceptually present but blank (e.g., vendor name redacted).
- All keys MUST always appear in every invoice JSON; only their values may be null or empty as defined above.
