; Настройка общего инсталлятора
[Setup]
AppName=ChildPCGuard
AppVersion=1.0
DefaultDirName={pf}\ChildPCGuard
DefaultGroupName=ChildPCGuard
AllowNoIcons=True
OutputDir=Output
OutputBaseFilename=ChildPCGuardInstaller
PrivilegesRequired=admin

[Files]
; Основное приложение "ChildPCGuard" для администратора
Source: "C:\Path\To\MainApp.exe"; DestDir: "{app}"; Flags: ignoreversion

; Приложение "Индикатор таймера" для простого пользователя
Source: "C:\Path\To\TimerIndicator.exe"; DestDir: "C:\Users\{code:GetSimpleUserName}\AppData\Local\TimerIndicator"; Flags: ignoreversion

[Icons]
; Ярлык для приложения "Блокировка по времени" в меню "Пуск" администратора
Name: "{group}\ChildPCGuard"; Filename: "{app}\MainApp.exe"

; Ярлык для автозагрузки приложения "Индикатор таймера" для простого пользователя
Name: "C:\Users\{code:GetSimpleUserName}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\TimerIndicator"; Filename: "C:\Users\{code:GetSimpleUserName}\AppData\Local\TimerIndicator\TimerIndicator.exe"; Tasks: addstartup

[Run]
; Запускаем основное приложение после установки (опционально)
Filename: "{app}\MainApp.exe"; Flags: nowait postinstall skipifsilent

; Добавляем логин для простого пользователя
Filename: "cmd"; Parameters: "/C net user SimpleUser Password123! /add"
Filename: "cmd"; Parameters: "/C net localgroup Users SimpleUser /add"

[Code]
; Функция для получения имени пользователя SimpleUser
function GetSimpleUserName(Value: string): string;
begin
  Result := 'SimpleUser';
end;
