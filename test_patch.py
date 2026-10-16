import unittest,zipfile,re,sys
from pathlib import Path
PACKAGE=Path(sys.argv.pop(1)) if len(sys.argv)>1 else Path(__file__).with_name('ECWolf_ModernCombat.pk3')
class CombatContract(unittest.TestCase):
 def setUp(self):
  with zipfile.ZipFile(PACKAGE) as z:
   self.names=z.namelist(); self.text=z.read('decorate.txt' if 'decorate.txt' in self.names else 'DECORATE').decode(); self.map=z.read('mapinfo.txt' if 'mapinfo.txt' in self.names else 'MAPINFO').decode()
 def actor(self,name):
  m=re.search(r'actor\s+'+name+r'\b[^\{]*\{',self.text,re.I);self.assertIsNotNone(m,name)
  pos=m.end(); depth=1
  for end in range(pos,len(self.text)):
   depth+=(self.text[end]=='{')-(self.text[end]=='}')
   if not depth:return self.text[pos:end]
 def test_engine_script_names(self):
  for name in ['decorate.txt','mapinfo.txt','sndinfo.txt']:self.assertIn(name,self.names)
 def test_separate_root_ammo_classes(self):
  for name in ['PistolAmmo','MachineGunAmmo']:self.assertRegex(self.text,r'actor '+name+r'\s*:\s*Ammo\b')
 def test_capacity_before_and_after_backpack(self):
  for name in ['PistolAmmo','MachineGunAmmo']:
   for prop in ['inventory.maxamount','ammo.backpackmaxamount']:self.assertIn(prop+' 400',self.actor(name))
 def test_weapon_ammo_assignments(self):
  for name,ammo in [('ECWolfPistol','PistolAmmo'),('ECWolfBluePistol','PistolAmmo'),('ECWolfMachineGun','MachineGunAmmo'),('ECWolfBlueAK47','MachineGunAmmo'),('ECWolfMinigun','MachineGunAmmo'),('ECWolfBlueMinigun','MachineGunAmmo')]:self.assertIn('weapon.ammotype1 "'+ammo+'"',self.actor(name))
 def test_ss_drops_weapon(self):self.assertEqual(re.findall(r'dropitem\s+"([^"]+)"',self.actor('ECWolfBlueGuard')),['ECWolfMachineGun'])
 def test_alternate_box_is_automatic_weapon_ammo(self):self.assertRegex(self.text,r'actor ECWolfMachineAmmoBox2\s*:\s*MachineGunAmmo replaces ClipBox2')
 def test_selected_player_has_no_legacy_clip_start(self):
  self.assertIn('playerclasses = "ECWolfArmoredBJ"',self.map)
  self.assertRegex(self.text,r'actor ECWolfArmoredBJ\s*:\s*PlayerPawn\b')
  self.assertNotIn('"Clip"',self.actor('ECWolfArmoredBJ'))
 def test_archive_integrity(self):
  with zipfile.ZipFile(PACKAGE) as z:self.assertIsNone(z.testzip())
if __name__=='__main__':unittest.main()
