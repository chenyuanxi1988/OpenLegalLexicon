"""Local, offline query and export; remote updates are an explicit command."""
import argparse
import json
from pathlib import Path
import sys

from .export import export_bundle
from .io import write_json
from .model import DOMAINS, load_entries, quality_report, select
from .validate import validate_entries, validate_sources


def parser():
    p = argparse.ArgumentParser(prog='oll', description='可追溯的中英文法律词汇')
    p.add_argument('--root', type=Path, default=Path.cwd(), help='repository data root; default: current directory')
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('validate', help='validate source licenses, hashes, schema and references')
    query = sub.add_parser('search', help='search Chinese, English, pinyin and IDs')
    query.add_argument('query', nargs='?', default='')
    query.add_argument('--limit', type=int, default=20)
    query.add_argument('--json', action='store_true')
    query.add_argument('--include-quarantined', action='store_true')
    build = sub.add_parser('build', help='build an attributed offline distribution')
    build.add_argument('--out', type=Path, required=True)
    for child in [query,build]:
        child.add_argument('--domain', choices=DOMAINS)
        child.add_argument('--jurisdiction', choices=['CN','TW','HK','SG','US','UK','EU','INTERNATIONAL'])
        child.add_argument('--origin', choices=['CN','TW','HK','SG','US','UK','EU','INTERNATIONAL'])
    report = sub.add_parser('report',help='report coverage, ambiguity and review gaps')
    report.add_argument('--out', type=Path)
    ingest = sub.add_parser('import-snapshot',help='explicitly re-extract previously downloaded public source documents')
    ingest.add_argument('--cache', type=Path, required=True)
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == 'import-snapshot':
            from .ingest import import_snapshot
            print(json.dumps(import_snapshot(args.root,args.cache),ensure_ascii=False))
            return 0
        errors = validate_sources(args.root)
        if errors:
            raise ValueError('\n'.join(errors))
        entries,sources = load_entries(args.root)
        errors = validate_entries(entries,sources,args.root)
        if errors:
            raise ValueError('\n'.join(errors))
        if args.command == 'validate':
            print(f'OK: {len(entries)} entries; {sum(s["expected_records"] for s in sources)} source records; {len(sources)} licensed sources')
        elif args.command == 'report':
            result = quality_report(entries,sources)
            if args.out:
                write_json(args.out,result)
            else:
                print(json.dumps(result,ensure_ascii=False,indent=2))
        else:
            filters = {key:getattr(args,key,None) for key in ['domain','jurisdiction','origin']}
            if args.command == 'build':
                chosen = select(entries, **filters)
                print(json.dumps(export_bundle(chosen,sources,args.root,args.out,filters),ensure_ascii=False))
            else:
                if args.limit < 1:
                    raise ValueError('--limit must be positive')
                chosen = select(entries,query=args.query,include_quarantined=args.include_quarantined,**filters)
                if args.json:
                    print(json.dumps({'total':len(chosen),'entries':chosen[:args.limit]},ensure_ascii=False,indent=2))
                else:
                    for e in chosen[:args.limit]:
                        print(f"{e['forms']['zh_Hans']} / {e['forms']['zh_Hant']}\n  {e['forms']['en']}\n  来源地区 {e['source_origin']}；法域 {','.join(e['jurisdictions']) or '待核查'}；领域 {','.join(e['domains'])}\n  {e['id']}；{e['review']['translation']}")
                    print(f'{len(chosen)} matches; showing {min(len(chosen),args.limit)}')
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f'ERROR: {error}',file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
