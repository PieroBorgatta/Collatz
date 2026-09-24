#!/usr/bin/env python3
"""Generate an auditable aggregate Lean source; NOT a modular build substitute.

Run in a prepared external assembly. Original source files remain unchanged.
Only import headers are hoisted, sections added, and two colliding private
identifiers alpha-renamed. A manifest records every source and transformation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re


def sha(data):
    return hashlib.sha256(data).hexdigest()


def code_mask(text):
    """Preserve offsets/newlines while masking nested comments and strings."""
    result = list(text)
    i, depth = 0, 0
    while i < len(text):
        if depth:
            if text.startswith('/-', i):
                result[i:i+2] = '  '; depth += 1; i += 2
            elif text.startswith('-/', i):
                result[i:i+2] = '  '; depth -= 1; i += 2
            else:
                if text[i] != '\n': result[i] = ' '
                i += 1
        elif text.startswith('/-', i):
            result[i:i+2] = '  '; depth = 1; i += 2
        elif text.startswith('--', i):
            stop = text.find('\n', i)
            if stop < 0: stop = len(text)
            result[i:stop] = ' ' * (stop-i); i = stop
        elif text[i] == '"':
            result[i] = ' '; i += 1
            closed = False
            while i < len(text):
                ch = text[i]
                if ch != '\n': result[i] = ' '
                i += 1
                if ch == '\\' and i < len(text):
                    if text[i] != '\n': result[i] = ' '
                    i += 1
                elif ch == '"':
                    closed = True; break
            if not closed: raise ValueError('Unclosed string')
        else: i += 1
    if depth: raise ValueError('Unclosed comment')
    return ''.join(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('targets', nargs='+')
    parser.add_argument('--output', default='WeightedVerifiedBundle.lean')
    args = parser.parse_args()
    root = Path.cwd()
    output = Path(args.output)
    if output.is_symlink():
        raise ValueError('Refusing to overwrite a symlink')
    if output.exists():
        previous = output.with_suffix('.manifest.json')
        if not previous.exists() or json.loads(previous.read_text()).get('aggregate_sha256') != sha(output.read_bytes()):
            raise ValueError('Refusing to overwrite a source without its matching aggregate receipt')
    local = {str(p.relative_to(root)).removesuffix('.lean').replace('/', '.'): p
             for p in root.rglob('*.lean')
             if not any(x in {'.lake', 'build'} for x in p.relative_to(root).parts)
             and p.name != Path(args.output).name}
    order, visiting, imports, sources = [], set(), {}, {}
    external = set()
    pattern = re.compile(r'^[^\S\n]*((?:public[^\S\n]+)?import)[^\S\n]+([^\n]+)', re.M)
    def visit(name):
        if name not in local:
            if name.split('.')[0] not in {'Mathlib', 'Lean', 'Std', 'Init'}:
                raise ValueError('Unknown external import: ' + name)
            external.add(name); return
        if name in imports: return
        if name in visiting: raise ValueError('Import cycle: ' + name)
        visiting.add(name)
        source = local[name].read_bytes().decode('utf-8')
        if '\r' in source: raise ValueError('Only LF source line endings supported: ' + name)
        mask = code_mask(source)
        children = [s for m in pattern.finditer(mask) for s in m[2].split()]
        for child in children: visit(child)
        imports[name] = children; sources[name] = source
        visiting.remove(name); order.append(name)
    for target in args.targets:
        if target not in local: raise ValueError('Missing target: ' + target)
        visit(target)
    collision_modules = {
        'Erdos1135.ND.PositiveDensity.ExplicitNumericalPrimitiveDecay',
        'Erdos1135.ND.PositiveDensity.ExplicitNumericalSyracuseMixing'}
    lines = ['/- Generated aggregate verification source. Apache-2.0 upstream; see UPSTREAM_NOTICE. -/']
    lines += ['import ' + x for x in sorted(external)]
    lines += ['']
    rows = []
    for index, name in enumerate(order):
        source = sources[name]
        mask = code_mask(source)
        changes = []
        for m in pattern.finditer(mask):
            start = m.start(1)
            changes.append((start, m.end(), '-- imports hoisted to aggregate header'))
        renames = {}
        if name in collision_modules:
            replacement = 'coefficient_cast_aggregate_' + str(index)
            renames['coefficient_cast'] = replacement
            for m in re.finditer(r'(?<![\w\'])coefficient_cast(?![\w\'])', mask):
                changes.append((m.start(), m.end(), replacement))
        for start, end, value in sorted(changes, reverse=True):
            source = source[:start] + value + source[end:]
        section = 'AggregateSource' + str(index)
        lines += ['', '/- BEGIN ' + name + ' -/', 'section ' + section]
        start_line = len(lines) + 1
        lines += source.splitlines()
        rows.append({'module': name, 'source_sha256': sha(sources[name].encode()),
                     'imports': imports[name], 'private_alpha_renames': renames,
                     'aggregate_first_source_line': start_line,
                     'aggregate_last_source_line': len(lines)})
        lines += ['end ' + section, '/- END ' + name + ' -/']
        if index % 25 == 0 or name in args.targets:
            lines += ['run_cmd Lean.logInfo "aggregate checked through ' + name + '"']
    data = ('\n'.join(lines) + '\n').encode()
    output = Path(args.output)
    output.write_bytes(data)
    manifest = {'verification_kind': 'aggregate elaboration, not modular build',
                'targets': args.targets, 'source_modules': len(order),
                'external_imports': sorted(external), 'aggregate_sha256': sha(data),
                'transformations': ['hoist import headers', 'wrap each original module in a section',
                                    'alpha-rename two colliding private identifiers',
                                    'insert progress log commands'],
                'sources': rows}
    output.with_suffix('.manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'modules': len(order), 'external_imports': len(external),
                      'lines': len(lines), 'output': str(output)}))


if __name__ == '__main__':
    main()
