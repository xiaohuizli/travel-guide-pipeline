#!/usr/bin/env python3
"""Query only; loads credential from environment or an explicitly configured Keychain item."""
import argparse,json,os,shutil,subprocess,sys,urllib.request,urllib.error
SERVICE='travel-guide-pipeline.tripai'
ACCOUNT='TRIPAI_API_KEY'
def credential():
    token=os.environ.get(ACCOUNT,'').strip()
    if token:return token
    if not shutil.which('security'):
        return ''
    result=subprocess.run(['security','find-generic-password','-s',SERVICE,'-a',ACCOUNT,'-w'],capture_output=True,text=True)
    return result.stdout.strip() if result.returncode==0 else ''
def main():
    ap=argparse.ArgumentParser();ap.add_argument('query');args=ap.parse_args()
    token=credential()
    if not token:
        print('未配置携程凭据。',file=sys.stderr);return 2
    data=json.dumps({'token':token,'query':args.query,'source':'github'}).encode()
    req=urllib.request.Request('https://wendao-skill-prod.ctrip.com/skill/query',data=data,headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=60) as res:
            body=res.read(2000000).decode('utf-8','replace')
            print(body.replace(token,'[REDACTED]'))
    except urllib.error.HTTPError as e:
        print('携程接口 HTTP '+str(e.code),file=sys.stderr);return 3
    except (urllib.error.URLError,TimeoutError):
        print('携程接口连接失败或超时。',file=sys.stderr);return 4
    return 0
if __name__=='__main__':sys.exit(main())
