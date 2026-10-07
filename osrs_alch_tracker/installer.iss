; Inno Setup Script for OSRS High Alchemy & Crafting Profit Dashboard
; Download Inno Setup from: https://jrsoftware.org/isdl.php

#define MyAppName "OSRS High Alchemy & Crafting Tracker"
#define MyAppVersion "1.3.1"
#define MyAppPublisher "jef11222"
#define MyAppURL "https://github.com/jef11222/osrs-alch-tracker"
#define MyAppExeName "OSRS_Alch_Tracker.exe"

[Setup]
; App Metadata
AppId={{9FA16BAF-A2EA-4125-83A8-B6E8D1B33BF9}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}/releases

; Default Installation Directory: %LocalAppData%\Programs\... (No Admin Rights Required)
DefaultDirName={localappdata}\Programs\OSRS Alch Tracker
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output Settings
OutputDir=dist
OutputBaseFilename=OSRS_Alch_Tracker_Setup
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

; Windows Settings
PrivilegesRequired=lowest
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: isreadme
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
