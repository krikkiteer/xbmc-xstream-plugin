# -*- coding: utf-8 -*-
from resources.lib.handler.jdownloaderHandler import cJDownloaderHandler
from resources.lib.download import cDownload
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.player import cPlayer
from resources.lib.handler.requestHandler import cRequestHandler
import urlresolver
import logger


class cHosterGui:

    SITE_NAME = 'cHosterGui'

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(self, oGui, oHoster, sMediaUrl, bGetRedirectUrl=False):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('showHosterMenu')
        oGuiElement.setTitle(oHoster.getDisplayName())

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())

        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    # step 2
    def showHosterMenu(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)
        self.showHosterMenuDirect(oGui, oHoster, sMediaUrl, bGetRedirectUrl)

        oGui.setEndOfDirectory()

    def showHosterMenuDirect(self, oGui, oHoster, sMediaUrl, bGetRedirectUrl=False, sFileName='', noResolve=False):
        # play
        self.__showPlayMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName, noResolve)

        # playlist
        self.__showPlaylistMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName, noResolve)

        # download
        self.__showDownloadMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName, noResolve)

        # JD
        self.__showJDMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName, noResolve)

    def __showPlayMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName='', noResolve=False):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('play')
        oGuiElement.setTitle('play')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', sFileName)
        oOutputParameterHandler.addParameter('noResolve', noResolve)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def __showDownloadMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName='', noResolve=False):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('download')
        oGuiElement.setTitle('download via XBMC')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', sFileName)
        oOutputParameterHandler.addParameter('noResolve', noResolve)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def __showJDMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName='', noResolve=False):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setTitle('an JDownloader senden')
        oGuiElement.setFunction('sendToJDownloader')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('noResolve', noResolve)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def __showPlaylistMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl, sFileName='', noResolve=False):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('addToPlaylist')
        oGuiElement.setTitle('add to playlist')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', sFileName)
        oOutputParameterHandler.addParameter('noResolve', noResolve)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def play(self):
        oInputParameterHandler = cInputParameterHandler()

        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')
        noResolve = oInputParameterHandler.getValue('noResolve')
        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        logger.info('call play: ' + sMediaUrl)

        if noResolve == 'True':
            sLink = sMediaUrl
        else:
            try:
                sLink = urlresolver.resolve(sMediaUrl)
                if sLink is False:
                    cGui().showInfo('Info', 'Dead link')
                    return
            except:
                cGui().showError('Error', 'Cannot resolve URL')
                return

        if sLink is not False:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(sLink)
            oGuiElement.setTitle(sFileName)

            oPlayer = cPlayer()
            oPlayer.clearPlayList()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()
        return

    def addToPlaylist(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        logger.info('call play: ' + sMediaUrl)

        sLink = urlresolver.resolve(sMediaUrl)

        if (sLink is not False):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(sLink)
            oGuiElement.setTitle(sFileName)

            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            oGui.showInfo('Playlist', 'Stream wurde hinzugefügt', 5)
            return
        oGui.showError('Playlist', 'Stream wurde nicht hinzugefügt', 5)
        return False

    def download(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        logger.info('call download: ' + sMediaUrl)

        sLink = urlresolver.resolve(sMediaUrl)
        if sLink is not False:
            oDownload = cDownload()
            oDownload.download(sLink, 'Stream')
            return

        oGui.setEndOfDirectory()

    def sendToJDownloader(self):
        oInputParameterHandler = cInputParameterHandler()

        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        logger.info('call send to JDownloader: ' + sMediaUrl)

        cJDownloaderHandler().sendToJDownloader(sMediaUrl)

    def __getRedirectUrl(self, sUrl):
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()
