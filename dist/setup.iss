; Имя файла: setup.iss
; Версия: Inno Setup 6.2.2 или новее
; Скрипт для установки программ Child PC Guard, Child PC Timer и Child PC Monitor

[Setup]
; Основная информация об установке
AppName=Child PC Guard Suite
AppVersion=1.0
; Устанавливает приложение в папку C:\Program Files (x86)\ChildPCGuard
DefaultDirName={commonpf32}\ChildPCGuard
; Название папки программы в Пуск
DefaultGroupName=Child PC Guard
; Название установщика
OutputBaseFilename=Child PC Guard Installer {AppVersion}
;
Compression=lzma2
SolidCompression=yes
; Требует прав администратора для записи в системные папки
;PrivilegesRequired=lowest
; Отключение создания стандартного деинсталлятора
Uninstallable=no
; Отключить страницу выбора каталога
DisableDirPage=yes
; Отключить страницу выбора группы программ
DisableProgramGroupPage=yes

[Files]
; Основные исполняемые файлы
Source: "Child PC Guard.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Child PC Timer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Windows CPG Monitor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Uninstall Child PC Guard.exe"; DestDir: "{app}"; Flags: ignoreversion
; Иконка перемещена по пути 'img\icon.ico'
Source: "img\icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Создание ярлыков в меню "Пуск" в общей папке для всех пользователей - (C:\ProgramData\Microsoft\Windows\Start Menu\Programs\)
Name: "{commonstartmenu}\Programs\Child PC Guard"; Filename: "{app}\Child PC Guard.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\icon.ico"
Name: "{commonstartmenu}\Programs\Child PC Timer"; Filename: "{app}\Child PC Timer.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\timer.ico"
Name: "{commonstartmenu}\Programs\Child PC Monitor"; Filename: "{app}\Windows CPG Monitor.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\monitor.ico"
Name: "{commonstartmenu}\Programs\Uninstall Child PC Guard"; Filename: "{app}\Uninstall Child PC Guard.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\uninstall.ico"
Name: "{commonstartmenu}\Programs\Logs Child PC Guard"; Filename: "notepad.exe"; Parameters: """{commonappdata}\Child PC Guard Data\log_chpcgu.txt"""; WorkingDir: "{commonappdata}\ChildPCGuard"; IconFilename: "{app}\img\logs.ico"

; Создание ярлыков для всех приложений на "Рабочем столе" для всех пользователей - (C:\Users\Public\Desktop)
Name: "{commondesktop}\Child PC Guard"; Filename: "{app}\Child PC Guard.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\icon.ico"
Name: "{commondesktop}\Child PC Timer"; Filename: "{app}\Child PC Timer.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\timer.ico"
Name: "{commondesktop}\Child PC Monitor"; Filename: "{app}\Windows CPG Monitor.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\monitor.ico"
Name: "{commondesktop}\Logs Child PC Guard"; Filename: "notepad.exe"; Parameters: """{commonappdata}\Child PC Guard Data\log_chpcgu.txt"""; WorkingDir: "{commonappdata}\ChildPCGuard"; IconFilename: "{app}\img\logs.ico"

; Создание ярлыка в папке автозагрузки пользователя который устанавливает программу
Name: "{userstartup}\Child PC Monitor"; Filename: "{app}\Windows CPG Monitor.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\icon.ico"

[Run]
; Автоматический запуск Child PC Monitor после установки с правами администратора
Filename: "{app}\Windows CPG Monitor.exe"; Description: "Запуск Child PC Monitor"; Flags: nowait postinstall skipifsilent

; Код для создания пункта с флажком запустить ли приложение после установки или нет
[Code]
var
  LaunchAfterInstall: Boolean;

// Функция для проверки прав администратора
function CheckAdminRights(): Boolean;
begin
  Result := IsAdmin(); // Возвращает True, если запущено с правами администратора
end;

// Функция для вывода сообщения и завершения установки
function ShowAdminErrorAndExit(): Boolean;
begin
  MsgBox('Пожалуйста, запустите установщик от имени администратора для корректной установки.', mbError, MB_OK);
  Result := False; // Прекращаем установку
end;

// Функция инициализации установки
function InitializeSetup(): Boolean;
begin
  LaunchAfterInstall := False; // Изначально выключено

  // Проверяем права администратора
  if not CheckAdminRights() then
  begin
    Result := ShowAdminErrorAndExit(); // Прекращаем установку
    Exit; // Выходим из функции
  end;

  Result := True; // Продолжаем установку
end;

// Процедура для обработки текущего шага установки
procedure CurStepChanged(CurStep: TSetupStep);
begin
  // Добавляем возможность выбора запуска программы после установки
  if CurStep = ssPostInstall then
  begin
    // Вопрос пользователю о запуске программы
    LaunchAfterInstall := MsgBox('Запустить Child PC Monitor после установки?', mbConfirmation, MB_YESNO) = IDYES;
  end;
end;

// Функция для определения, нужно ли запускать приложение после установки
function ShouldLaunchAfterInstall: Boolean;
begin
  Result := LaunchAfterInstall;
end;

// Процедура запуска приложения после установки
procedure LaunchApplicationAfterInstall();
begin
  if ShouldLaunchAfterInstall then
  begin
    Exec(ExpandConstant('{app}\Child PC Monitor.exe'), '', '', SW_SHOWNORMAL, ewNoWait, ResultCode);
  end;
end;
