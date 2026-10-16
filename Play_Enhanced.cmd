@echo off
setlocal
cd /d "%~dp0"
if not exist "ecwolf.exe" goto missingengine
if not exist "ECWolf_ModernCombat.pk3" goto missingpatch
set "GAMEBASE=D:\steam\steamapps\common\Wolfenstein 3D\base"
if not exist "%GAMEBASE%\VSWAP.WL6" set /p "GAMEBASE=Enter the folder containing VSWAP.WL6: "
if not exist "%GAMEBASE%\VSWAP.WL6" goto missingdata
set "MODS="
for %%F in (ECWolf_RMST.pk3 ECWolf_RMST_SFX.pk3 ECWolf_RMST_CoffeFix.pk3 ECWolf_HD.pk3 ECWolf_HDFace.pk3 ECWolf_ModernAudio.pk3 ECWolf_PaintingsAI.pk3 ECWolf_ModernMenu.pk3 ECWolf_WolfIntroAI.pk3 ECWolf_Environment_Enhanced.pk3) do call :addmod "%%F"
set MODS=%MODS% "%~dp0ECWolf_ModernCombat.pk3"
cd /d "%GAMEBASE%"
"%~dp0ecwolf.exe" --data WL6 --res 1920 1080 --fullscreen --file %MODS% > "%~dp0ECWolf-ammo-test.log" 2>&1
set "RESULT=%ERRORLEVEL%"
echo ECWolf exit code: %RESULT%. See ECWolf-ammo-test.log.
pause
exit /b %RESULT%
:addmod
if exist "%~1" set MODS=%MODS% "%~dp0%~1"
exit /b
:missingengine
echo Extract this ZIP into your ECWolf folder beside ecwolf.exe.
pause
exit /b 1
:missingpatch
echo Missing ECWolf_ModernCombat.pk3 from this package.
pause
exit /b 1
:missingdata
echo Wolfenstein WL6 data folder not found.
pause
exit /b 1
