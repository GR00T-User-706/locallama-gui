#ifndef MyLoAIVersion
  #define MyLoAIVersion "1.2.0"
#endif
#define MyLoAIName "MyLoAI Control Center"
#define MyLoAIPublisher "MyLoAI"
#define MyLoAIExe "MyLoAI Control Center.exe"

[Setup]
AppId={{D6A6A1C1-0C0B-4E4C-9B44-7A4D1E2A3F90}
AppName={#MyLoAIName}
AppVersion={#MyLoAIVersion}
AppPublisher={#MyLoAIPublisher}
DefaultDirName={localappdata}\Programs\MyLoAI Control Center
DefaultGroupName={#MyLoAIName}
DisableProgramGroupPage=yes
OutputDir=..\..\dist\installer
OutputBaseFilename=MyLoAI-Control-Center-{#MyLoAIVersion}-Windows-x64
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#MyLoAIExe}
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "..\..\dist\MyLoAI Control Center\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\USER_MANUAL.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "..\..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyLoAIName}"; Filename: "{app}\{#MyLoAIExe}"
Name: "{autodesktop}\{#MyLoAIName}"; Filename: "{app}\{#MyLoAIExe}"; Tasks: desktopicon
Name: "{autoprograms}\{#MyLoAIName} User Manual"; Filename: "{app}\docs\USER_MANUAL.md"

[Run]
Filename: "{app}\{#MyLoAIExe}"; Description: "Launch {#MyLoAIName}"; Flags: nowait postinstall skipifsilent
