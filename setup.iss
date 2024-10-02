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
; Отключить страницу выбора каталога
DisableDirPage=yes
; Отключить страницу выбора группы программ
;DisableProgramGroupPage=yes
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

; Копирование файлов из папки img в папку с приложениями
Source: "img\*"; DestDir: "{app}\img"; Flags: ignoreversion recursesubdirs createallsubdirs
; Копируем файл data.json с правами на изменение (файл находится на одном уровне с .iss)
Source: "data.json"; DestDir: "{commonappdata}\Child PC Guard Data"; Flags: ignoreversion; Permissions: "everyone-full"
; Копируем файл log_chpcgu.txt с правами на изменение (файл находится на одном уровне с .iss)
Source: "log_chpcgu.txt"; DestDir: "{commonappdata}\Child PC Guard Data"; Flags: ignoreversion; Permissions: "everyone-full"

[Icons]
; Создание ярлыков в меню "Пуск" в общей папке для всех пользователей - (C:\ProgramData\Microsoft\Windows\Start Menu\Programs\)
Name: "{commonstartmenu}\Programs\Child PC Guard\Child PC Guard"; Filename: "{app}\Child PC Guard.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\icon.ico"
Name: "{commonstartmenu}\Programs\Child PC Guard\Child PC Timer"; Filename: "{app}\Child PC Timer.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\timer.ico"
Name: "{commonstartmenu}\Programs\Child PC Guard\Child PC Unlock User"; Filename: "{app}\Child PC Unlock User.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\unlock.ico"
Name: "{commonstartmenu}\Programs\Child PC Guard\Child PC Monitor"; Filename: "{app}\Windows CPG Monitor.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\monitor.ico"
Name: "{commonstartmenu}\Programs\Child PC Guard\Logs Child PC Guard"; Filename: "notepad.exe"; Parameters: """{commonappdata}\Child PC Guard Data\log_chpcgu.txt"""; WorkingDir: "{commonappdata}\Child PC Guard"; IconFilename: "{app}\img\logs.ico"

; Создание ярлыков для всех приложений на "Рабочем столе" для всех пользователей - (C:\Users\Public\Desktop)
;Name: "{commondesktop}\Child PC Guard"; Filename: "{app}\Child PC Guard.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\icon.ico"
Name: "{commondesktop}\Child PC Timer"; Filename: "{app}\Child PC Timer.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\timer.ico"

; Создание ярлыка в папке автозагрузки пользователя сессии при установке программы
;Name: "{userstartup}\Child PC Monitor"; Filename: "{app}\Windows CPG Monitor.exe"; WorkingDir: "{app}"; IconFilename: "{app}\img\icon.ico"

[Run]
; Запуск приложения создания задачи в планировщике заданий в момент установки (приложение должно быть в одной папке и на одном уровне с файлом инсталляции программы)
Filename: "{app}\add_task_schedule.exe"; Flags: waituntilterminated

[UninstallRun]
; Удаление задачи - 'Start CPG Monitor', через CMD из планировщика заданий (для деинсталлятора)
Filename: "{cmd}"; Parameters: "/C schtasks /Delete /TN ""Start CPG Monitor"" /F"; Flags: runhidden





















