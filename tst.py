# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MyDialog1
###########################################################################

class MyDialog1 ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        sizer_lang = wx.BoxSizer( wx.VERTICAL )

        self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        sizer_lang.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

        sizer_txt_lang = wx.BoxSizer( wx.VERTICAL )

        self.stat_txt = wx.StaticText( self, wx.ID_ANY, _(u"Выберите язык"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stat_txt.Wrap( -1 )

        self.stat_txt.SetForegroundColour( wx.Colour( 255, 0, 0 ) )

        sizer_txt_lang.Add( self.stat_txt, 0, 0, 5 )


        sizer_lang.Add( sizer_txt_lang, 0, wx.ALIGN_CENTER, 5 )

        sizer_btn_lang = wx.BoxSizer( wx.HORIZONTAL )

        self.btn_uk = wx.Button( self, wx.ID_ANY, _(u"Українська"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_uk.SetLabelMarkup( _(u"Українська") )
        sizer_btn_lang.Add( self.btn_uk, 0, wx.ALL, 5 )

        self.btn_en = wx.Button( self, wx.ID_ANY, _(u"English"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer_btn_lang.Add( self.btn_en, 0, wx.ALL, 5 )

        self.btn_ru = wx.Button( self, wx.ID_ANY, _(u"Русский"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer_btn_lang.Add( self.btn_ru, 0, wx.ALL, 5 )


        sizer_lang.Add( sizer_btn_lang, 0, wx.EXPAND, 5 )

        self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        sizer_lang.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )


        bSizer1.Add( sizer_lang, 1, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()
        bSizer1.Fit( self )

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


