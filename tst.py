import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(400, 300))

        # Создаем панель
        panel = wx.Panel(self)

        # Создаем тулбар
        toolbar = self.CreateToolBar()

        # Добавляем первую радиокнопку
        self.btn_tool_block_interface = toolbar.AddTool(wx.ID_ANY,
                                                        "Заблокировать интерфейс",
                                                        wx.Bitmap(r"img\close.ico"),
                                                        wx.NullBitmap,
                                                        wx.ITEM_RADIO,
                                                        "Заблокировать интерфейс",
                                                        "Блокировка интерфейса")

        # Добавляем вторую радиокнопку
        self.btn_tool_unblock_interface = toolbar.AddTool(wx.ID_ANY,
                                                          "Разблокировать интерфейс",
                                                          wx.Bitmap(r"img\open.ico"),
                                                          wx.NullBitmap,
                                                          wx.ITEM_RADIO,
                                                          "Разблокировать интерфейс",
                                                          "Разблокировать интерфейс")

        # Реализуем тулбар
        toolbar.Realize()

        # Привязываем события к радиокнопкам
        # self.Bind(wx.EVT_TOOL, self.OnBlockInterface, self.btn_tool_block_interface.GetId())
        # self.Bind(wx.EVT_TOOL, self.OnUnblockInterface, self.btn_tool_unblock_interface.GetId())

        self.Centre()
        self.Show()

    def OnBlockInterface(self, event):
        print("Интерфейс заблокирован")

    def OnUnblockInterface(self, event):
        print("Интерфейс разблокирован")

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, title="Toolbar Radio Button Example")
        self.SetTopWindow(frame)
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
