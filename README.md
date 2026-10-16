ECWolf ammo and SS weapon fix v4

INSTALL
1. Close ECWolf. Back up the current ECWolf_ModernCombat.pk3.
2. Extract this ZIP into C:\Users\andre\AppData\Local\Programs\ECWolf.
3. Replace ECWolf_ModernCombat.pk3 when prompted.
4. Run Play_Ammo_Fixed.cmd. Do not use a previous test launcher.
5. Start a NEW GAME. Old saves retain old inventory and ammo classes.

BEHAVIOR CONFIGURED
- Pistol ammo is separate from machine-gun/minigun ammo.
- Each ammo pool has capacity 400, including backpack capacity.
- Machine gun and minigun intentionally share their automatic-weapon pool.
- SS guards explicitly drop ECWolfMachineGun (weapon pickup), not pistol ammo.
- Brown guards continue to drop pistol clips.
- Both automatic-weapon ammo-box variants use MachineGunAmmo.
- Pistol begins with 8 rounds. Capacity 400 does not mean 400 starting rounds.

The launcher omits ECWolf_400Ammo, old SS drop fixes, Combat_Compatible,
ModernCombat_AmmoFix and ModernCombat_SSWeapon. Do not manually add them.
It preserves installed graphics packs and loads corrected ModernCombat last.
The existing HD graphics are retained; no new artwork is included.

WHY
The previous build retained extensionless root scripts. This build uses
ECWolf PK3 script filenames decorate.txt, mapinfo.txt and sndinfo.txt.
The explicit player class uses PlayerPawn to avoid inherited legacy Clip items.
Both ammo roots specify inventory and backpack limits of 400.

VALIDATION
8 package contract tests pass; the old patch fails 3 of those tests.
These inspect scripts/archive structure. They do not run the ECWolf engine.
Full gameplay is NOT verified: no compatible runtime or WL6 game data here.
If startup fails, send ECWolf-ammo-test.log.
In a new game, collect ammo above 99, switch pistol/machine gun to compare counts,
fire the pistol and verify machine ammo stays unchanged, then kill an SS guard
and collect its machine gun. Test again when already carrying a machine gun.
