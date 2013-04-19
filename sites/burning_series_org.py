# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
import logger
from ParameterHandler import *
from resources.lib.config import cConfig


if cConfig().getSetting('metahandler') == 'true':
    META = True
    try:
        from metahandler import metahandlers
    except:
        META = False
        logger.info("Could not import package 'metahandler'")
else:
    META = False

# Variablen definieren die "global" verwendet werden sollen
SITE_IDENTIFIER = 'burning_series_org'
SITE_NAME = 'Burning-Seri.es'
SITE_ICON = 'burning_series.jpg'

URL_MAIN = 'http://www.burning-seri.es'
URL_SERIES = 'http://www.burning-seri.es/serie-alphabet'
URL_ZUFALL = 'http://www.burning-seri.es/zufall'


def __createMenuEntry(oGui, sFunction, sLabel, lParams, sMetaTitle='', iTotal=0):
    oParams = ParameterHandler()
    #oOutputParameterHandler = cOutputParameterHandler()
    # Create all paramter auf the lOuputParameter
    try:
        for param in lParams:
            oParams.setParam(param[0], param[1])
    except Exception, e:
        logger.error("Can't add parameter to menu entry with label: %s: %s" % (sLabel, e))
        oParams = ""

    # Create the gui element
    oGuiElement = cGuiElement(sLabel, SITE_IDENTIFIER, sFunction)
    if META and sMetaTitle != '':
        oMetaget = metahandlers.MetaData()
        meta = oMetaget.get_meta('tvshow', sMetaTitle)
        oGuiElement.setItemValues(meta)
        oGuiElement.setThumbnail(meta['cover_url'])
        oGuiElement.setFanart(meta['backdrop_url'])
        oParams.setParam('imdbID', meta['imdb_id'])
    oGui.addFolder(oGuiElement, oParams, iTotal=iTotal)


#def showSeries():
def load():
    oGui = cGui()

    sUrl = URL_SERIES
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', 'http://burning-seri.es/')
    sHtmlContent = oRequestHandler.request()

    sPattern = "<ul id='serSeries'>(.*?)</ul>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sHtmlContent = aResult[1][0]

        sPattern = '<li><a href="([^"]+)">(.*?)</a></li>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sTitle = cUtil().unescape(aEntry[1])
                __createMenuEntry(oGui, 'showSeasons', sTitle, [['siteUrl', URL_MAIN + '/' + str(aEntry[0])], ['Title', sTitle]], sTitle, len(aResult[1]))

    oGui.setView('tvshows')
    oGui.setEndOfDirectory()


def showSeasons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('Title')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sImdb = oInputParameterHandler.getValue('imdbID')

    logger.info("%s: show seasons of '%s' " % (SITE_NAME, sTitle))

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', 'http://burning-seri.es/')
    sHtmlContent = oRequestHandler.request()

    sPattern = '<ul class="pages">(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHtmlContent = aResult[1][0]

        sPattern = '[^n]"><a href="([^"]+)">(.*?)</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            seasonNums = []
            for aEntry in aResult[1]:
                seasonNums.append(str(aEntry[1]))
                if META and not sImdb == '':
                    oMetaget = metahandlers.MetaData()
                    meta = oMetaget.get_seasons(sTitle, sImdb, seasonNums)
            ii = 0
            for aEntry in aResult[1]:
                seasonNum = seasonNums[ii]
                oGuiElement = cGuiElement('Staffel ' + seasonNum, SITE_IDENTIFIER, 'showEpisodes')
                if META and not sImdb == '':
                    meta[ii]['TVShowTitle'] = sTitle
                    oGuiElement.setItemValues(meta[ii])
                    oGuiElement.setThumbnail(meta[ii]['cover_url'])
                    oGuiElement.setFanart(meta[ii]['backdrop_url'])
                oParams = ParameterHandler()
                oParams.setParam('siteUrl', URL_MAIN + '/' + str(aEntry[0]))
                oParams.setParam('Title', sTitle)
                oParams.setParam('Season', seasonNum)
                oGui.addFolder(oGuiElement, oParams, iTotal=len(aResult[1]))
                ii += 1
    oGui.setView('seasons')
    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oParams = ParameterHandler()
    sShowTitle = oParams.getValue('Title')
    sUrl = oParams.getValue('siteUrl')
    sImdb = oParams.getValue('imdbID')
    sSeason = oParams.getValue('Season')

    logger.info("%s: show episodes of '%s' season '%s' " % (SITE_NAME, sShowTitle, sSeason))

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<table>(.*?)</table>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHtmlContent = aResult[1][0]
        sPattern = '<td>([^<]+)</td>\s*<td><a href="([^"]+)">(.*?)</a>.*?<td class="nowrap">(\s*<a|\s*</td).*?</tr>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                if aEntry[3].strip() == '</td':
                    continue
                sNumber = str(aEntry[0]).strip()
                oGuiElement = cGuiElement('Episode ' + sNumber, SITE_IDENTIFIER, 'showHosters')
                if META and not sImdb == '':
                    oMetaget = metahandlers.MetaData()
                    meta = oMetaget.get_episode_meta(sShowTitle, sImdb, sSeason, sNumber)
                    meta['TVShowTitle'] = sShowTitle
                    oGuiElement.setItemValues(meta)
                    oGuiElement.setThumbnail(meta['cover_url'])
                    oGuiElement.setFanart(meta['backdrop_url'])

                sPattern = '<strong>(.*?)</strong>'
                aResultTitle = oParser.parse(str(aEntry[2]), sPattern)
                if aResultTitle[0]:
                    sTitleName = str(aResultTitle[1][0]).strip()
                else:
                    sPattern = '<span lang="en">(.*?)</span>'
                    aResultTitle = oParser.parse(str(aEntry[2]), sPattern)
                    if aResultTitle[0]:
                        sTitleName = str(aResultTitle[1][0]).strip()
                    else:
                        sTitleName = ''
                sTitle = sNumber
                sTitleName = cUtil().unescape(sTitleName.decode('utf-8')).encode('utf-8')
                oParams.setParam('EpisodeTitle', sTitleName)
                sTitle = sTitle + ' - ' + sTitleName

                oGuiElement.setTitle(sTitle)
                oParams.setParam('siteUrl', URL_MAIN + '/' + str(aEntry[1]))
                oParams.setParam('EpisodeNr', sNumber)

                oParams.setParam('Title', sShowTitle+' - S'+sSeason+'E'+sTitle)
                oGui.addFolder(oGuiElement, oParams, iTotal=len(aResult[1]))

    oGui.setView('episodes')
    oGui.setEndOfDirectory()


def __createInfo(oGui, sHtmlContent, sTitle):
    sPattern = '<div id="desc_spoiler">([^<]+)</div>.*?<img src="([^"]+)" alt="Cover"/>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sDescription = cUtil().unescape(aEntry[0].decode('utf-8')).encode('utf-8').strip()
            oGuiElement = cGuiElement('info (press Info Button)', SITE_IDENTIFIER, 'dummyFolder')
            oGuiElement.setDescription(sDescription)
            oGuiElement.setThumbnail(URL_MAIN+'/'+aEntry[1])
            oGui.addFolder(oGuiElement)


def dummyFolder():
    return


def showHosters():
    oGui = cGui()

    oParams = ParameterHandler()
    sTitle = oParams.getValue('Title')
    sUrl = oParams.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if not META:
        __createInfo(oGui, sHtmlContent, sTitle)

    sPattern = '<h3>Hoster dieser Episode(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHtmlContent = aResult[1][0]

        sPattern = '<li><a href="([^"]+)">.*?class="icon ([^"]+)"></span> ([^<]+?)</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                oHoster = cHosterHandler().getHoster2('//'+str(aEntry[1]).lower()+'/')
                if oHoster:
                    oGuiElement = cGuiElement(str(aEntry[2]), SITE_IDENTIFIER, 'getHosterUrlandPlay')
                    oParams.setParam('siteUrl', URL_MAIN + '/' + str(aEntry[0]))
                    oParams.setParam('Hoster', oHoster)
                    oGui.addFolder(oGuiElement, oParams, bIsFolder=True)
    oGui.setEndOfDirectory()


def __getMovieTitle(sHtmlContent):
    sPattern = '</ul><h2>(.*?)<small id="titleEnglish" lang="en">(.*?)</small>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            return str(aEntry[0]).strip() + ' - ' + str(aEntry[1]).strip()
    return ''


def getHosterUrlandPlay():
    oGui = cGui()

    oParams = ParameterHandler()
    sTitle = oParams.getValue('Title')
    sUrl = oParams.getValue('siteUrl')
    sHoster = oParams.getValue('Hoster')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div id="video_actions">.*?<a href="([^"]+)" target="_blank">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sStreamUrl = aResult[1][0]
        oHoster = cHosterHandler().getHoster(sHoster)
        cHosterGui().showHosterMenuDirect(oGui, oHoster, sStreamUrl, sFileName=sTitle)
        oGui.setEndOfDirectory()
        return
    oGui.setEndOfDirectory()
