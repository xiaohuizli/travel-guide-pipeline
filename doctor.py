#!/usr/bin/env python3
"""Static readiness only. Never reads credential values into output."""
import argparse, json, os, shutil, subprocess
from pathlib import Path

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--skills-dir', type=Path, default=Path(os.environ.get('CODEX_HOME', str(Path.home()/'.codex')))/'skills')
    args=parser.parse_args()
    config=json.loads((Path(__file__).resolve().parent/'pipeline.json').read_text())
    skills={d['name']:(args.skills_dir/d['name']/'SKILL.md').is_file() for d in config['dependencies']}
    keychain = False
    if shutil.which('security'):
        keychain = subprocess.run(['security','find-generic-password','-s','travel-guide-pipeline.tripai','-a','TRIPAI_API_KEY'],capture_output=True).returncode == 0
    result={'tripai_keychain_item_present':keychain,'skills':skills,'python':True,'node':bool(shutil.which('node')),'playwright_skill':(args.skills_dir/'playwright'/'SKILL.md').is_file(),'tc_chengxin_cli':bool(shutil.which('tc-chengxin') or (Path.home()/'.workbuddy/binaries/node/cli-connector-packages/bin/tc-chengxin').is_file()),'credentials_present':{k:bool(os.environ.get(k)) for k in config['collection']['optional_api_env']},'browser_access':'requires_live_check','api_access':'not_tested','html_rendering':'requires_live_check'}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    # Dependencies are optional adapters; a missing one does not block the core workflow.
    return 0

if __name__=='__main__':
    raise SystemExit(main())
