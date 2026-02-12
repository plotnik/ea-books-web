# Grafana NPE
# ===========
#
# The CSV file exported from Grafana contains a column named "Line".  
# Each row in this column is a JSON object that includes a field called "body".
#
# For each row, extract the value of the "body" field and save it to a separate file named sequentially as `001.log`, `002.log`, and so on.  
# All these files should be written into a directory whose name is provided as a command-line argument.
#
# Locate the line in the output that contains “java.lang.NullPointerException,” then extract that line and the next five lines.
#
# ::

import csv
import json
import sys
import os
import hashlib
import json
import re
from pathlib import Path
from collections import defaultdict

if len(sys.argv) != 3:
    print("Usage: grafana-npe <input.csv> <output_folder>")
    sys.exit(1)
  
output_dir = Path(sys.argv[2])
csv_path = Path(output_dir, sys.argv[1])
    
# Separators in file
#
# ::
    
START_MARKER = "### NullPointerException"
END_MARKER = "### Body"
 
# Extract exceptions into output_dir
#
# ::
    
def extract_exceptions():
    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if "Line" not in reader.fieldnames:
            print("CSV does not contain a 'Line' column")
            sys.exit(1)

        for idx, row in enumerate(reader, start=1):
            result = ""

            raw_date = row.get("Date")
            result += raw_date + "\n\n"

            raw_json = row.get("Line", "").strip()
            if not raw_json:
                continue

            try:
                data = json.loads(raw_json)
            except json.JSONDecodeError as e:
                print(f"Skipping row {idx}: invalid JSON ({e})")
                continue

            body = data.get("body")
            if body is not None:
                result += body + "\n\n"

            result += f"### Stacktrace\n\n"
            attributes = data.get("attributes") or {}
            stacktrace = attributes.get("exception.stacktrace")
            if stacktrace:
                result += stacktrace + "\n\n"

            # Find in result the line containing "java.lang.NullPointerException" and extract this line and following 5 lines
            lines = result.splitlines()
            for i, line in enumerate(lines):
                if "java.lang.NullPointerException" in line:
                    extracted = "\n".join(lines[i:i + 6])
                    result = "### NullPointerException\n\n" + extracted + "\n\n### Body\n\n" + result
                    break

        
            filename = output_dir / f"{count + 1:03d}.log"
            with filename.open("w", encoding="utf-8") as out:
                out.write(result) 

            count += 1

    print(f"Extracted {count} files into '{output_dir}'")

 
# Normalize stack trace text so equivalent stacks match more often.
#
# - strip trailing whitespace
# - collapse multiple blank lines
# - remove variable CGLIB suffixes like ``$$FastClassBySpringCGLIB$$777f0e43``
#   (keeps the stable prefix)
#
# ::  
  
def normalize_stack(stack_text: str) -> str:
    lines = [ln.rstrip() for ln in stack_text.splitlines()]

    # Normalize dynamic Spring CGLIB class suffixes
    # Example: ApiOrderControllerV2$$FastClassBySpringCGLIB$$777f0e43 -> ApiOrderControllerV2$$FastClassBySpringCGLIB$$<id>
    cg_pattern = re.compile(r"(\$\$FastClassBySpringCGLIB\$\$)[0-9a-fA-F]+")
    lines = [cg_pattern.sub(r"\1<id>", ln) for ln in lines]

    # Collapse multiple blank lines
    out = []
    blank = False
    for ln in lines:
        if ln.strip() == "":
            if not blank:
                out.append("")
            blank = True
        else:
            out.append(ln)
            blank = False

    return "\n".join(out).strip()
    
# Extracts the NPE stack section:
# from '### NullPointerException' to just before '### Body'
# Returns None if markers not found.
#  
# ::
    
def extract_stack(text: str) -> str | None:
    start = text.find(START_MARKER)
    if start == -1:
        return None

    end = text.find(END_MARKER, start)
    if end == -1:
        # If no END_MARKER, take everything from start
        stack = text[start:]
    else:
        stack = text[start:end]

    return stack.strip()

# Create a stable short key for grouping and display.      
#
# ::
    
def stable_key(normalized_stack: str) -> str:
    h = hashlib.sha1(normalized_stack.encode("utf-8")).hexdigest()
    return h[:12]

# Group .log files by NPE stack trace.
#
# ::

def group_exceptions():

    folder = output_dir
    pattern = "*.log" # Glob pattern for log files
    report = None # Optional path to write JSON report (groups).
  
    if not folder.exists() or not folder.is_dir():
        raise SystemExit(f"Folder not found or not a directory: {folder}")

    files = sorted(folder.glob(pattern))
    if not files:
        raise SystemExit(f"No files matching '{pattern}' in {folder}")

    groups = defaultdict(list)         # key -> [filenames]
    stack_by_key = {}                  # key -> normalized stack
    missing_marker = []                # files without recognizable stack

    for p in files:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"Skipping {p.name}: read error: {e}")
            continue

        stack = extract_stack(text)
        if stack is None:
            missing_marker.append(p.name)
            continue

        norm = normalize_stack(stack)
        key = stable_key(norm)

        groups[key].append(p.name)
        stack_by_key.setdefault(key, norm)

    # Sort groups by size descending
    sorted_groups = sorted(groups.items(), key=lambda kv: len(kv[1]), reverse=True)

    print(f"Scanned folder: {folder}")
    print(f"Log files found: {len(files)}")
    print(f"Grouped by stack: {len(sorted_groups)}")
    if missing_marker:
        print(f"Files missing '{START_MARKER}' marker: {len(missing_marker)}")

    print("\n=== Groups (largest first) ===")
    for i, (key, names) in enumerate(sorted_groups, start=1):
        print(f"\n[{i}] group={key}  count={len(names)}")
        # Print a short "signature" line (top stack frame if present)
        norm_stack = stack_by_key[key]
        sig = next((ln.strip() for ln in norm_stack.splitlines() if ln.strip().startswith("at ")), None)
        if sig:
            print(f"    signature: {sig}")
        print(f"    files: {', '.join(names[:12])}" + (f" ... (+{len(names)-12} more)" if len(names) > 12 else ""))

    if report:
        report = {
            "folder": str(folder),
            "total_files": len(files),
            "missing_marker_files": missing_marker,
            "groups": [
                {
                    "key": key,
                    "count": len(names),
                    "files": names,
                    "normalized_stack": stack_by_key[key],
                }
                for key, names in sorted_groups
            ],
        }
        Path(report).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nWrote report: {report}")


# main
# ----
#
# ::

if __name__ == "__main__":
    extract_exceptions()
    group_exceptions()
  
