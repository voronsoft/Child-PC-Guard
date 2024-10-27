"""
Модуль добавления задания в 'Планировщик заданий'
Запуск каждые две минуты приложения - Windows CPG Monitor.exe
(для запуска мониторинга за программой Child PC Guard)
"""
import datetime
import sys

import win32com.client

from config_app import path_monitor_exe
from function import log_error

scheduler = win32com.client.Dispatch('Schedule.Service')
scheduler.Connect()
rootFolder = scheduler.GetFolder("\\")

# Название задачи в планировщике задач
taskName = "Start CPG Monitor"


def task_exists(task_name):
    """
    Проверяет, существует ли задача с таким именем в Планировщике заданий.

    :param task_name: Название задачи
    :return: bool: True/False
    """
    try:
        task = rootFolder.GetTask(task_name)
        return True
    except Exception:
        return False


def run_add_task():
    """
    Функция добавления задачи в 'Планировщик заданий'
    :return:
    """

    # Если задача уже существует, выводим сообщение и выходим
    if task_exists(taskName):
        log_error(f"Задача '{taskName}' уже существует в Планировщике заданий.\nУстановка отменена.")
    else:
        # Создание новой задачи, если ее еще нет
        taskDef = scheduler.NewTask(0)

        # Заполнение информации о задаче
        registrationInfo = taskDef.RegistrationInfo
        registrationInfo.Description = ("Запускает CPG APP Monitor каждые 2 минуты в течении:"
                                        " Безгранично. Работает от имени группа: Пользователи.")
        registrationInfo.Author = "TG: @norovprog"
        registrationInfo.Date = datetime.datetime.now().isoformat()

        # Настройки задачи
        settings = taskDef.Settings
        settings.Enabled = True
        settings.MultipleInstances = 1  # IgnoreNew
        settings.AllowHardTerminate = True
        settings.ExecutionTimeLimit = "PT72H"
        settings.Priority = 7

        # Триггер запуска
        trigger = taskDef.Triggers.Create(1)  # TimeTrigger
        trigger.StartBoundary = "2024-09-30T00:00:00"
        trigger.Repetition.Interval = "PT2M"
        trigger.Repetition.StopAtDurationEnd = False
        trigger.Enabled = True

        # Привилегии
        principal = taskDef.Principal
        principal.GroupId = "S-1-5-32-545"  # Группа Пользователи (SID)
        principal.RunLevel = 0  # LeastPrivilege

        # Действие запуска программы
        action = taskDef.Actions.Create(0)  # Exec
        # Путь к приложению для запуска из Планировщика задач
        action.Path = path_monitor_exe
        # action.Path = r"C:\Program Files (x86)\Child PC Guard\Windows CPG Monitor.exe"

        # Регистрируем задачу в планировщике
        rootFolder.RegisterTaskDefinition(
                taskName,
                taskDef,
                6,  # TASK_CREATE_OR_UPDATE
                None,  # Логин пользователя (None = текущий пользователь)
                None,
                3,  # TASK_LOGON_GROUP
                None
        )

        log_error(f"Задача '{taskName}' успешно добавлена в 'Планировщик заданий'")


if __name__ == '__main__':
    run_add_task()
