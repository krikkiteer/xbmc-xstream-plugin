# -*- coding: utf-8 -*-
from os.path import join
from sys import path
from xbmc import translatePath
import xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.xstream')
__cwd__ = __settings__.getAddonInfo('path')

# Add different library path
path.append(translatePath(join(__cwd__, "resources", "lib")))
path.append(translatePath(join(__cwd__, "resources", "lib", "gui")))
path.append(translatePath(join(__cwd__, "resources", "lib", "handler")))
path.append(translatePath(join(__cwd__, "resources", "art", "sites")))
path.append(translatePath(join(__cwd__, "sites")))

# Run xstream
from xstream import run
run()
