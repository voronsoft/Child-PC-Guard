WXPYTHON localization doc  

**Supporting internationalization**  
In the interconnected world that we live in today, it is very important to take
internationalization into account when developing an application's interface.  
There is very little to lose in designing an application that completely supports internationalization right
from the beginning, but a whole lot to lose if you don't.  
This recipe will show how to set up an application to use wxPython's built-in support for interface translations.  

**How to do it...**
Below, we will create a complete sample application that shows how to support localization
in a wxPython application's user interface.  
The first thing to note is the alias for wx.GetTranslation that we use below to wrap all interface strings in the application:  

```python
import wx
import os
# Make a shorter alias
_ = wx.GetTranslation
```  
Next, during the creation of our App object, we create and save a reference to a Locale object.  
We then tell the Locale object where we keep our translation files, so that it knows where to look up translations when the GetTranslation function is called:  
```python
class I18NApp(wx.App):
    def OnInit(self):
         self.SetAppName("I18NTestApp")
         # Get Language from last run if set
         config = wx.Config()
         language = config.Read('lang', 'LANGUAGE_DEFAULT')
         # Setup the Locale
         self.locale = wx.Locale(getattr(wx, language))
         path = os.path.abspath("./locale") + os.path.sep
         self.locale.AddCatalogLookupPathPrefix(path)
         self.locale.AddCatalog(self.GetAppName())
         # Local is not setup so we can create things that
         # may need it to retrieve translations.
         self.frame = TestFrame(None,
         title=_("Sample App"))
         self.frame.Show()
         return True
```
Then, in the rest, we create a simple user interface that will allow the application to switch
the language between English and Japanese:  
```python
class TestFrame(wx.Frame):
    """Main application window"""

    def __init__(self, *args, **kwargs):
        super(TestFrame, self).__init__(*args, **kwargs)
        # Attributes
        self.panel = TestPanel(self)
        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize((300, 300))


class TestPanel(wx.Panel):
    def __init__(self, parent):
        super(TestPanel, self).__init__(parent)
        
        # Attributes
        self.closebtn = wx.Button(self, wx.ID_CLOSE)
        self.langch = wx.Choice(self,
                                choices=[_("English"),
                                         _("Japanese")]
                                )
        # Layout
        self.__DoLayout()
        # Event Handler
        self.Bind(wx.EVT_CHOICE, self.OnChoice)
        self.Bind(wx.EVT_BUTTON,
                  lambda event: self.GetParent().Close()
                  )


def __DoLayout(self):
    vsizer = wx.BoxSizer(wx.VERTICAL)
    hsizer = wx.BoxSizer(wx.HORIZONTAL)
    
    label = wx.StaticText(self, label=_("Hello"))
    hsizer.AddStretchSpacer()
    hsizer.Add(label, 0, wx.ALIGN_CENTER)
    hsizer.AddStretchSpacer()
    
    langsz = wx.BoxSizer(wx.HORIZONTAL)
    langlbl = wx.StaticText(self, label=_("Language"))
    langsz.AddStretchSpacer()
    langsz.Add(langlbl, 0, wx.ALIGN_CENTER_VERTICAL)
    langsz.Add(self.langch, 0, wx.ALL, 5)
    langsz.AddStretchSpacer()
    
    vsizer.AddStretchSpacer()
    vsizer.Add(hsizer, 0, wx.EXPAND)
    vsizer.Add(langsz, 0, wx.EXPAND | wx.ALL, 5)
    vsizer.Add(self.closebtn, 0, wx.ALIGN_CENTER)
    vsizer.AddStretchSpacer()
    
    self.SetSizer(vsizer)


    def OnChoice(self, event):
        sel = self.langch.GetSelection()
        config = wx.Config()
        if sel == 0:
            val = 'LANGUAGE_ENGLISH'
        else:
            val = 'LANGUAGE_JAPANESE'
            config.Write('lang', val)
 
if __name__ == '__main__':
    app = I18NApp(False)
    app.MainLoop()
```
**How it works...**  
The little sample application above shows how to make use of the support for translations in
a wxPython application. Changing the selected language in the Choice control and restarting
the application will change the interface strings between English and Japanese. Making use
of translations is pretty easy, so let's just take a look at the important parts that make it work.
First, we created an alias of _ for the function wx.GetTranslation, so that it is shorter to
type and easier to read. This function should be wrapped around any string in the application
that will be shown to the user in the interface.
Next, in our Application's OnInit method, we did a few things to set up the proper locale
information for loading the configured translations. First, we created a Locale object. It is
necessary to keep a reference to this object so that it does not get garbage collected. Hence,
we saved it to self.locale. Next, we set up the Locale object to let it know where our
translation resource files are located, by first calling AddCatalogLookupPathPrefix with
the directory where we keep our translation files. Then we tell it the name of the resource files
for our application by calling AddCatalog with the name of our application object. In order for
the translations to be loaded, the following directory structure is required for each language
under the catalog lookup path prefix directory:
Lang_Canonical_Name/LC_MESSAGES/CatalogName.mo
So, for example, for our application's Japanese translation, we have the following directory
layout under our locale directory.
ja_JP/LC_MESSAGES/I18NTestApp.mo
After the Locale object has been created, any calls to GetTranslation will use the locale
to load the appropriate string from the gettext catalog file.  
  
**There's more...**  
wxPython uses gettext-formatted files for loading string resources from. There are two
files for each translation. The .po file (Portable Object) is the file that is edited to create the
mapping of the default string to the translated version. The other file is the .mo file (Machine
Object) which is the compiled version of the .po file. To compile a .po file to a .mo file, you
need to use the msgfmt tool. This is part of gettext on any Linux platform. It can also be
installed on OS X through fink, and on Windows through Cygwin. The following command
line statement will generate the .mo file from the given input .po file.
```jsunicoderegexp
msgfmt ja_JP.po
```

**Distributing an application**
Once the application that you have been working on is complete, it is time to put together a
way to distribute the application to its users. wxPython applications can be distributed like any
other Python application or script, by creating a setup.py script and using the distutils
module's setup function. However, this recipe will focus on how to create standalone
executables for Windows and OS X by creating a build script that uses py2exe and py2app
respectively for the two target platforms. Creating a standalone application makes it much
easier for the user to install the application on their system, which means that more people
are likely to use it.  
**Getting ready**
Here, we will create a simple setup.py template that, with a few simple customizations, can
be used to build Windows and OS X binaries for most wxPython applications. The Application
Information section here at the top can be modified to specify the application's name and
other specific information.  
```python
import wx
import sys
#---- Application Information ----#
APP = "FileEditor.py"
NAME = "File Editor"
VERSION = "1.0"
AUTHOR = "Author Name"
AUTHOR_EMAIL = "authorname@someplace.com"
URL = "http://fileeditor_webpage.foo"
LICENSE = "wxWidgets"
YEAR = "2010"
#---- End Application Information ----#
```
Here, we will define a method that uses py2exe to build a Windows executable from the
Python script specified in the APP variable in the Application Information section:  
```python
RT_MANIFEST = 24
def BuildPy2Exe():
    """Generate the Py2exe files"""
    from distutils.core import setup
    try:
    import py2exe
    except ImportError:
    print "\n!! You dont have py2exe installed. !!\n"
    exit()
```
Windows binaries have a manifest embedded in them that specifies dependencies and other
settings. The sample code that accompanies this chapter includes the following two XML files
that will ensure that the GUI has the proper themed controls when running on Windows XP
and greater:  
```python
    pyver = sys.version_info[:2]
    if pyver == (2, 6):
    fname = "py26manifest.xml"
    elif pyver == (2, 5):
    fname = "py25manifest.xml"
    else:
    vstr = ".".join(pyver)
    assert False, "Unsupported Python Version %s" % vstr
    with open(fname, 'rb') as handle:
    manifest = handle.read()
    manifest = manifest % dict(prog=NAME)
```
The OPTS dictionary specifies the py2exe options. These are some standard settings
that should be good for most applications, but they can be tweaked further if necessary
for specific use cases:  
```python
    OPTS = {"py2exe" : {"compressed" : 1,
    "optimize" : 1,
    "bundle_files" : 2,
    "excludes" : ["Tkinter",],
    "dll_excludes": ["MSVCP90.dll"]}}
```
The windows keyword to the setup function is used to specify that we are creating a GUI
application and is used to specify what the application icon and manifest are to embed in
the binary:  
```python
    setup(
        name=NAME,
        version=VERSION,
        options=OPTS,
        windows=[{"script": APP,
                  "icon_resources": [(1, "Icon.ico")],
                  "other_resources": [(RT_MANIFEST, 1,
                                       manifest)],
                  }],
        description=NAME,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        license=LICENSE,
        url=URL,
)
```
Next we have our OS X build method that uses py2app to build the binary applet bundle:  
```python
def BuildOSXApp():
    """Build the OSX Applet"""
    from setuptools import setup
```
Here, we define a PLIST, which is very similar in purpose to the manifest used by Windows
binaries. It is used to define some information about the application that the OS uses to know
what roles the application fills.  
```python
    # py2app uses this to generate the plist xml for
    # the applet.
    copyright = "Copyright %s %s" % (AUTHOR, YEAR)
    appid = "com.%s.%s" % (NAME, NAME)
    PLIST = dict(CFBundleName=NAME,
                 CFBundleIconFile='Icon.icns',
                 CFBundleShortVersionString=VERSION,
                 CFBundleGetInfoString=NAME + " " + VERSION,
                 CFBundleExecutable=NAME,
                 CFBundleIdentifier=appid,
                 CFBundleTypeMIMETypes=['text/plain', ],
                 CFBundleDevelopmentRegion='English',
                 NSHumanReadableCopyright=copyright
                 )
```
The following dictionary specifies the py2app options that setup() will use when building
the application:  
```python
    PY2APP_OPTS = dict(iconfile = "Icon.icns",
                        argv_emulation = True,
                        optimize = True,
                        plist = PLIST)
    setup(
        app = [APP,],
        version = VERSION,
        options = dict( py2app = PY2APP_OPTS),
        description = NAME,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        license = LICENSE,
        url = URL,
        setup_requires = ['py2app'],
        )

if __name__ == '__main__':
    if wx.Platform == '__WXMSW__':
        # Windows
        BuildPy2Exe()
    elif wx.Platform == '__WXMAC__':
        # OSX
        BuildOSXApp()
    else:
        print "Unsupported platform: %s" % wx.Platform
```
**How it works...**
With the previous set-up script, we can build standalone binaries on both Windows and OS X for our FileEditor script.  
So let's take a look at each of the two functions, BuildPy2exe and BuildOSXApp, to see how each of them works.  
  
BuildPy2exe performs the necessary preparations in order to run setup for building a
standalone binary on Windows machines by using py2exe.  
There are three important parts
to take note of in this function. First is the section where we create the manifest.  
Between
versions 2.5 and 2.6, the Windows runtime libraries that were used to build the Python
interpreter binaries changed.  
Due to this, we need to specify different dependencies in
our binary's manifest in order for it to be able to load the correct runtimes and give our
GUI application the correct themed appearance.  
The two possible manifests for either
Python 2.5 or 2.6 are included with this topic's sample source code.  

Second is the py2exe options dictionary.  
This dictionary contains the py2exe specific
options to use when bundling the script.  
We used five options: compressed, optimize,
bundle_files, excludes, and dll_excludes.  
The compressed option states that we
want to compress the resulting .exe file.  
The optimize says to optimize the Python byte
code.  
We can specify 0, 1, or 2 here, for different levels of optimizations. The bundle_files
option specifies the level at which to bundle dependencies into the library.zip file.  
The
lower the number (1-3), the greater the number of files that will be bundled into the ZIP file,
reducing the overall number of individual files that need to be distributed.  
Using 1 can often 
cause problems with wxPython applications, so using 2 or 3 is suggested. Next, the excludes
option is a list of modules to exclude from the resulting bundle.  
We specified Tkinter here
just to ensure that none of its dependencies accidentally get drawn in making our binary
larger.  
Finally, the dll_excludes option was used to work around an issue when using
py2exe with Python 2.6.

Third and finally is the windows parameter in the setup command.  
This is used to specify that we are building a GUI application, and is where we specify the application's icon to
embed into the .exe as well as the manifest that we spoke of earlier.

Running setup with py2exe is as simple as the following command line statement:
```python
python setup.py py2app
```
**There's more...**
Included below is some additional information about some specific distribution dependency issues for Windows applications,  
as well as some references for creating installers for applications on Windows and OS X.

*Py2Exe dependencies*
After running the py2exe setup command, make sure that you review the list of dependencies
that were not included, and that are listed at the end of the output. There are a couple of
additional files that you may need to manually include in your application's dist folder for
it to run properly when deployed on a different computer. For Python 2.5, the msvcr71.dll
and gdiplus.dll files are typically needed. For Python 2.6, the msvcr90.dll and
gdiplus.dll files are needed. The msvcr .dll files are copyrighted by Microsoft, so you
should review the licensing terms to make sure you have the rights to redistribute them. If
not, users may be required to install them separately using the freely-availably redistributable
runtime package that can be downloaded from Microsoft's website.

*Installers*
After building your application with either py2exe or py2app, you will need a way to help the
application's users to properly install the files onto their systems. For Windows, there are a
number of options available for building installers: NSIS (http://nsis.sourceforge.net)
and Inno Setup (http://www.jrsoftware.org/isinfo.php) are two popular free options.
On OS X, the necessary tools are already installed. Simply use the Disk Utility application
to make a disk image (.dmg) file and then copy the built applet into it.

