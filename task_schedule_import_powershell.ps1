# Скрипт выполняет запуск task_data.xml файла, в котором описано задание для планировщика задач.
#
# Политика выполнения сценариев PowerShell (Execution Policy) по умолчанию запрещает выполнение сценариев (скриптов .ps1) в системе.
# Это сделано для защиты от выполнения потенциально вредоносных скриптов.
# Решение что бы выполнение скрипта не блокировалось при запуске:
# Изменение политики для текущей сессии PowerShell (безопасный вариант):
# Это изменит политику только для текущей сессии PowerShell (она будет действовать до закрытия окна).
# Открой PowerShell с правами администратора и выполни команду:
# Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
# Это позволит выполнить скрипт в этой сессии без изменения глобальных настроек политики.
# После изменения политики попробуй снова запустить скрипт:
# Запусти скрипт командой : .\task_schedule_import_powershell.ps1
# После выполнения скрипта рекомендуется вернуть политику выполнения на более безопасный уровень:
# Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope LocalMachine
# Таким образом, ты сможешь избежать случайного выполнения нежелательных скриптов в будущем.


# Устанавливаем политику выполнения для текущей сессии
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# Получаем путь к каталогу, где находится сценарий
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Указываем путь к XML файлу
# Используем относительный путь к файлу XML
# $xmlPath = "C:\Program Files (x86)\Child PC Guard\task_data.xml"
$xmlPath = Join-Path $scriptDir "task_data.xml"

# Чтение содержимого XML-файла
$xmlContent = Get-Content $xmlPath -Raw

# Регистрируем задачу с использованием содержимого XML
Register-ScheduledTask -Xml $xmlContent -TaskName "Start CPG Monitor"
