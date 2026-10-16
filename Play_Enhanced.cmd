@echo off
setlocal
cd /d "%~dp0"
if not exist "ecwolf.exe" (
 echo Extract this package into your ECWolf folder beside ecwolf.exe.
 pause
 exit /b 1
)
if not exist "ECWolf_HD.pk3" (
 echo Missing ECWolf_HD.pk3. Keep your existing HD pack in this folder.
 pause
 exit /b 1
)
set "GAMEBASE=D:\steam\steamapps\common\Wolfenstein 3D\base"
if not exist "%GAMEBASE%\VSWAP.WL6" (
 set /p "GAMEBASE=Enter the folder containing your Wolfenstein 3D WL6 files: "
)
if not exist "%GAMEBASE%\VSWAP.WL6" (
 echo Wolfenstein 3D game data not found.
 pause
 exit /b 1
)
set "MODS="
for %%F in (ECWolf_RMST.pk3 ECWolf_RMST_SFX.pk3 ECWolf_RMST_CoffeFix.pk3 ECWolf_400Ammo.pk3 ECWolf_HD.pk3 ECWolf_HDFace.pk3 ECWolf_ModernAudio.pk3 ECWolf_PaintingsAI.pk3 ECWolf_ModernMenu.pk3 ECWolf_WolfIntroAI.pk3) do call :addmod "%%F"
set MODS=%MODS% --file "%~dp0ECWolf_ModernCombat_SSWeapon.pk3"
echo Starting at 1920x1080. Close the game normally when finished.
cd /d "%GAMEBASE%"
"%~dp0ecwolf.exe" --data WL6 --res 1920 1080 --fullscreen %MODS% > "%~dp0ECWolf-test.log" 2>&1
set "RESULT=%ERRORLEVEL%"
echo ECWolf exit code: %RESULT%
echo Startup output is in ECWolf-test.log. This alone does not verify gameplay.
pause
exit /b %RESULT%
:addmod
if exist "%~1" set MODS=%MODS% --file "%~dp0%~1"
exit /b
