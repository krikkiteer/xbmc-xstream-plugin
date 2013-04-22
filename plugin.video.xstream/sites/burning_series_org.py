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
import HTMLParser


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
URL_GENRE = 'http://www.burning-seri.es/serie-genre'


def __createMenuEntry(oGui, sFunction, sLabel, lParams, sMetaTitle='', iTotal=0):
    oParams = ParameterHandler()
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


def load():
    oGui = cGui()

    oParams = ParameterHandler()
    oGui.addFolder(cGuiElement('Series', SITE_IDENTIFIER, 'showSeries'), oParams)
    oGui.addFolder(cGuiElement('Genres', SITE_IDENTIFIER, 'showGenres'), oParams)
    oGui.setEndOfDirectory()


def showSeries():
    oGui = cGui()

    oRequestHandler = cRequestHandler(URL_SERIES)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
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


def showGenres():
    oGui = cGui()

    oRequestHandler = cRequestHandler(URL_GENRE)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="genre">.+?<span><strong>(.+?)</strong></span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for genreTitle in aResult[1]:
            oParams = ParameterHandler()
            oParams.setParam('sTitle', genreTitle)

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showSeriesForGenre')
            oGuiElement.setTitle(genreTitle)

            oGui.addFolder(oGuiElement, oParams)

    oGui.setEndOfDirectory()


def showSeriesForGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    gTitle = oInputParameterHandler.getValue('sTitle')

    oRequestHandler = cRequestHandler(URL_GENRE)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="genre">.+?<span><strong>%s</strong></span>.+?<ul>(.+?)</div>' % (gTitle)
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sPattern = '<li><a href="(.+?)">(.+?)</a></li>'
        aResult = oParser.parse(aResult[1][0], sPattern)
        if aResult[0]:
            for sUrl, sTitle in aResult[1]:
                sUrl = '%s/%s' % (URL_MAIN, sUrl)
                oParams = ParameterHandler()
                oParams.setParam('sTitle', sTitle)
                oParams.setParam('siteUrl', sUrl)
                oParams.setParam('imdbID', '')

                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showSeasons')
                oGuiElement.setTitle(sTitle)

                oGui.addFolder(oGuiElement, oParams)
    oGui.setEndOfDirectory()


def showSeasons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('Title')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sImdb = oInputParameterHandler.getValue('imdbID')

    logger.info("%s: show seasons of '%s' " % (SITE_NAME, sTitle))

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
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

    oParser = cParser()
    hParser = HTMLParser.HTMLParser()
    sPattern = '<tr>.+?<td>(.+?)</td>.+?<td><a href="(.+?)">.+?<strong>(.+?)</strong>.+?<span lang="(.+?)">(.+?)</span>.+?</a></td>.+?<td class="nowrap">(.+?)</td>.+?</tr>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for sNumber, sUrl, episodeTitle, origLanguage, origLanguageTitle, hosterlinks in aResult[1]:
            sUrl = '%s/%s' % (URL_MAIN, sUrl)
            episodeTitle = hParser.unescape(episodeTitle)
            origLanguageTitle = hParser.unescape(origLanguageTitle)

            oGuiElement = cGuiElement('Episode ' + sNumber, SITE_IDENTIFIER, 'showHosters')
            if META and sImdb:
                oMetaget = metahandlers.MetaData()
                meta = oMetaget.get_episode_meta(sShowTitle, sImdb, sSeason, sNumber)
                meta['TVShowTitle'] = sShowTitle
                oGuiElement.setItemValues(meta)
                oGuiElement.setThumbnail(meta['cover_url'])
                oGuiElement.setFanart(meta['backdrop_url'])

            # how do we detect the language of the episode ?
            # fixed to 'de' for now as most of it seems to be german on burning-seri.es
            sTitle = 's%se%s - %s (%s)' % (sSeason.zfill(2), sNumber.zfill(2), episodeTitle, 'de')
            oGuiElement.setTitle(sTitle)
            oParams.setParam('siteUrl', sUrl)
            oParams.setParam('EpisodeNr', sNumber)
            oParams.setParam('sTitle', sTitle)
            oGui.addFolder(oGuiElement, oParams, iTotal=len(aResult[1]))

    oGui.setView('episodes')
    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()

    oParams = ParameterHandler()
    sUrl = oParams.getValue('siteUrl')
    sTitle = oParams.getValue('sTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<h3>Hoster dieser Episode(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHtmlContent = aResult[1][0]
        sPattern = '<li><a href="(.+?)"><span .+? class="icon (.+?)"></span>.+?</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for sUrl, sHoster in aResult[1]:
                sUrl = '%s/%s' % (URL_MAIN, sUrl)

                oGuiElement = cGuiElement(sHoster, SITE_IDENTIFIER, 'getHosterUrlandPlay')
                oParams.setParam('siteUrl', sUrl)
                oParams.setParam('sTitle', sTitle)
                oGui.addFolder(oGuiElement, oParams, bIsFolder=True)
    oGui.setEndOfDirectory()


def getHosterUrlandPlay():
    oGui = cGui()

    oParams = ParameterHandler()
    sTitle = oParams.getValue('sTitle')
    sUrl = oParams.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div id="video_actions">.*?<a href="([^"]+)" target="_blank">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sStreamUrl = aResult[1][0]
        oHoster = cHosterHandler().getHoster(sStreamUrl)
        cHosterGui().showHosterMenuDirect(oGui, oHoster, sStreamUrl, sFileName=sTitle)
        oGui.setEndOfDirectory()
        return
    oGui.setEndOfDirectory()
