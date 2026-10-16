"""Build against Andre's existing ECWolf_ModernCombat.pk3; Python 3 stdlib only."""
from pathlib import Path
import re
import zipfile
import sys

def build(source, output):
    with zipfile.ZipFile(source) as src:
        text = src.read('DECORATE').decode('utf-8')
        pattern = r'(actor ECWolfBlueGuard : Schutzstafell replaces Schutzstafell\s*\{\s*)dropitem "[^"]+"'
        fixed, count = re.subn(pattern, r'\1dropitem "ECWolfMachineGun"', text)
        if count != 1:
            raise ValueError('Expected exactly one ECWolfBlueGuard definition; no output written')
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as dst:
            for item in src.infolist():
                dst.writestr(item, fixed.encode('utf-8') if item.filename == 'DECORATE' else src.read(item.filename))
    return fixed

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: python build_patch.py INPUT.pk3 OUTPUT.pk3')
    build(*sys.argv[1:])
