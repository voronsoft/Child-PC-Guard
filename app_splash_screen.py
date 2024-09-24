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

        # Инициализация окна без рамки и с прозрачным фоном
        # super().__init__(None, style=wx.FRAME_SHAPED | wx.STAY_ON_TOP)

        image_path = os.path.join(FOLDER_IMG, 'screensaver1.png')
        # Проверка существования файла изображения
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Файл не найден: {image_path}")

        # Загрузка изображения
        self.bitmap = wx.Bitmap(image_path)

        # Установка размеров окна по размерам изображения
        self.SetClientSize((self.bitmap.GetWidth(), self.bitmap.GetHeight()))

        # Устанавливаем окно в центре экрана
        self.Center()

        # Установка прозрачного фона и формы окна по изображению
        self.SetWindowShape()

        # Привязка события отрисовки
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        # Таймер для закрытия окна через 2 секунды
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnCloseTimer, self.timer)
        self.timer.Start(1500)  # Запускаем таймер на 2 секунды

    def SetWindowShape(self):
        """Устанавливает форму окна по форме изображения."""
        region = wx.Region(self.bitmap)
        self.SetShape(region)

    def OnPaint(self, event):
        """Отрисовка изображения на окне."""
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0)

    def OnCloseTimer(self, event):
        """Закрывает окно заставки."""
        self.Destroy()

def main():
    app = wx.App(False)
    splash = SplashScreen(None)
    splash.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
