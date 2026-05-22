#!/usr/bin/env python3
"""Validate all submission deliverables for the Llama 3.2 Structured JSON Fine-Tuning task."""
import json, csv, os, sys

PASS = "\033[92m✅ PASS\033[0m"
FAIL = "\033[91m❌ FAIL\033[0m"
WARN = "\033[93m⚠️  WARN\033[0m"
total_pass = 0
total_fail = 0

def check(condition, msg):
    global total_pass, total_fail
    if condition:
        print(f"  {PASS} {msg}")
        total_pass += 1
    else:
        print(f"  {FAIL} {msg}")
        total_fail += 1
    return condition

def file_exists(path):
    return os.path.isfile(path)

def file_not_empty(path):
    return os.path.isfile(path) and os.path.getsize(path) > 10

# ═══════════════════════════════════════════════
print("\n" + "="*60)
print("  SUBMISSION VALIDATION REPORT")
print("="*60)

# ── 1. Required Files Exist ──
print("\n[1/8] Checking required files exist...")
required_files = [
    "schema/invoice_schema.md",
    "schema/po_schema.md",
    "data/curated_train.jsonl",
    "data/curation_log.md",
    "training_config.md",
    "screenshots/training_config.png",
    "screenshots/loss_curve.png",
    "eval/baseline_responses.md",
    "eval/baseline_scores.csv",
    "eval/summary.md",
    "eval/finetuned_responses.md",
    "eval/finetuned_scores.csv",
    "eval/before_vs_after.md",
    "eval/failures/failure_01.md",
    "eval/failures/failure_02.md",
    "eval/failures/failure_03.md",
    "eval/failures/failure_04.md",
    "eval/failures/failure_05.md",
    "prompts/prompt_iterations.md",
    "prompts/prompt_eval.md",
    "report.md",
    "README.md",
]
for f in required_files:
    check(file_not_empty(f), f"File exists and non-empty: {f}")

# ── 2. JSONL Validation ──
print("\n[2/8] Validating data/curated_train.jsonl...")
jsonl_path = "data/curated_train.jsonl"
if file_exists(jsonl_path):
    with open(jsonl_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    check(len(lines) == 80, f"Exactly 80 training examples (found {len(lines)})")
    
    inv_count = 0
    po_count = 0
    valid_json_count = 0
    null_fields = 0
    multi_items = 0
    non_usd = 0
    has_instruction = 0
    has_input = 0
    has_output = 0
    placeholder_inputs = 0
    
    inv_keys = {"vendor","invoice_number","date","due_date","currency","subtotal","tax","total","line_items"}
    po_keys = {"buyer","supplier","po_number","date","delivery_date","currency","total","items"}
    
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
            valid_json_count += 1
            
            if "instruction" in obj: has_instruction += 1
            if "input" in obj: has_input += 1
            if "output" in obj: has_output += 1
            
            # Check for placeholder inputs
            if obj.get("input","").startswith("<"):
                placeholder_inputs += 1
            
            # Parse output
            out = json.loads(obj.get("output","{}"))
            
            if "invoice" in obj.get("instruction","").lower():
                inv_count += 1
                # Check invoice schema keys
                if i < 3:  # spot-check first few
                    missing = inv_keys - set(out.keys())
                    if missing:
                        print(f"  {WARN} INV line {i+1} missing keys: {missing}")
            elif "purchase order" in obj.get("instruction","").lower():
                po_count += 1
                if i >= len(lines)-3:  # spot-check last few
                    missing = po_keys - set(out.keys())
                    if missing:
                        print(f"  {WARN} PO line {i+1} missing keys: {missing}")
            
            # Check for null fields
            if out.get("tax") is None or out.get("due_date") is None or out.get("delivery_date") is None:
                null_fields += 1
            
            # Check multi-item
            arr = out.get("line_items", out.get("items", []))
            if len(arr) >= 3:
                multi_items += 1
            
            # Check non-USD
            if out.get("currency","USD") != "USD":
                non_usd += 1
                
        except json.JSONDecodeError as e:
            print(f"  {FAIL} Line {i+1} is not valid JSON: {e}")
    
    check(valid_json_count == len(lines), f"All {len(lines)} lines are valid JSON")
    check(inv_count == 50, f"50 invoice examples (found {inv_count})")
    check(po_count == 30, f"30 purchase order examples (found {po_count})")
    check(has_instruction == len(lines), f"All examples have 'instruction' field")
    check(has_input == len(lines), f"All examples have 'input' field")
    check(has_output == len(lines), f"All examples have 'output' field")
    check(placeholder_inputs == 0, f"No placeholder inputs like '<invoice raw text...>' (found {placeholder_inputs})")
    check(null_fields >= 15, f"≥15 examples with null optional fields (found {null_fields})")
    check(multi_items >= 10, f"≥10 examples with 3+ line items (found {multi_items})")
    check(non_usd >= 5, f"≥5 examples with non-USD currency (found {non_usd})")

# ── 3. CSV Validation ──
print("\n[3/8] Validating eval/baseline_scores.csv...")
csv_path = "eval/baseline_scores.csv"
if file_exists(csv_path):
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    expected_cols = {"filename","raw_output_first_50_chars","is_valid_json","has_all_required_keys","key_accuracy","value_accuracy","notes"}
    actual_cols = set(reader.fieldnames) if reader.fieldnames else set()
    check(expected_cols.issubset(actual_cols), f"Baseline CSV has required columns: {expected_cols & actual_cols}")
    check(len(rows) == 20, f"Baseline CSV has 20 rows (found {len(rows)})")

print("\n[4/8] Validating eval/finetuned_scores.csv...")
csv_path2 = "eval/finetuned_scores.csv"
if file_exists(csv_path2):
    with open(csv_path2, "r", encoding="utf-8") as f:
        reader2 = csv.DictReader(f)
        rows2 = list(reader2)
    actual_cols2 = set(reader2.fieldnames) if reader2.fieldnames else set()
    check(expected_cols.issubset(actual_cols2), f"Finetuned CSV has required columns")
    check(len(rows2) == 20, f"Finetuned CSV has 20 rows (found {len(rows2)})")

# ── 4. Schema Files ──
print("\n[5/8] Validating schema files...")
for schema_file in ["schema/invoice_schema.md", "schema/po_schema.md"]:
    if file_exists(schema_file):
        content = open(schema_file, "r", encoding="utf-8").read()
        check(len(content) > 500, f"{schema_file} has substantial content ({len(content)} chars)")

# ── 5. Training Config ──
print("\n[6/8] Validating training_config.md...")
if file_exists("training_config.md"):
    tc = open("training_config.md", "r", encoding="utf-8").read().lower()
    check("lora" in tc, "training_config.md mentions LoRA")
    check("rank" in tc, "training_config.md mentions rank")
    check("alpha" in tc, "training_config.md mentions alpha")
    check("learning rate" in tc or "learning_rate" in tc, "training_config.md mentions learning rate")
    check("epoch" in tc, "training_config.md mentions epochs")
    check("batch" in tc, "training_config.md mentions batch size")
    check("justif" in tc or "reason" in tc or "because" in tc, "training_config.md contains justifications")
    check("loss" in tc and "curve" in tc, "training_config.md contains loss curve analysis")

# ── 6. Failure Analysis ──
print("\n[7/8] Validating failure analysis files...")
for i in range(1, 6):
    fp = f"eval/failures/failure_{i:02d}.md"
    if file_exists(fp):
        fc = open(fp, "r", encoding="utf-8").read().lower()
        check(len(fc) > 500, f"{fp} has substantial content")
        check("what went wrong" in fc or "wrong" in fc, f"{fp} describes what went wrong")
        check("why" in fc, f"{fp} analyzes why it failed")
        check("training data" in fc or "training" in fc, f"{fp} proposes training data fix")

# ── 7. Report ──
print("\n[8/8] Validating report.md...")
if file_exists("report.md"):
    report = open("report.md", "r", encoding="utf-8").read()
    word_count = len(report.split())
    check(word_count >= 250, f"report.md has ≥250 words ({word_count} words)")
    check("prompt" in report.lower() and "fine-tun" in report.lower(), "report.md discusses prompting vs fine-tuning")

# ═══════════════════════════════════════════════
print("\n" + "="*60)
print(f"  RESULTS: {total_pass} passed, {total_fail} failed")
print("="*60)

if total_fail == 0:
    print(f"\n  🎉 ALL CHECKS PASSED! Repository is ready for submission.\n")
else:
    print(f"\n  ⚠️  {total_fail} check(s) failed. Review the issues above.\n")

sys.exit(total_fail)
