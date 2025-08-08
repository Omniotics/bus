#!/usr/bin/env python3
"""
reader_paths.py

Validate and build reader path specific manuscripts.

Usage:
  python reader_paths.py --check
  python reader_paths.py --build

When run with --build, generates one manuscript per path in `build/paths/`.
"""
import os
import yaml
import argparse
from typing import List


def load_modules(mod_dir):
    modules = {}
    for fname in os.listdir(mod_dir):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(mod_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        if not text.startswith('---'):
            continue
        parts = text.split('---', 2)
        front = yaml.safe_load(parts[1])
        body = parts[2].strip() if len(parts) > 2 else ''
        modules[front['id']] = {
            'title': front.get('title', front['id']),
            'body': body
        }
    return modules


def check_paths(modules, reader_paths_file):
    errors = []
    data = yaml.safe_load(open(reader_paths_file, 'r', encoding='utf-8'))
    for path in data.get('paths', []):
        name = path.get('name')
        for mid in path.get('modules', []) or []:
            if mid not in modules:
                errors.append(f"Reader path {name} references missing module {mid}")
    return errors


def build_paths(modules, reader_paths_file, out_dir):
    data = yaml.safe_load(open(reader_paths_file, 'r', encoding='utf-8'))
    for path in data.get('paths', []):
        name = path.get('name')
        os.makedirs(os.path.join(out_dir, 'paths'), exist_ok=True)
        out_path = os.path.join(out_dir, 'paths', f"{name}.md")
        parts: List[str] = [f"# {path.get('description', name).strip().capitalize()}\n"]
        for mid in path.get('modules', []) or []:
            if mid not in modules:
                continue
            title = modules[mid]['title']
            body = modules[mid]['body']
            parts.append(f"\n## {title} ({mid})\n")
            parts.append(body)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(parts))
        print(f"Wrote {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Validate and build reader paths")
    parser.add_argument('--modules', default='modules', help='Modules directory')
    parser.add_argument('--reader_paths', default='chapters/reader_paths.yml', help='Reader paths YAML')
    parser.add_argument('--out', default='build', help='Output directory')
    parser.add_argument('--check', action='store_true', help='Only check paths')
    args = parser.parse_args()

    modules = load_modules(args.modules)
    if args.check:
        errors = check_paths(modules, args.reader_paths)
        if errors:
            print("READER PATH CHECK FAILED")
            for e in errors:
                print(" -", e)
            raise SystemExit(1)
        else:
            print("READER PATH CHECK PASSED")
    else:
        errors = check_paths(modules, args.reader_paths)
        if errors:
            print("READER PATH CHECK FAILED; aborting build")
            for e in errors:
                print(" -", e)
            raise SystemExit(1)
        build_paths(modules, args.reader_paths, args.out)


if __name__ == '__main__':
    main()