import os
import random

import wx

import config_localization
import function
from config_app import SCREENSAVER1, SCREENSAVER2

# Подключаем локализацию
_ = config_localization.setup_locale(function.read_data_json("language"))


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

        # Загрузка изображения для заставки, выбирается рандомно одно из изображений из папки с изображениями
        image_path = random.choice([SCREENSAVER1, SCREENSAVER2])  # Случайно выбираем одно из изображений
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

        # Запуск таймера для плавного исчезновения через 0,5 секунды
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
        self.fade_out_timer.Start(5)  # Каждые 5 миллисекунд уменьшаем прозрачность

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
