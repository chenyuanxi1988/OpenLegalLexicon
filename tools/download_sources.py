"""Fetch known, public sources into a new/cache directory (HTTPS only)."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import json
from pathlib import Path
import shutil
import subprocess
import time

from openlegallexicon.io import digest, read_json, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path.cwd())
    parser.add_argument('--cache',type=Path,required=True)
    args = parser.parse_args()
    sources = read_json(args.root/'data/sources.json')
    judicial = next(s for s in sources if s['id']=='tw-judicial')
    curl = shutil.which('curl')
    if not curl:
        raise SystemExit('curl is required with HTTPS certificate validation')
    targets = [(f'judicial-{i}.html',f'https://www.judicial.gov.tw/tw/lp-1501-1-{i}-60.html') for i in range(1,judicial['pages']+1)]
    targets.append(('tipo-trademark.csv','https://tiponet.tipo.gov.tw/datagov/tm/004-102-001.csv'))
    args.cache.mkdir(parents=True,exist_ok=True)
    manifest_path=args.cache/'downloads.json'
    previous={r['path']:r for r in read_json(manifest_path)} if manifest_path.exists() else {}
    def fetch(item):
        name,url=item
        path=args.cache/name
        if path.exists():
            if name not in previous or digest(path)!=previous[name]['sha256']:
                raise ValueError(f'{name}: cached file lacks a matching retrieval manifest; use a fresh cache directory')
            return previous[name]
        temporary=path.with_suffix(path.suffix+'.part')
        subprocess.run([curl,'--fail','--location','--proto','=https','--proto-redir','=https','--max-time','45','--retry','2','--silent','--show-error','--output',str(temporary),url],check=True)
        temporary.replace(path)
        result={'path':name,'url':url,'sha256':digest(path),'bytes':path.stat().st_size,'retrieved':date.today().isoformat()}
        time.sleep(0.4)
        return result
    # Save each successful result so interruption does not lose retrieval evidence.
    with ThreadPoolExecutor(max_workers=2) as pool:
        for row in pool.map(fetch,targets):
            previous[row['path']]=row
            write_json(manifest_path,list(previous.values()))
            print(row['path'],row['bytes'],flush=True)
    print('Review source licenses, then run oll import-snapshot --cache <directory>.')


if __name__=='__main__':main()
