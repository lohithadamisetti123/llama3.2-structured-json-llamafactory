# Purchase Order JSON Schema

Each model output for a purchase order MUST be a single valid JSON object with the following keys, no extra wrapping, no markdown, no code fences.

## Top-level keys

- `buyer` (string)  
  Organization or person placing the order.  
  If absent or illegible, use an empty string "".

- `supplier` (string)  
  Supplier or vendor receiving the order.  
  If absent, use an empty string "".

- `po_number` (string)  
  Purchase order identifier (e.g., "PO-2024-010").  
  If absent, use an empty string "".

- `date` (string, format "YYYY-MM-DD")  
  Date the PO was issued, converted to ISO format.  
  If missing or ambiguous, use null.

- `delivery_date` (string or null, format "YYYY-MM-DD")  
  Expected delivery date.  
  If not specified, use null.

- `currency` (string, 3-letter code)  
  Currency of the PO values (e.g., "USD", "INR").  
  If unknown but symbol suggests something, choose a consistent code; otherwise "XXX".

- `total` (float)  
  Numeric total amount of the PO.  
  If only line totals exist, compute a sum; if still impossible, use 0.0.

- `items` (array of objects)  
  Array of item objects; must always exist, can be empty only in truly item-less documents.

## `items` object schema

Each item object MUST contain:

- `item_name` (string)  
  Name or description of the item. If missing, use an empty string "".

- `quantity` (integer)  
  Ordered quantity; if missing, use 1.

- `unit_price` (float)  
  Unit price; if only line total is present, divide by quantity; if unknown, use 0.0.

## Absent or optional fields

- Use `null` for `date` and `delivery_date` when not present.
- Strings use empty string "" when the field exists conceptually but is blank or redacted.
- All keys MUST appear in every purchase order JSON; only their values may be null or empty as defined above.
