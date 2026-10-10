@echo off
title Update OSRS Alch Bridge Plugin
echo =======================================================
echo   Updating AlchBridgePlugin.jar for Microbot / RuneLite
echo =======================================================
echo.

:copy_loop
copy /Y "%~dp0bridge_plugin\AlchBridgePlugin.jar" "%USERPROFILE%\.runelite\microbot-plugins\AlchBridgePlugin.jar" >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] AlchBridgePlugin.jar successfully updated!
    echo.
    echo The new in-game Alchs/hr and Profit/hr overlay is installed.
    echo You can now launch Microbot!
    echo.
    pause
    exit /b 0
)

echo [NOTICE] Microbot is currently running and holding the plugin file.
echo Please close or restart Microbot, then press any key to finish the update...
pause >nul
goto copy_loop
