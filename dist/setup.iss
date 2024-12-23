; Имя файла: setup.iss
; Версия: Inno Setup 6.2.2 или новее
; Скрипт для установки программ Child PC Guard, Child PC Timer и Child PC Monitor

[Setup]
; Основная информация об установке
AppName=Child PC Guard Suite
AppVersion=1.0
; Устанавливает приложение в папку C:\Program Files (x86)\Child PC Guard
DefaultDirName={commonpf32}\Child PC Guard
; Название папки программы в Пуск
DefaultGroupName=Child PC Guard
; Название установщика
OutputBaseFilename=Child PC Guard Installer
; Метод сжатия
Compression=lzma2
SolidCompression=yes
; Отключить страницу выбора каталога для установки приложения
DisableDirPage=yes
; Отключить страницу выбора группы программ
DisableProgramGroupPage=yes
; Отключение стандартного деинсталлятора
Uninstallable=yes
; Имя для деинсталлятора (Будет отображаться в апплете панели управления "Удаление или изменение программы". )
UninstallDisplayName=Uninstaller CPG
; Иконка деинсталлятора в панели управления (Будет отображаться в апплете панели управления "Удаление или изменение программы".)
UninstallDisplayIcon={app}\img\uninstall.ico
; Права для установщика
PrivilegesRequired=admin

; Включение диалога выбора языка
ShowLanguageDialog=yes

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "ukrainian"; MessagesFile: "compiler:Languages\Ukrainian.isl"

[Dirs]
; Создание папки с доступом на изменение для всех пользователей
Name: "{commonappdata}\Child PC Guard Data"; Permissions: "everyone-full everyone-readexec"

[Files]
; Основные исполняемые файлы
Source: "Child PC Guard.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Child PC Timer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Child PC Unlock User.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Windows CPG Monitor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "run_bot_telegram.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "unins000.exe"; DestDir: "{app}"; Flags: ignoreversion

; Копирование папки img в папку с приложениями (и всем содержимым)
Source: "img\*"; DestDir: "{app}\img"; Flags: ignoreversion recursesubdirs createallsubdirs
; Копируем файл data.json с правами на изменение (файл находится на одном уровне с .iss)
Source: "data.json"; DestDir: "{commonappdata}\Child PC Guard Data"; Flags: ignoreversion; Permissions: "everyone-full"
; Копируем файл log_chpcgu.txt с правами на изменение (файл находится на одном уровне с .iss)
Source: "log_chpcgu.txt"; DestDir: "{commonappdata}\Child PC Guard Data"; Flags: ignoreversion; Permissions: "everyone-full"
; Копируем install_info.txt с правами на изменение (файл находится на одном уровне с .iss)
Source: "install_info.txt"; DestDir: "{commonappdata}\Child PC Guard Data"; Flags: ignoreversion; Permissions: "everyone-full"

[Icons]
; Создание ярлыков в меню "Пуск" в общей папке для всех пользователей - (C:\ProgramData\Microsoft\Windows\Start Menu\Programs\)
Name: "{commonstartmenu}\Programs\Child PC Guard\Child PC Guard"; Filename: "{app}\Child PC Guard.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\icon.ico"
Name: "{commonstartmenu}\Programs\Child PC Guard\Child PC Timer"; Filename: "{app}\Child PC Timer.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\timer.ico"
Name: "{commonstartmenu}\Programs\Child PC Guard\Child PC Unlock User"; Filename: "{app}\Child PC Unlock User.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\unlock.ico"
Name: "{commonstartmenu}\Programs\Child PC Guard\Child PC Monitor"; Filename: "{app}\Windows CPG Monitor.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\monitor.ico"
Name: "{commonstartmenu}\Programs\Child PC Guard\Logs Child PC Guard"; Filename: "notepad.exe"; Parameters: """{commonappdata}\Child PC Guard Data\log_chpcgu.txt"""; WorkingDir: "{commonappdata}\Child PC Guard"; IconFilename: "{app}\img\logs.ico"

; Создание ярлыков для приложений на "Рабочем столе" (для всех пользователей - (C:\Users\Public\Desktop))
Name: "{commondesktop}\Child PC Timer"; Filename: "{app}\Child PC Timer.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\timer.ico"
Name: "{commondesktop}\Child PC Guard"; Filename: "{app}\Child PC Guard.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\icon.ico"

[Run]
; Перезагрузка ПК после установки что бы изменения в реестре вступили в силу относится к -[Registry]
Filename: "{cmd}"; Parameters: "/C shutdown /r /t 5"; Flags: runhidden; Description: "Система будет перезагружена через 5 секунд..."

[UninstallRun]
; Указание на деинсталлятор
Filename: "{app}\UNinstallerCPG.exe"; RunOnceId: "UninstallerCPG"

[Registry]
; Flags: overwrite: Указывает, что если значение уже существует, оно будет перезаписано.
; Включаем UAC на уровне системы
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"; ValueType: dword; ValueName: "EnableLUA"; ValueData: "1"
; Отключение UAC предупреждения для администраторов
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"; ValueType: dword; ValueName: "ConsentPromptBehaviorAdmin"; ValueData: "0"
; Отключение UAC предупреждения для пользователей
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"; ValueType: dword; ValueName: "ConsentPromptBehaviorUser"; ValueData: "0"

; Код выполняет запись в файл (install_info.txt) пути установки программы для последующего считывания приложением
[Code]
procedure InitializeWizard();
begin
  MsgBox('ENG - A reboot may be required for successful installation. Please click "Да" to continue.' + #13#10 + 'УКР - Для успішного встановлення може знадобитися перезавантаження. Будь ласка, натисніть "Так", щоб продовжити.' + #13#10 + 'РУС - Для успешной установки может потребоваться перезагрузка. Пожалуйста, нажмите "Да" для продолжения.', mbInformation, MB_OK);
end;

function AppRunning(AppName: string): Boolean;
var
  ResultCode: Integer;
begin
  Result := false;
  // Запускаем команду tasklist для проверки наличия процесса в списке запущенных
  if Exec(ExpandConstant('{cmd}'), '/C tasklist /FI "IMAGENAME eq ' + AppName + '"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    // Если процесс найден, результат не равен 0, значит, он запущен
    Result := ResultCode = 0;
  end;
end;

procedure UpdateInstallInfoFile;
var
  // Переменная для хранения пути к файлу install_info.txt
  InfoFilePath: String;
  // Переменная для хранения полного пути установки
  InstallPath: String;
  // Переменная для хранения строки в формате JSON
  TxtContent: String;
begin
  // Определяем полный путь к файлу install_info.txt в папке с данными приложения
  InfoFilePath := ExpandConstant('{commonappdata}\\Child PC Guard Data\\install_info.txt');
  // Получаем полный путь установки приложения
  InstallPath := ExpandConstant('{app}');

  // Формируем строку с адресом для записи
  TxtContent := InstallPath;

  // Создаем строковый список для записи информации в файл
  with TStringList.Create do
  try
    // Добавляем TXT-контент в строковый список
    Add(TxtContent);
    // Сохраняем данные в указанный файл
    SaveToFile(InfoFilePath);
  finally
    // Освобождаем память, занятую TStringList
    Free;
  end;
end;

  // Вызов функции для выполнения записи пути в файл
procedure CurStepChanged(CurStep: TSetupStep);
begin
  // Выполняем запись в файл после копирования файлов
  if CurStep = ssPostInstall then
  begin
    UpdateInstallInfoFile;
  end;
end;
