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
;
Compression=lzma2
SolidCompression=yes
; Отключить страницу выбора каталога для установки приложения
;DisableDirPage=yes
; Отключить страницу выбора группы программ
DisableProgramGroupPage=yes
; Имя для деинсталлятора (Будет отображаться в апплете панели управления "Удаление или изменение программы". )
UninstallDisplayName=CPG uninstall
; Иконка деинсталлятора в панели управления (Будет отображаться в апплете панели управления "Удаление или изменение программы".)
UninstallDisplayIcon={app}\img\uninstall.ico

[Dirs]
; Создание папки с доступом на изменение для всех пользователей
Name: "{commonappdata}\Child PC Guard Data"; Permissions: "everyone-full everyone-readexec"

[Files]
; Основные исполняемые файлы
Source: "Child PC Guard.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Child PC Timer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Child PC Unlock User.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Windows CPG Monitor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "add_task_schedule.exe"; DestDir: "{app}"; Flags: ignoreversion

; Копирование папки img в папку с приложениями (и всем содержимым)
Source: "img\*"; DestDir: "{app}\img"; Flags: ignoreversion recursesubdirs createallsubdirs
; Копируем файл data.json с правами на изменение (файл находится на одном уровне с .iss)
Source: "data.json"; DestDir: "{commonappdata}\Child PC Guard Data"; Flags: ignoreversion; Permissions: "everyone-full"
; Копируем файл log_chpcgu.txt с правами на изменение (файл находится на одном уровне с .iss)
Source: "log_chpcgu.txt"; DestDir: "{commonappdata}\Child PC Guard Data"; Flags: ignoreversion; Permissions: "everyone-full"
; Копируем install_info.json с правами на изменение (файл находится на одном уровне с .iss)
Source: "install_info.json"; DestDir: "{commonappdata}\Child PC Guard Data"; Flags: ignoreversion; Permissions: "everyone-full"

[Icons]
; Создание ярлыков в меню "Пуск" в общей папке для всех пользователей - (C:\ProgramData\Microsoft\Windows\Start Menu\Programs\)
Name: "{commonstartmenu}\Programs\Child PC Guard\Child PC Guard"; Filename: "{app}\Child PC Guard.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\icon.ico"
Name: "{commonstartmenu}\Programs\Child PC Guard\Child PC Timer"; Filename: "{app}\Child PC Timer.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\timer.ico"
Name: "{commonstartmenu}\Programs\Child PC Guard\Child PC Unlock User"; Filename: "{app}\Child PC Unlock User.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\unlock.ico"
Name: "{commonstartmenu}\Programs\Child PC Guard\Child PC Monitor"; Filename: "{app}\Windows CPG Monitor.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\monitor.ico"
Name: "{commonstartmenu}\Programs\Child PC Guard\Logs Child PC Guard"; Filename: "notepad.exe"; Parameters: """{commonappdata}\Child PC Guard Data\log_chpcgu.txt"""; WorkingDir: "{commonappdata}\Child PC Guard"; IconFilename: "{app}\img\logs.ico"

; Создание ярлыков для приложений на "Рабочем столе" (для всех пользователей - (C:\Users\Public\Desktop))
Name: "{commondesktop}\Child PC Timer"; Filename: "{app}\Child PC Timer.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\timer.ico"

[Run]
; Запуск приложения создания задачи в планировщике заданий в момент установки (приложение должно быть в одной папке и на одном уровне с файлом инсталляции программы)
Filename: "{app}\add_task_schedule.exe"; Flags: waituntilterminated

[UninstallRun]
; Удаление задачи - 'Start CPG Monitor', через CMD из планировщика заданий (для деинсталлятора)
Filename: "{cmd}"; Parameters: "/C schtasks /Delete /TN ""Start CPG Monitor"" /F"; Flags: runhidden

; Код выполняет запись в файл (install_info.json) пути установки программы для последующего считывания приложением
[Code]
procedure UpdateInstallInfoFile;
var
  // Переменная для хранения пути к файлу install_info.json
  InfoFilePath: String;
  // Переменная для хранения полного пути установки
  InstallPath: String;
  // Переменная для хранения строки в формате JSON
  JsonContent: String;
begin
  // Определяем полный путь к файлу install_info.json в папке с данными приложения
  InfoFilePath := ExpandConstant('{commonappdata}\Child PC Guard Data\install_info.json');

  // Получаем полный путь установки приложения
  InstallPath := ExpandConstant('{app}');

  // Формируем строку в формате JSON
  JsonContent := '{"app_ins_path": "' + InstallPath + '"}';

  // Создаем строковый список для записи информации в файл
  with TStringList.Create do
  try
    // Устанавливаем кодировку UTF-8 для сохранения
    Encoding := TEncoding.UTF8;

    // Добавляем JSON-контент в строковый список
    Add(JsonContent);

    // Сохраняем данные в указанный файл
    SaveToFile(InfoFilePath);
  finally
    // Освобождаем память, занятую TStringList
    Free;
  end;
end;
