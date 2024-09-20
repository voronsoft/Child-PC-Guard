; Имя файла: setup.iss
; Версия: Inno Setup 6.2.2 или новее
; Скрипт для установки программ Child PC Guard, Child PC Timer и Child PC Monitor

[Setup]
; Основная информация об установке
AppName=Child PC Guard Suite
AppVersion=1.0
DefaultDirName={pf}\ChildPCGuard
DefaultGroupName=Child PC Guard
OutputBaseFilename=ChildPCGuard_Installer
Compression=lzma2
SolidCompression=yes
; Требует прав администратора для записи в системные папки
PrivilegesRequired=admin
; Отключение создания стандартного деинсталлятора
Uninstallable=no

[Files]
; Основные исполняемые файлы
Source: "dist\Child PC Guard.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Child PC Timer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Windows CPG Monitor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Uninstall Child PC Guard.exe"; DestDir: "{app}"; Flags: ignoreversion

; Иконка приложения устанавливается в папку с программами
Source: "dist\icon.ico"; DestDir: "{app}"; Flags: ignoreversion

; Файл данных и файл для логов устанавливаются в папку ProgramData (общую для всех пользователей)
Source: "dist\data.json"; DestDir: "{commonappdata}\ChildPCGuard"; Flags: ignoreversion
Source: "dist\log_chpcgu.txt"; DestDir: "{commonappdata}\ChildPCGuard"; Flags: ignoreversion

[Icons]
; Создание ярлыков для всех приложений в меню "Пуск"
Name: "{group}\Child PC Guard"; Filename: "{app}\Child PC Guard.exe"; WorkingDir: "{app}"
Name: "{group}\Child PC Timer"; Filename: "{app}\Child PC Timer.exe"; WorkingDir: "{app}"
Name: "{group}\Child PC Monitor"; Filename: "{app}\Windows CPG Monitor.exe"; WorkingDir: "{app}"
Name: "{group}\Uninstall Child PC Guard"; Filename: "{app}\Uninstall Child PC Guard.exe"; WorkingDir: "{app}"
Name: "{group}\Logs Child PC Guard"; Filename: "notepad.exe"; Parameters: """{commonappdata}\ChildPCGuard\log_chpcgu.txt"""; WorkingDir: "{commonappdata}\ChildPCGuard"; IconFilename: "{app}\icon.ico"

; Создание ярлыков для всех приложений на рабочем столе
Name: "{commondesktop}\Child PC Guard"; Filename: "{app}\Child PC Guard.exe"; WorkingDir: "{app}"
Name: "{commondesktop}\Child PC Timer"; Filename: "{app}\Child PC Timer.exe"; WorkingDir: "{app}"
Name: "{commondesktop}\Child PC Monitor"; Filename: "{app}\Windows CPG Monitor.exe"; WorkingDir: "{app}"
; Name: "{commondesktop}\Uninstall Child PC Guard"; Filename: "{app}\Uninstall Child PC Guard.exe"; WorkingDir: "{app}"
Name: "{commondesktop}\Logs Child PC Guard"; Filename: "notepad.exe"; Parameters: """{commonappdata}\ChildPCGuard\log_chpcgu.txt"""; WorkingDir: "{commonappdata}\ChildPCGuard"; IconFilename: "{app}\icon.ico"

; Создание ярлыка для автозагрузки Windows CPG Monitor.exe
Name: "{userstartup}\Child PC Monitor"; Filename: "{app}\Windows CPG Monitor.exe"; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"; Flags: runasadmin

[Run]
; Автоматический запуск Child PC Monitor после установки с правами администратора
Filename: "{app}\Windows CPG Monitor.exe"; Description: "Запуск Child PC Monitor"; Flags: nowait postinstall skipifsilent runasadmin

; Код для создания пункта с флажком запустить ли приложение после установки или нет
[Code]
var
  LaunchAfterInstall: Boolean;

function InitializeSetup(): Boolean;
begin
  LaunchAfterInstall := False;  // Изначально выключено
  Result := True; // Продолжаем установку
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  // Добавляем возможность выбора запуска программы после установки
  if CurStep = ssPostInstall then
  begin
    // Вопрос пользователю о запуске программы
    LaunchAfterInstall := MsgBox('Запустить Child PC Guard после установки?', mbConfirmation, MB_YESNO) = IDYES;
  end;
end;

function ShouldLaunchAfterInstall: Boolean;
begin
  Result := LaunchAfterInstall;
end;