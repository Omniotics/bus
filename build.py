#!/usr/bin/env python3
"""
build.py

Concatenate modules into a single book. Modules are sorted by their IDs.
Outputs `build/book.md`.
"""
import os
import yaml
import argparse
from pathlib import Path


def load_module_contents(mod_dir):
    modules = []
    for fname in sorted(os.listdir(mod_dir)):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(mod_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        if not text.startswith('---'):
            continue
        front, body = text.split('---', 2)[1:]  # front matter and body
        data = yaml.safe_load(front)
        body = body.strip()
        modules.append((data['id'], data.get('title', data['id']), body))
    return modules


def build_book(mod_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    modules = load_module_contents(mod_dir)
    parts = ["# Omniotics Manuscript\n"]
    for mid, title, body in modules:
        parts.append(f"\n## {title} ({mid})\n")
        parts.append(body)
    book = "\n\n".join(parts)
    out_path = os.path.join(out_dir, 'book.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(book)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Build the Omniotics manuscript")
    parser.add_argument('--modules', default='modules', help='Directory containing modules')
    parser.add_argument('--out', default='build', help='Output directory')
    args = parser.parse_args()
    path = build_book(args.modules, args.out)
    print(f"Wrote {path}")


if __name__ == '__main__':
    main()