#!/usr/bin/env python3
"""
check.py

This script validates the structure of the Omniotics modular book repository. It checks that:
  * Module dependencies exist and do not exceed 5 per module.
  * Claims referenced in modules exist.
  * Dependency graph has no cycles.
  * Reader paths reference existing modules.

Run with no arguments from the repository root.
"""

import yaml
import os
import sys
import argparse


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
        if len(parts) < 3:
            continue
        front = yaml.safe_load(parts[1])
        modules[front['id']] = front
    return modules


def load_claims(claim_dir):
    claims = {}
    for fname in os.listdir(claim_dir):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(claim_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        if not text.startswith('---'):
            continue
        parts = text.split('---', 2)
        if len(parts) < 3:
            continue
        front = yaml.safe_load(parts[1])
        claims[front['id']] = front
    return claims


def validate(modules, claims):
    """Return a list of validation error messages."""
    errors = []
    # Dependency existence and count
    for mid, mod in modules.items():
        deps = mod.get('depends_on') or []
        if len(deps) > 5:
            errors.append(f"Module {mid} has more than 5 dependencies")
        for dep in deps:
            if dep not in modules:
                errors.append(f"Module {mid} depends on missing module {dep}")
    # Claims existence
    for mid, mod in modules.items():
        for claim in mod.get('claims') or []:
            if claim not in claims:
                errors.append(f"Module {mid} references missing claim {claim}")
    # Cycle detection via DFS
    visited = {}

    def dfs(node, stack):
        visited[node] = True
        stack.add(node)
        for dep in modules[node].get('depends_on') or []:
            if dep not in modules:
                continue
            if dep not in visited:
                if dfs(dep, stack):
                    return True
            elif dep in stack:
                errors.append(f"Cycle detected: {node} -> {dep}")
                return True
        stack.remove(node)
        return False

    for mid in modules:
        if mid not in visited:
            dfs(mid, set())
    return errors


def check_reader_paths(modules, reader_paths_file):
    errors = []
    if not reader_paths_file or not os.path.exists(reader_paths_file):
        return errors
    with open(reader_paths_file, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
        except Exception as exc:
            return [f"Failed to parse reader paths YAML: {exc}"]
    for path in data.get('paths', []):
        name = path.get('name')
        for mid in path.get('modules', []) or []:
            if mid not in modules:
                errors.append(f"Reader path {name} references missing module {mid}")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate Omniotics modular book structure")
    parser.add_argument('--modules', default='modules', help='Directory containing module files')
    parser.add_argument('--claims', default='claims', help='Directory containing claim files')
    parser.add_argument('--reader_paths', default='chapters/reader_paths.yml', help='Reader paths YAML file')
    args = parser.parse_args()

    modules = load_modules(args.modules)
    claims = load_claims(args.claims)

    errors = validate(modules, claims)
    errors += check_reader_paths(modules, args.reader_paths)

    if errors:
        print("CHECK FAILED")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("CHECK PASSED")
        sys.exit(0)


if __name__ == '__main__':
    main()