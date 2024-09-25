# import os
# import wx
# import gettext
#
# from config_app import FOLDER_IMG
#
# _ = gettext.gettext
#
# class SplashScreen(wx.Frame):
#     def __init__(self, parent):
#         wx.Frame.__init__(self,
#                           parent,
#                           id=wx.ID_ANY,
#                           title=_("Child PC Guard"),
#                           pos=wx.DefaultPosition,
#                           size=wx.DefaultSize,
#                           style=wx.FRAME_SHAPED | wx.STAY_ON_TOP
#                           )
#
#         # Загрузка изображения
#         image_path = os.path.join(FOLDER_IMG, 'screensaver1.png')
#         self.bitmap = wx.Bitmap(image_path)
#
#         # Установка размеров окна по размерам изображения
#         self.SetClientSize((self.bitmap.GetWidth(), self.bitmap.GetHeight()))
#         # Устанавливаем окно в центре экрана
#         self.Center()
#
#         # Установка прозрачного фона и формы окна по изображению
#         self.SetWindowShape()
#
#         # Устанавливаем изначально полностью прозрачное окно (прозрачность = 0)
#         self.SetTransparent(0)
#
#         # Привязка события отрисовки
#         self.Bind(wx.EVT_PAINT, self.OnPaint)
#
#         # Таймер для анимации плавного появления
#         self.alpha_value = 0  # Начальная прозрачность (0 = полностью прозрачно)
#         self.fade_in_timer = wx.Timer(self)
#         self.Bind(wx.EVT_TIMER, self.OnFadeInTimer, self.fade_in_timer)
#         self.fade_in_timer.Start(30)  # Каждые 30 миллисекунд обновляем прозрачность
#
#         # Таймер для закрытия окна после полной отрисовки
#         self.close_timer = wx.Timer(self)
#         self.Bind(wx.EVT_TIMER, self.OnCloseTimer, self.close_timer)
#
#     def SetWindowShape(self):
#         """Устанавливает форму окна по форме изображения."""
#         region = wx.Region(self.bitmap)
#         self.SetShape(region)
#
#     def OnPaint(self, event):
#         """Отрисовка изображения на окне."""
#         dc = wx.BufferedPaintDC(self)
#         dc.DrawBitmap(self.bitmap, 0, 0, True)
#
#     def OnFadeInTimer(self, event):
#         """Плавное появление окна."""
#         if self.alpha_value < 255:
#             self.alpha_value += 3  # Увеличиваем прозрачность
#             self.SetTransparent(self.alpha_value)  # Устанавливаем новую прозрачность
#         else:
#             self.OnCloseTimer(event)
#             self.fade_in_timer.Stop()  # Останавливаем таймер после достижения полной прозрачности
#             self.Destroy()
#             #self.close_timer.Start(1000)  # Закрываем окно через 1.5 секунды после полного появления
#
#     def OnCloseTimer(self, event):
#         """Закрывает окно заставки."""
#         self.Close(True)
#         self.Destroy()
#
# def main_splash():
#     app = wx.App(False)
#     splash = SplashScreen(None)
#     splash.Show()
#     app.MainLoop()
#
# if __name__ == "__main__":
#     main_splash()


import os
import wx
import gettext

from config_app import FOLDER_IMG

_ = gettext.gettext


class SplashScreen(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self,
                          parent,
                          id=wx.ID_ANY,
                          title=_("Child PC Guard"),
                          pos=wx.DefaultPosition,
                          size=wx.DefaultSize,
                          style=wx.FRAME_SHAPED | wx.STAY_ON_TOP
                          )

        # Загрузка изображения
        image_path = os.path.join(FOLDER_IMG, 'screensaver1.png')
        self.bitmap = wx.Bitmap(image_path)

        # Установка размеров окна по размерам изображения
        self.SetClientSize((self.bitmap.GetWidth(), self.bitmap.GetHeight()))
        # Устанавливаем окно в центре экрана
        self.Center()

        # Установка прозрачного фона и формы окна по изображению
        self.SetWindowShape()

        # Изначально заставка полностью видима (прозрачность = 255)
        self.SetTransparent(255)

        # Привязка события отрисовки
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        # Таймер для плавного исчезновения
        self.alpha_value = 100  # Начальная прозрачность
        self.fade_out_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnFadeOutTimer, self.fade_out_timer)

        # Запуск таймера для плавного исчезновения через 2 секунды
        wx.CallLater(500, self.StartFadeOut)

    def SetWindowShape(self):
        """Устанавливает форму окна по форме изображения."""
        region = wx.Region(self.bitmap)
        self.SetShape(region)

    def OnPaint(self, event):
        """Отрисовка изображения на окне."""
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0, True)

    def StartFadeOut(self):
        """Запускает процесс плавного исчезновения окна."""
        self.fade_out_timer.Start(5)  # Каждые 30 миллисекунд уменьшаем прозрачность

    def OnFadeOutTimer(self, event):
        """Плавное исчезновение окна."""
        if self.alpha_value > 0:
            self.alpha_value -= 5  # Уменьшаем прозрачность
            self.SetTransparent(self.alpha_value)  # Устанавливаем новую прозрачность
        else:
            self.fade_out_timer.Stop()  # Останавливаем таймер, когда прозрачность достигнет 0
            self.Close(True)  # Закрываем окно


def main_splash():
    app = wx.App(False)
    splash = SplashScreen(None)
    splash.Show()
    app.MainLoop()


if __name__ == "__main__":
    main_splash()
