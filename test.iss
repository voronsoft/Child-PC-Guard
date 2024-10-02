;
;
; Пример файла Inno Setup для установки тестового приложения
[Setup]
; Основные параметры установки
; Название приложения
AppName=Test Setup  
; Версия приложения 
AppVersion=1.0                   
; Директория по умолчанию для установки - C:\Program Files (x86)\Test Folder
DefaultDirName={commonpf}\Test Folder  
; Название группы (папки) в меню "Пуск"
DefaultGroupName=Test Folder
; Директория для сохранения установочного файла
OutputDir=.\Output               
; Имя выходного установочного файла
OutputBaseFilename=TestAppSetup
; Требуется запуск от имени администратора
;PrivilegesRequired=admin
;
; Имя для деинсталлятора (Будет отображаться в апплете панели управления "Удаление или изменение программы". )
UninstallDisplayName=CPG uninstall    

; Иконка деинсталлятора в панели управления (Будет отображаться в апплете панели управления "Удаление или изменение программы".)
UninstallDisplayIcon={app}\uninstall.ico    

         
[Files]
; Укажите файлы, которые будут включены в установку
;Source: "task_data.xml"; DestDir: "{app}"; Flags: ignoreversion
; Приложение для запуска создания задачи в планировщике заданий.
Source: "add_task_schedule.exe"; DestDir: "{app}"; Flags: ignoreversion


[Icons]
; Создание ярлыка в меню "Пуск\Test Folder\Тест ярлык в пуск" и на рабочем столе
Name: "{group}\Тест ярлык в пуск"; Filename: "{app}\1YourApp.exe"
; Создание ярлыка на рабочем столе
Name: "{userdesktop}\Тест ярлык РС"; Filename: "{app}\2YourApp.exe"
; Создас значек в папке автозагрузки пользователя
Name: "{userstartup}\Test link.lnk"; Filename: "{app}\3YourApp.exe"


[Run]
; Запуск приложения создания задачи в планировщике заданий в момент установки (приложение должно быть в одной папке и на одном уровне с файлом инсталляции программы)
Filename: "{app}\add_task_schedule.exe"; Flags: waituntilterminated

[UninstallRun]
; Удаление задачи - 'Start CPG Monitor', через CMD из планировщика заданий (для деинсталлятора)
Filename: "{cmd}"; Parameters: "/C schtasks /Delete /TN ""Start CPG Monitor"" /F"; Flags: runhidden

[UninstallDelete]
; Удаление дополнительных файлов или папок при деинсталляции (пример удалить ярлык из папки автозагрузки ПОЛЬЗОВАТЕЛЯ (для деинсталлятора))
; Путь для примера - C:\Users\USER_NAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
Type: files; Name: "{userstartup}\Test link.lnk"

