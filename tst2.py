# -*- coding: utf-8 -*-
import wx
import wx.html
import function
import config_localization

# Подключаем локализацию
_ = config_localization.setup_locale(function.read_data_json("language"))


###########################################################################
## Class DocWindow
## Класс окна для документации
###########################################################################

class DocWindow(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self,
                           parent,
                           id=wx.ID_ANY,
                           title=_("Документация"),
                           pos=wx.DefaultPosition,
                           size=(700, 500),
                           style=wx.DEFAULT_DIALOG_STYLE
                           )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        # Создаем HtmlWindow для отображения документации
        self.html_win = wx.html.HtmlWindow(self, size=(700, 450))

        # HTML-контент
        html_content = """
        <html>
            <head>
                <title>Документация</title>
                <style>
                    body { font-family: 'Segoe UI'; font-size: 12px; }
                    h1 { color: #333; }
                    h2 { color: #007acc; }
                    ul { list-style-type: disc; }
                    li { margin: 5px 0; }
                </style>
            </head>
            <body>
                <h1>Описание программы</h1>
                <p>Эта программа предназначена для управления детскими компьютерами.</p>
                <h2>Основные функции:</h2>
                <ul>
                    <li>Мониторинг активности</li>
                    <li>Ограничение времени использования</li>
                    <li>Удаленный доступ</li>
                </ul>
                <p>Вы можете изменить настройки в меню.</p>
                <h2>Примечание:</h2>
                <p>Не забудьте сохранить изменения перед выходом из программы.</p>
            </body>
        </html>
        """

        # Устанавливаем HTML-контент
        self.html_win.SetPage(html_content)

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(self.html_win, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)

        # Подключаемые события в программе ---------------
        self.Bind(wx.EVT_CLOSE, self.on_close)  # Событие закрытия окна

    # Обработчики событий
    def on_close(self, event):
        """Обработчик закрытия программы"""
        self.Destroy()


# Основная секция для запуска программы
if __name__ == '__main__':
    app = wx.App(False)
    doc_app = DocWindow(None)
    doc_app.Show()
    app.MainLoop()
