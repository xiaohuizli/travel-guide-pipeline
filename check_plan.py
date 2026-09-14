#!/usr/bin/env python3
"""Check finite plan invariants; does not verify travel facts or HTML appearance."""
import argparse
import json
import re
from datetime import date, timedelta
from pathlib import Path


def check(root):
    errors, warnings = [], []
    def require(ok, message):
        if not ok:
            errors.append(message)
    def money(v):
        return type(v) is int and v >= 0
    try:
        brief, evidence, plan = [json.loads((root / n).read_text(encoding='utf-8'))
                                 for n in ('brief.json', 'evidence.json', 'plan.json')]
        if not all(isinstance(v, dict) for v in (brief, evidence, plan)):
            raise ValueError('Top-level JSON values must be objects')
        sources = evidence['sources']
        require(isinstance(sources, list), 'sources must be a list')
        ids = [s['id'] for s in sources]
        require(len(ids) == len(set(ids)), 'Duplicate source IDs')
        source_map = {s['id']: s for s in sources}
        for s in sources:
            require(bool(re.fullmatch(r'S[1-9]\d*', s['id'])), 'Invalid source ID: ' + str(s['id']))
            require(s.get('access') in ('full', 'partial', 'blocked'), 'Invalid access: ' + s['id'])
            require(isinstance(s.get('url'), str) and s['url'].startswith(('https://', 'http://')),
                    'Missing public URL: ' + s['id'])
            require(bool(s.get('retrieved_at')), 'Missing retrieval time: ' + s['id'])
        def refs(obj, label):
            values = obj.get('source_ids', [])
            require(isinstance(values, list), label + ': source_ids must be a list')
            for sid in values:
                require(sid in source_map, label + ': unknown source ' + str(sid))
            return values
        for f in evidence.get('facts', []):
            r = refs(f, 'Fact ' + str(f.get('id')))
            require(f.get('status') in ('verified', 'reported', 'unknown'), 'Invalid fact status')
            if f.get('status') in ('verified', 'reported'):
                require(bool(r), 'Sourced fact has no sources')
                require(any(source_map.get(i, {}).get('access') in ('full', 'partial') for i in r),
                        'Sourced fact relies only on missing/blocked sources')
        count = brief['days']
        require(type(count) is int and count > 0, 'brief.days must be a positive integer')
        days = plan['days']
        require(len(days) == count, 'Day count differs from brief')
        require([d['day'] for d in days] == list(range(1, len(days) + 1)), 'Day numbers are not contiguous')
        start = date.fromisoformat(brief['start_date']) if brief.get('start_date') else None
        if start and brief.get('end_date') and type(count) is int:
            require(date.fromisoformat(brief['end_date']) == start + timedelta(days=count - 1),
                    'Start/end dates disagree with day count')
        for i, d in enumerate(days):
            if start:
                require(d.get('date') == (start + timedelta(days=i)).isoformat(), 'Incorrect date on day ' + str(i + 1))
            for item in d.get('items', []):
                refs(item, 'Day ' + str(i + 1))
        total = 0
        for b in plan['budget']:
            value = b['amount_minor']
            require(money(value), 'Budget amounts must be nonnegative integer minor units')
            if money(value):
                total += value
            require(b.get('kind') in ('allocation', 'quote', 'estimate'), 'Invalid budget kind')
            require(bool(b.get('basis')), 'Missing budget unit/person basis')
            r = refs(b, 'Budget')
            if b.get('kind') == 'quote':
                require(bool(r), 'Quote has no source')
        require(money(plan['budget_total_minor']) and plan['budget_total_minor'] == total,
                'Budget total differs from line items or is invalid')
        limit = brief.get('budget_limit_minor')
        if limit is not None:
            require(money(limit), 'Invalid budget limit')
            if money(limit) and total > limit:
                warnings.append('Budget exceeds stated limit; resolve or disclose before delivery')
        media_ids = [m['id'] for m in evidence.get('media', [])]
        require(len(media_ids) == len(set(media_ids)), 'Duplicate media IDs')
        for m in evidence.get('media', []):
            require(m.get('source_id') in source_map, 'Unknown media source')
        guide = root / 'guide.md'
        if guide.exists():
            for ref in re.findall(r'\[([SM][1-9]\d*)\]', guide.read_text(encoding='utf-8')):
                require(ref in source_map or ref in media_ids, 'Unknown guide reference: ' + ref)
        else:
            warnings.append('guide.md missing; only structured plan was checked')
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        errors.append('Invalid or missing input: ' + str(exc))
    return {'errors': errors, 'warnings': warnings,
            'scope': 'Structure/date/budget/reference checks only; no fact or visual verification'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('work_dir', type=Path)
    result = check(parser.parse_args().work_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if result['errors'] else 0)
