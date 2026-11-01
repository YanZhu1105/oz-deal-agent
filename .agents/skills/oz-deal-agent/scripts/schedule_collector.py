#!/usr/bin/env python3
"""Install the optional per-user 15-minute RSS collector with macOS launchd."""
import argparse
import hashlib
import json
import os
import plistlib
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().with_name('agent.py')
DATA = Path(os.environ.get('OZ_DEAL_DATA', str(Path.home()/'.local/share/oz-deal-agent'))).expanduser().resolve()
LABEL = 'com.ozdealagent.collector.' + hashlib.sha256(str(DATA).encode()).hexdigest()[:12]
PLIST = Path.home()/'Library'/'LaunchAgents'/(LABEL+'.plist')


def service_config(python=sys.executable):
    return {'Label':LABEL, 'ProgramArguments':[str(Path(python).resolve()),str(DATA/'collector'/'agent.py'),'collect'],
            'EnvironmentVariables':{'OZ_DEAL_DATA':str(DATA)}, 'StartInterval':900,
            'RunAtLoad':True, 'StandardOutPath':str(DATA/'collector.log'),
            'StandardErrorPath':str(DATA/'collector-error.log')}


def install():
    if sys.platform != 'darwin': raise RuntimeError('Automatic collector installation currently supports macOS only')
    if not SCRIPT.is_file(): raise RuntimeError('Collector script not found')
    DATA.mkdir(parents=True,exist_ok=True); PLIST.parent.mkdir(parents=True,exist_ok=True)
    collector_dir=DATA/'collector'; collector_dir.mkdir(parents=True,exist_ok=True)
    staged=collector_dir/'agent.py.tmp'
    shutil.copyfile(SCRIPT,staged); os.replace(staged,collector_dir/'agent.py')
    config=service_config()
    if PLIST.exists():
        with PLIST.open('rb') as f: existing=plistlib.load(f)
        if existing != config: raise RuntimeError('A different collector configuration already exists; inspect it before changing it: '+str(PLIST))
    else:
        # Exclusive creation prevents overwriting another job in a race.
        with PLIST.open('xb') as f: plistlib.dump(config,f)
    domain='gui/'+str(os.getuid()); target=domain+'/'+LABEL
    check=subprocess.run(['launchctl','print',target],capture_output=True,text=True)
    if check.returncode:
        result=subprocess.run(['launchctl','bootstrap',domain,str(PLIST)],capture_output=True,text=True)
        if result.returncode: raise RuntimeError('launchctl bootstrap failed: '+result.stderr.strip())
    check=subprocess.run(['launchctl','print',target],capture_output=True,text=True)
    if check.returncode: raise RuntimeError('Collector could not be verified as loaded: '+check.stderr.strip())
    return {'installed':True,'label':LABEL,'interval_minutes':15,'state_directory':str(DATA),'plist':str(PLIST),'note':'Loaded service; this does not prove a successful RSS fetch. Inspect status or collector logs.'}


def status():
    if sys.platform != 'darwin': raise RuntimeError('The collector manager currently supports macOS only')
    target='gui/'+str(os.getuid())+'/'+LABEL
    result=subprocess.run(['launchctl','print',target],capture_output=True,text=True)
    return {'installed':PLIST.exists(),'loaded':result.returncode==0,'label':LABEL,'state_directory':str(DATA),'note':'Loaded does not mean the latest RSS fetch succeeded. Check agent status and collector logs.'}

def uninstall():
    if sys.platform != 'darwin': raise RuntimeError('The collector manager currently supports macOS only')
    if not PLIST.exists(): return {'removed':False,'reason':'not installed'}
    with PLIST.open('rb') as f: config=plistlib.load(f)
    args=config.get('ProgramArguments',[])
    if config.get('Label') != LABEL or len(args)!=3 or args[1:]!=[str(DATA/'collector'/'agent.py'),'collect'] or config.get('EnvironmentVariables',{}).get('OZ_DEAL_DATA')!=str(DATA):
        raise RuntimeError('Collector job does not match this installation; refusing to remove it')
    domain='gui/'+str(os.getuid());target=domain+'/'+LABEL
    if subprocess.run(['launchctl','print',target],capture_output=True).returncode==0:
        r=subprocess.run(['launchctl','bootout',domain,str(PLIST)],capture_output=True,text=True)
        if r.returncode: raise RuntimeError('launchctl bootout failed: '+r.stderr.strip())
    PLIST.unlink()
    return {'removed':True,'note':'Preferences, deal history and local collector files were preserved.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['install','status','uninstall']);args=p.parse_args()
    try: print(json.dumps({'install':install,'status':status,'uninstall':uninstall}[args.action](),ensure_ascii=False,indent=2))
    except Exception as e: print(json.dumps({'error':str(e)},ensure_ascii=False),file=sys.stderr);sys.exit(1)
if __name__=='__main__':main()
