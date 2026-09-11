"""Compile and query real librime in a disposable test profile."""
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

from openlegallexicon.io import write_json


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--bundle',type=Path,required=True)
    parser.add_argument('--deployer',default='rime_deployer')
    parser.add_argument('--include',type=Path,default=Path('/usr/include'))
    parser.add_argument('--library',default='rime')
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    source=Path(__file__).resolve().parents[1]/'tests/rime_smoke.c'
    with tempfile.TemporaryDirectory(prefix='oll-rime-') as tmp:
        root=Path(tmp)
        for name in ['user','shared','build','logs']:(root/name).mkdir()
        for p in args.bundle.glob('*.yaml'):shutil.copyfile(p,root/'user'/p.name)
        (root/'user/default.yaml').write_text('config_version: "1.0"\nschema_list:\n  - schema: openlegal_hans\n  - schema: openlegal_hant\n')
        dirs=[str(root/name) for name in ['user','shared','build']]
        subprocess.run([args.deployer,'--build',*dirs],check=True,capture_output=True,text=True)
        for suffix in ['hans','hant']:
            for extension in ['table.bin','prism.bin']:
                if not (root/'build'/f'openlegal_{suffix}.{extension}').is_file():
                    raise ValueError('Rime failed to generate compiled dictionary files')
        compiler=shutil.which('cc') or shutil.which('clang')
        if not compiler:raise ValueError('C compiler is required')
        library=Path(args.library)
        link=[str(library),f'-Wl,-rpath,{library.parent}'] if library.is_file() else ['-l'+args.library]
        subprocess.run([compiler,'-I',str(args.include),str(source),*link,'-o',str(root/'smoke')],check=True,capture_output=True,text=True)
        checks=[('hans','xingzhengchufen','行政处分'),('hant','xingzhengchufen','行政處分'),('hans','lvshi','律师'),('hant','lvshi','律師'),('hans',"yin'hang'fa",'银行法'),('hans',"kuai'ji'fa",'会计法'),('hans','chongfuchufa','重复处罚')]
        results=[]
        for suffix,keys,expected in checks:
            result=subprocess.run([str(root/'smoke'),*dirs,str(root/'logs'),'openlegal_'+suffix,keys,expected],capture_output=True,text=True)
            if result.returncode:
                raise ValueError(f'{keys} -> {expected}: {result.stdout}\n{result.stderr}')
            results.append({'schema':'openlegal_'+suffix,'keys':keys,'expected':expected,'output':result.stdout.strip(),'passed':True})
        report={'engine':'librime','isolated_profile':True,'tests':results}
        if args.out:write_json(args.out,report)
        print(f'PASS: compiled 2 dictionaries and verified {len(checks)} live candidate queries')


if __name__=='__main__':main()
