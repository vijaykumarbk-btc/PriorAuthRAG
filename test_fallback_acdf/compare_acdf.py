import re
import difflib
from pathlib import Path

old_path = Path("hierarchical-processing/Cigna_ACDF_hierarchical.md")
new_path = Path("test_fallback_acdf/Cigna_ACDF.hierarchical.md")

old_text = old_path.read_text(encoding="utf-8")
new_text = new_path.read_text(encoding="utf-8")

print("=== 1. DOCUMENT SIZE & VOLUME ===")
print(f"Old File (Docling):        {len(old_text):>7} chars | {len(old_text.splitlines()):>5} lines | {len(old_text.split()):>5} words")
print(f"New File (Fallback Tier):  {len(new_text):>7} chars | {len(new_text.splitlines()):>5} lines | {len(new_text.split()):>5} words")

def extract_headings(text):
    return [line.strip() for line in text.splitlines() if line.strip().startswith("#")]

old_headings = extract_headings(old_text)
new_headings = extract_headings(new_text)

print("\n=== 2. HEADING COMPARISON ===")
print(f"Old Headings Total: {len(old_headings)}")
print(f"New Headings Total: {len(new_headings)}")

print("\nSample Old Headings:")
for h in old_headings[:10]:
    print("  OLD:", h)

print("\nSample New Headings:")
for h in new_headings[:10]:
    print("  NEW:", h)

sections = [
    "CMM-601: Anterior Cervical Discectomy and Fusion",
    "CMM-601.1: General Guidelines",
    "CMM-601.2: Osteotomy",
    "CMM-601.3: Anterior Cervical Discectomy",
    "CMM-601.4: Initial Primary Anterior Cervical Discectomy and Fusion",
    "CMM-601.5: Anterior Cervical Corpectomy",
    "CMM-601.6: Repeat Anterior Cervical Discectomy and Fusion",
    "CMM-601.7: Adjacent Segment Disease",
    "CMM-601.8: ACDF Following Failed Cervical Disc Arthroplasty",
    "CMM-601.9: Non-Indications",
    "Codes (CMM-601)",
    "Evidence Discussion",
    "References (CMM-601)"
]

print("\n=== 3. CLINICAL SECTION COVERAGE ===")
for s in sections:
    in_old = any(s.lower() in h.lower() for h in old_headings)
    in_new = any(s.lower() in h.lower() for h in new_headings)
    status_old = "FOUND" if in_old else "MISSING"
    status_new = "FOUND" if in_new else "MISSING"
    print(f"  {s[:55]:<55} | Old: {status_old:<7} | New: {status_new:<7}")

# Check tables
old_tables = old_text.count("| --- |") + old_text.count("|---|") + old_text.count("|---")
new_tables = new_text.count("| --- |") + new_text.count("|---|")
print("\n=== 4. TABLE EXTRACTION ===")
print(f"Old Markdown Tables: {old_text.count('|---|') + old_text.count('| --- |') + old_text.count('--- |')}")
print(f"New Markdown Tables: {new_text.count('| --- |')}")

# Vocabulary overlap
words_old = set(re.findall(r"\b\w+\b", old_text.lower()))
words_new = set(re.findall(r"\b\w+\b", new_text.lower()))
jaccard = len(words_old & words_new) / len(words_old | words_new)
overlap_old = len(words_old & words_new) / len(words_old)
overlap_new = len(words_old & words_new) / len(words_new)

print("\n=== 5. VOCABULARY OVERLAP ===")
print(f"Shared Unique Words:      {len(words_old & words_new)}")
print(f"Vocabulary Jaccard:       {jaccard * 100:.2f}%")
print(f"Old Vocabulary Retained:  {overlap_old * 100:.2f}%")
print(f"New Vocabulary in Old:    {overlap_new * 100:.2f}%")
