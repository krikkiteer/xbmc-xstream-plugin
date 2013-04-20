# -*- coding: utf-8 -*-
from resources.lib.gui.contextElement import cContextElement
from resources.lib.config import cConfig
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from ParameterHandler import *

import xbmc
import xbmcgui
import xbmcplugin

import urllib


class cGui:

    def addFolder(self, oGuiElement, oOutputParameterHandler='', bIsFolder=True, iTotal=0):
        sItemUrl = self.__createItemUrl(oGuiElement, oOutputParameterHandler)
        oListItem = self.createListItem(oGuiElement)

        oListItem = self.__createContextMenu(oGuiElement, oListItem, bIsFolder, oOutputParameterHandler)

        sPluginHandle = cPluginHandler().getPluginHandle()
        xbmcplugin.addDirectoryItem(sPluginHandle, sItemUrl, oListItem, isFolder=bIsFolder, totalItems=iTotal)

    def createListItem(self, oGuiElement):
        oListItem = xbmcgui.ListItem(oGuiElement.getTitle(), oGuiElement.getTitleSecond(), oGuiElement.getIcon(), oGuiElement.getThumbnail())
        oListItem.setInfo(oGuiElement.getType(), oGuiElement.getItemValues())

        oListItem.setProperty('fanart_image', oGuiElement.getFanart())
        aProperties = oGuiElement.getItemProperties()
        for sPropertyKey in aProperties.keys():
            oListItem.setProperty(sPropertyKey, aProperties[sPropertyKey])

        return oListItem

    def __createContextMenu(self, oGuiElement, oListItem, bIsFolder, oOutputParams=''):
        sPluginPath = cPluginHandler().getPluginPath()
        aContextMenus = []

        if len(oGuiElement.getContextItems()) > 0:
            for oContextItem in oGuiElement.getContextItems():
                oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = "%s?site=%s&function=%s&%s" % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)
                aContextMenus += [(oContextItem.getTitle(), "XBMC.RunPlugin(%s)" % (sTest,),)]

        oContextItem = cContextElement()
        oContextItem.setTitle("Info")
        aContextMenus += [(oContextItem.getTitle(), "XBMC.Action(Info)",)]
        if not bIsFolder:
            oContextItem.setTitle("add to Playlist")

            aContextMenus += [(oContextItem.getTitle(), "XBMC.Action(Info)",)]
            oContextItem.setTitle("Download")
            aContextMenus += [(oContextItem.getTitle(), "XBMC.Action(Info)",)]
            oContextItem.setTitle("send to JDownloader")
            aContextMenus += [(oContextItem.getTitle(), "XBMC.Action(Info)",)]

        oListItem.addContextMenuItems(aContextMenus)
        return oListItem

    def setEndOfDirectory(self):
        iHandler = cPluginHandler().getPluginHandle()
        xbmcplugin.setPluginCategory(iHandler, "")
        # add some sort methods, these will be present in all views
        xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_SIZE)
        xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_VIDEO_RATING)
        xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_PROGRAM_COUNT)
        xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
        xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_GENRE)

        xbmcplugin.endOfDirectory(iHandler, True)

    def setView(self, content='movies'):
        iHandler = cPluginHandler().getPluginHandle()
        if content == 'movies':
            xbmcplugin.setContent(iHandler, 'movies')
        elif content == 'tvshows':
            xbmcplugin.setContent(iHandler, 'tvshows')
        elif content == 'seasons':
            xbmcplugin.setContent(iHandler, 'seasons')
        elif content == 'episodes':
            xbmcplugin.setContent(iHandler, 'episodes')
        if cConfig().getSetting('auto-view') == 'true':
            xbmc.executebuiltin("Container.SetViewMode(%s)" % cConfig().getSetting(content + '-view'))

    def updateDirectory(self):
        xbmc.executebuiltin("Container.Refresh")

    def __createItemUrl(self, oGuiElement, oOutputParameterHandler=''):
        if (oOutputParameterHandler == ''):
            oOutputParameterHandler = cOutputParameterHandler()

        sParams = oOutputParameterHandler.getParameterAsUri()
        sPluginPath = cPluginHandler().getPluginPath()

        if len(oGuiElement.getFunction()) == 0:
            sItemUrl = "%s?site=%s&title=%s&%s" % (sPluginPath, oGuiElement.getSiteName(), urllib.quote_plus(oGuiElement.getTitle()), sParams)
        else:
            sItemUrl = "%s?site=%s&function=%s&title=%s&%s" % (sPluginPath, oGuiElement.getSiteName(), oGuiElement.getFunction(), urllib.quote_plus(oGuiElement.getTitle()), sParams)
        return sItemUrl

    def showKeyBoard(self, sDefaultText=""):
        # Create the keyboard object and display it modal
        oKeyboard = xbmc.Keyboard(sDefaultText)
        oKeyboard.doModal()

        # If key board is confirmed and there was text entered return the text
        if oKeyboard.isConfirmed():
            sSearchText = oKeyboard.getText()
            if len(sSearchText) > 0:
                return sSearchText

        return False

    def openSettings(self):
        cConfig().showSettingsWindow()

    def showNofication(self, sTitle, iSeconds=0):
        if not cConfig().isDharma():
            return

        if (iSeconds == 0):
            iSeconds = 1000
        else:
            iSeconds = iSeconds * 1000

        xbmc.executebuiltin("Notification(%s,%s,%s)" % (cConfig().getLocalizedString(30308), (cConfig().getLocalizedString(30309) % str(sTitle)), iSeconds))

    def showError(self, sTitle, sDescription, iSeconds=0):
        if iSeconds == 0:
            iSeconds = 1000
        else:
            iSeconds = iSeconds * 1000

        xbmc.executebuiltin("Notification(%s,%s,%s)" % (str(sTitle), (str(sDescription)), iSeconds))

    def showInfo(self, sTitle, sDescription, iSeconds=0):
        if not cConfig().isDharma():
            return

        if (iSeconds == 0):
            iSeconds = 1000
        else:
            iSeconds = iSeconds * 1000

        xbmc.executebuiltin("Notification(%s,%s,%s)" % (str(sTitle), (str(sDescription)), iSeconds))
