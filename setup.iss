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

[Files]
; Основные исполняемые файлы
Source: "dist\Child PC Guard.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Child PC Timer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Windows CPG Monitor.exe"; DestDir: "{app}"; Flags: ignoreversion

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
Name: "{group}\Logs  Child PC Guard"; Filename: "notepad.exe"; Parameters: """{commonappdata}\ChildPCGuard\log_chpcgu.txt"""; WorkingDir: "{commonappdata}\ChildPCGuard"; IconFilename: "{app}\icon.ico"

; Создание ярлыков для всех приложений на рабочем столе
Name: "{commondesktop}\Child PC Guard"; Filename: "{app}\Child PC Guard.exe"; WorkingDir: "{app}"
Name: "{commondesktop}\Child PC Timer"; Filename: "{app}\Child PC Timer.exe"; WorkingDir: "{app}"
Name: "{commondesktop}\Child PC Monitor"; Filename: "{app}\Windows CPG Monitor.exe"; WorkingDir: "{app}"
Name: "{commondesktop}\Logs  Child PC Guard"; Filename: "notepad.exe"; Parameters: """{commonappdata}\ChildPCGuard\log_chpcgu.txt"""; WorkingDir: "{commonappdata}\ChildPCGuard"; IconFilename: "{app}\icon.ico"

; Создание ярлыка для автозагрузки Windows CPG Monitor.exe
Name: "{userstartup}\Child PC Monitor"; Filename: "{app}\Windows CPG Monitor.exe"; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"; Flags: runasadmin

; Создание ярлыка для удаления приложения
;Name: "{group}\Удалить Child PC Guard Suite"; Filename: "{uninstall}"; IconFilename: "{app}\icon.ico"

[Run]
; Автоматический запуск Child PC Monitor после установки с правами администратора
Filename: "{app}\Windows CPG Monitor.exe"; Description: "Запуск Child PC Monitor"; Flags: nowait postinstall skipifsilent runasadmin

;[UninstallDelete]
;; Удаление файлов данных и логов при деинсталляции (удаляем папку с файлами)
;Type: filesandordirs; Name: "{commonappdata}\ChildPCGuard"
;
;[UninstallRun]
;; Запуск команд при деинсталляции для остановки всех приложений
;Filename: "{app}\Child PC Guard.exe"; Parameters: "/stop"; Flags: runhidden
;Filename: "{app}\Child PC Timer.exe"; Parameters: "/stop"; Flags: runhidden
;Filename: "{app}\Windows CPG Monitor.exe"; Parameters: "/stop"; Flags: runhidden

;[Code]
;; Дополнительный код для удаления приложений и иконок
;procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
;begin
;  if CurUninstallStep = usPostUninstall then
;  begin
;    DeleteFile(ExpandConstant('{commondesktop}\Child PC Guard.lnk'));
;    DeleteFile(ExpandConstant('{commondesktop}\Child PC Timer.lnk'));
;    DeleteFile(ExpandConstant('{commondesktop}\Child PC Monitor.lnk'));
;    DeleteFile(ExpandConstant('{commondesktop}\Logs  Child PC Guard.lnk'));
;    DeleteFile(ExpandConstant('{userstartup}\Child PC Monitor.lnk')); ; Удаление ярлыка из автозагрузки
;    DeleteFile(ExpandConstant('{app}\icon.ico')); ; Удаление иконки из папки программы
;  end;
;end;
