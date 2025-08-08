#!/usr/bin/env python3
"""
graph.py

Generate a dependency graph of modules.
Outputs a Graphviz dot file (`build/graph.dot`) and a plain text edge list (`build/graph.txt`).
"""
import os
import yaml
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
        front = yaml.safe_load(parts[1])
        modules[front['id']] = {
            'title': front.get('title', front['id']),
            'depends_on': front.get('depends_on') or []
        }
    return modules


def write_graph(modules, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    dot_lines = ["digraph Modules {", "  rankdir=LR;"]
    txt_lines = []
    for mid, mod in modules.items():
        label = mod['title'].replace('"', '\"')
        dot_lines.append(f'  "{mid}" [label="{label}\n({mid})"];')
    for mid, mod in modules.items():
        for dep in mod['depends_on']:
            dot_lines.append(f'  "{mid}" -> "{dep}";')
            txt_lines.append(f'{mid} -> {dep}')
    dot_lines.append("}")
    with open(os.path.join(out_dir, 'graph.dot'), 'w', encoding='utf-8') as f:
        f.write("\n".join(dot_lines))
    with open(os.path.join(out_dir, 'graph.txt'), 'w', encoding='utf-8') as f:
        f.write("\n".join(txt_lines))


def main():
    parser = argparse.ArgumentParser(description="Generate module dependency graph")
    parser.add_argument('--modules', default='modules', help='Modules directory')
    parser.add_argument('--out', default='build', help='Output directory')
    args = parser.parse_args()
    modules = load_modules(args.modules)
    write_graph(modules, args.out)
    print(f"Wrote {os.path.join(args.out, 'graph.dot')} and graph.txt")


if __name__ == '__main__':
    main()