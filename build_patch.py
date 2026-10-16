"""Build ECWolf v4 from an existing ModernCombat PK3 (Python 3 stdlib)."""
from pathlib import Path
import re
import sys
import zipfile


def build(source, output):
    if Path(source).resolve() == Path(output).resolve():
        raise ValueError('Input and output must differ')
    with zipfile.ZipFile(source) as src:
        entries = {n: src.read(n) for n in src.namelist()}
    for old, new in [('DECORATE','decorate.txt'),('MAPINFO','mapinfo.txt'),('SNDINFO','sndinfo.txt')]:
        if old in entries:
            if new in entries:
                raise ValueError('Ambiguous script: ' + new)
            entries[new] = entries.pop(old)
    text = entries['decorate.txt'].decode('utf-8')
    for ammo in ['PistolAmmo', 'MachineGunAmmo']:
        pattern = r'(actor\s+' + ammo + r'\s*:\s*Ammo\s*\{)[^}]*}'
        body = r'\1\n    inventory.maxamount 400\n    ammo.backpackmaxamount 400\n}'
        text, count = re.subn(pattern, body, text)
        if count != 1:
            raise ValueError('Expected exactly one ' + ammo)
    pattern = r'(actor ECWolfBlueGuard : Schutzstafell replaces Schutzstafell\s*\{)[^}]*}'
    text, count = re.subn(pattern, r'\1\n    dropitem "ECWolfMachineGun"\n}', text)
    if count != 1:
        raise ValueError('Expected exactly one SS override')
    # The explicit MAPINFO player class starts clean, without BJPlayer's legacy Clip.
    text = re.sub(r'actor ECWolfArmoredBJ\s*:\s*BJPlayer(?:\s+replaces\s+BJPlayer)?',
                  'actor ECWolfArmoredBJ : PlayerPawn', text)
    if 'replaces ClipBox2' not in text:
        text += '''\nactor ECWolfMachineAmmoBox2 : MachineGunAmmo replaces ClipBox2
{
    inventory.amount 80
    inventory.maxamount 400
    inventory.pickupsound "misc/ammobox_pkup"
    states
    {
        Spawn:
            AMO2 A -1
            stop
    }
}
'''
    entries['decorate.txt'] = text.encode('utf-8')
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as dst:
        for name, data in entries.items():
            dst.writestr(name, data)
    return text

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: python build_patch.py INPUT.pk3 OUTPUT.pk3')
    build(*sys.argv[1:])
