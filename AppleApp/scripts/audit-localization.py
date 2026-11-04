#!/usr/bin/env python3
"""Portable catalog checks and conservative Swift literal inventory (not AST coverage)."""
import json
import re
from pathlib import Path
from collections import Counter

root = Path(__file__).resolve().parents[1]
catalog = json.loads((root / 'Resources/Localization/Localizable.xcstrings').read_text())
strings = catalog['strings']
def parameters(text):
    pattern = r'%(?:(\d+)\$)?(?:[-+ #0]*)(?:\d+)?(?:\.\d+)?(lld|llu|ld|lu|@|d|u|f|s)'
    result = []
    for index, match in enumerate(re.finditer(pattern, text.replace('%%', '')), 1):
        result.append((int(match[1] or index), match[2]))
    return Counter(result)

errors = []
missing = []
translated = 0
for key, entry in strings.items():
    unit = entry.get('localizations', {}).get('zh-TW', {}).get('stringUnit', {})
    if not unit.get('value'):
        missing.append(key)
        continue
    translated += 1
    if parameters(key) != parameters(unit['value']):
        errors.append(key)
    hant = entry.get('localizations', {}).get('zh-Hant', {}).get('stringUnit', {})
    assert hant == unit, key
assert not errors, f'Parameter mismatches: {errors}'

# Every Swift file, including engine and authentication, is inventoried without
# mutating it. Includes logs, identifiers and API strings: manual triage required.
literals = []
swift = sorted(root.rglob('*.swift'))
for path in swift:
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if line.lstrip().startswith('//'):
            continue
        for match in re.finditer(r'"((?:\\.|[^"\\])*)"', line):
            value = match[1]
            if re.search('[A-Za-z]', value) and value not in strings:
                literals.append({'path': str(path.relative_to(root)), 'line': number, 'literal': value})
report = {'swift_files_scanned': len(swift), 'catalog_entries': len(strings),
          'zh_TW_entries': translated, 'catalog_coverage_percent': round(translated / len(strings) * 100, 2),
          'missing_catalog_keys': missing, 'unclassified_source_literals': literals}
out = root / 'localization-audit.json'
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if not isinstance(v, list)}, ensure_ascii=False))
print(f'PASS: format parameters and zh-Hant fallback parity. Inventory: {out.name}')
