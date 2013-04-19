# -*- coding: utf-8 -*-
import urllib
import logger
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.config import cConfig

from json import loads
import re
from ParameterHandler import *


SITE_IDENTIFIER = 'kinox_to'
SITE_NAME = 'Kinox.to'
SITE_ICON = 'kinox.png'

URL_MAIN = 'http://kinox.to'
URL_CINEMA_PAGE = 'http://kinox.to/Cine-Films.html'
URL_GENRE_PAGE = 'http://kinox.to/Genre.html'
URL_MOVIE_PAGE = 'http://kinox.to/Movies.html'
URL_SERIE_PAGE = 'http://kinox.to/Series.html'
URL_DOCU_PAGE = 'http://kinox.to/Documentations.html'

URL_FAVOURITE_MOVIE_PAGE = 'http://kinox.to/Popular-Movies.html'
URL_FAVOURITE_SERIE_PAGE = 'http://kinox.to/Popular-Series.html'
URL_FAVOURITE_DOCU_PAGE = 'http://kinox.to/Popular-Documentations.html'

URL_LATEST_SERIE_PAGE = 'http://kinox.to/Latest-Series.html'
URL_LATEST_DOCU_PAGE = 'http://kinox.to/Latest-Documentations.html'

URL_SEARCH = 'http://kinox.to/Search.html'
URL_MIRROR = 'http://kinox.to/aGET/Mirror/'
URL_EPISODE_URL = 'http://kinox.to/aGET/MirrorByEpisode/'
URL_AJAX = 'http://kinox.to/aGET/List/'
URL_LANGUAGE = 'http://kinox.to/aSET/PageLang/1'


def load():
    logger.info("Load %s" % SITE_NAME)

    sSecurityValue = __getSecurityCookieValue()
    __initSiteLanguage(sSecurityValue)
    oParams = ParameterHandler()
    oParams.setParam('securityCookie', sSecurityValue)
    ## Create all main menu entries
    oGui = cGui()

    oParams.setParam('siteUrl', URL_MAIN)
    oParams.setParam('page', 1)
    oParams.setParam('mediaType', 'news')
    oGui.addFolder(cGuiElement('Neues von Heute', SITE_IDENTIFIER, 'showNews'), oParams)
    oParams.setParam('siteUrl', URL_MOVIE_PAGE)
    oParams.setParam('mediaType', 'movie')
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showMovieMenu'), oParams)
    oParams.setParam('siteUrl', URL_DOCU_PAGE)
    oParams.setParam('mediaType', 'series')
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showSeriesMenu'), oParams)
    oParams.setParam('siteUrl', URL_SERIE_PAGE)
    oParams.setParam('mediaType', 'documentation')
    oGui.addFolder(cGuiElement('Dokumentationen', SITE_IDENTIFIER, 'showDocuMenu'), oParams)
    oParams.setParam('siteUrl', URL_SEARCH)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'), oParams)
    # __createMenuEntry(oGui, 'showNews', 'Neues von Heute', [['siteUrl', URL_MAIN], ['page', 1],
      # ['mediaType', 'news'], ['securityCookie', sSecurityValue]])
    # __createMenuEntry(oGui, 'showCinemaMovies', 'Aktuelle KinoFilme',
      # [['securityCookie', sSecurityValue]])
    # __createMenuEntry(oGui, 'showCharacters', 'Filme', [['siteUrl', URL_MOVIE_PAGE],
      # ['page', 1], ['mediaType', 'movie'], ['securityCookie', sSecurityValue]])
    # __createMenuEntry(oGui, 'showGenres', 'Genre', [['securityCookie', sSecurityValue]])
    # __createMenuEntry(oGui, 'showCharacters', 'Serien', [['siteUrl', URL_SERIE_PAGE],
      # ['page', 1], ['mediaType', 'series'], ['securityCookie', sSecurityValue]])
    # __createMenuEntry(oGui, 'showCharacters', 'Dokumentationen', [['siteUrl', URL_DOCU_PAGE],
      # ['page', 1], ['mediaType', 'documentation'], ['securityCookie', sSecurityValue]])
    # __createMenuEntry(oGui, 'showFavItems', 'Beliebteste Filme',
      # [['siteUrl', URL_FAVOURITE_MOVIE_PAGE], ['page', 1], ['mediaType', 'movie'],
      # ['securityCookie', sSecurityValue]])
    # __createMenuEntry(oGui, 'showFavItems', 'Beliebteste Serien',
      # [['siteUrl', URL_FAVOURITE_SERIE_PAGE], ['page', 1], ['mediaType', 'series'],
      # ['securityCookie', sSecurityValue]])
    # __createMenuEntry(oGui, 'showFavItems', 'Beliebteste Dokumentationen',
      # [['siteUrl', URL_FAVOURITE_DOCU_PAGE], ['page', 1], ['mediaType', 'documentation'],
      # ['securityCookie', sSecurityValue]])
    # __createMenuEntry(oGui, 'showFavItems', 'Neuste Serien', [['siteUrl', URL_LATEST_SERIE_PAGE],
      # ['page', 1], ['mediaType', 'series'], ['securityCookie', sSecurityValue]])
    # __createMenuEntry(oGui, 'showFavItems', 'Neuste Dokumentationen',
      # [['siteUrl', URL_LATEST_DOCU_PAGE], ['page', 1], ['mediaType', 'documentation'],
      # ['securityCookie', sSecurityValue]])
    # __createMenuEntry(oGui, 'showSearch', 'Suche', [['siteUrl', URL_SEARCH],
      # ['securityCookie', sSecurityValue]])
    oGui.setEndOfDirectory()


######## Allgemeines
def __createMenuEntry(oGui, sFunction, sLabel, lOutputParameter):
    oOutputParameterHandler = cOutputParameterHandler()

    # Create all paramters out of lOuputParameter
    try:
        for outputParameter in lOutputParameter:
            oOutputParameterHandler.addParameter(outputParameter[0], outputParameter[1])
    except Exception, e:
        logger.error("Can't add parameter to menu entry with label: %s: %s" % (sLabel, e))
        oOutputParameterHandler = ""

    # Create the gui element
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)


######## Seitenspezifisch
def showMovieMenu():
    oGui = cGui()
    oParams = ParameterHandler()

    oGui.addFolder(cGuiElement('Kinofilme', SITE_IDENTIFIER, 'showCinemaMovies'), oParams)
    oGui.addFolder(cGuiElement('A-Z', SITE_IDENTIFIER, 'showCharacters'), oParams)
    oGui.addFolder(cGuiElement('Genres', SITE_IDENTIFIER, 'showGenres'), oParams)
    oParams.setParam('siteUrl', URL_FAVOURITE_MOVIE_PAGE)
    oGui.addFolder(cGuiElement('Beliebteste Filme', SITE_IDENTIFIER, 'showFavItems'), oParams)
    oGui.setEndOfDirectory()


def showSeriesMenu():
    oGui = cGui()
    oParams = ParameterHandler()

    oGui.addFolder(cGuiElement('A-Z', SITE_IDENTIFIER, 'showCharacters'), oParams)
    #oGui.addFolder(cGuiElement('Genres',SITE_IDENTIFIER,'showGenres'),oParams)
    oParams.setParam('siteUrl', URL_FAVOURITE_SERIE_PAGE)
    oGui.addFolder(cGuiElement('Beliebteste Serien', SITE_IDENTIFIER, 'showFavItems'), oParams)
    oGui.setEndOfDirectory()


def showDocuMenu():
    oGui = cGui()
    oParams = ParameterHandler()

    oGui.addFolder(cGuiElement('A-Z', SITE_IDENTIFIER, 'showCharacters'), oParams)
    #oGui.addFolder(cGuiElement('Genres',SITE_IDENTIFIER,'showGenres'),oParams)
    oParams.setParam('siteUrl', URL_FAVOURITE_DOCU_PAGE)
    oGui.addFolder(cGuiElement('Beliebteste Dokumentationen', SITE_IDENTIFIER, 'showFavItems'), oParams)
    oParams.setParam('siteUrl', URL_LATEST_DOCU_PAGE)
    oGui.addFolder(cGuiElement('Neuste Dokumentationen', SITE_IDENTIFIER, 'showFavItems'), oParams)
    oGui.setEndOfDirectory()


def __createTitleWithLanguage(sLanguage, sTitle):
    sTitle = cUtil().unescape(sTitle)
    #sTitle = str(sTitle).replace('\\\\','\\')
    if sLanguage == "1":
        return sTitle + " (de)"
    elif sLanguage == "2":
        return sTitle + " (en)"
    elif sLanguage == "7":
        return sTitle + " (tu)"

    return sTitle


def __getHtmlContent(sUrl=None, sSecurityValue=None):
    oInputParameterHandler = cInputParameterHandler()

    # Test if a url is available and set it
    if sUrl is None and not oInputParameterHandler.exist("siteUrl"):
        logger.error("There is no url we can request.")
        return False
    else:
        if sUrl is None:
            sUrl = oInputParameterHandler.getValue("siteUrl")

    # Test is a security value is available
    if sSecurityValue is None:
        if oInputParameterHandler.exist("securityCookie"):
            sSecurityValue = oInputParameterHandler.getValue("securityCookie")
        else:
            sSecurityValue = ""
    # preferred language
    sPrefLang = __getPreferredLanguage()
    # Make the request
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('Cookie', sPrefLang + sSecurityValue + 'ListDisplayYears=Always;')  # ListMode=cover;
    oRequest.addHeaderEntry('Referer', 'http://kinox.to/')
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry('Host', 'kinox.to')

    return oRequest.request()


def __getPreferredLanguage():
    oConfig = cConfig()
    sLanguage = oConfig.getSetting('prefLanguage')
    if sLanguage == '0':
        sPrefLang = 'ListNeededLanguage=25%2C24%2C26%2C2%2C5%2C6%2C7%2C8%2C11%2C15%2C16%2C9%2C12%2C13%2C14%2C17%2C4'
    elif sLanguage == '1':
        sPrefLang = 'ListNeededLanguage=25%2C24%2C26%2C5%2C6%2C7%2C8%2C11%2C15%2C16%2C9%2C12%2C13%2C14%2C17%2C4%2C1'
    else:
        sPrefLang = ''
    return sPrefLang


def __getSecurityCookieValue():
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = "var hash=\[(.*?)\]"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is False:
        logger.error("Can't find script file for cookie")
        return False
    for aEntry in aResult[1][0].split(","):
        sScriptFile = URL_MAIN + str(aEntry).replace("'", "").strip()
        sScriptFile.replace(" ", "")

        logger.info("scriptfile: %s" % sScriptFile)
        oRequestHandler = cRequestHandler(sScriptFile)
        oRequestHandler.addHeaderEntry('Referer', 'http://kinox.to/')
        oRequestHandler.addHeaderEntry('Accept', '*/*')
        oRequestHandler.addHeaderEntry('Host', 'kinox.to')
        sHtmlContent = oRequestHandler.request()

    sPattern = "escape\(hsh \+ \"([^\"]+)\"\)"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        logger.info("No hash value found for the cookie")
        return False

    sHash = aResult[1][0]

    sHash = sHashSnippet + sHash
    sSecurityCookieValue = "sitechrx=" + str(sHash) + ";Path=/"

    oRequestHandler = cRequestHandler(URL_MAIN + "/")
    oRequestHandler.addHeaderEntry("Cookie", sSecurityCookieValue)
    oRequestHandler.request()

    logger.info("Token: %s" % sSecurityCookieValue)

    return sSecurityCookieValue


def __initSiteLanguage(sSecurityValue):
    oRequestHandler = cRequestHandler(URL_LANGUAGE)
    oRequestHandler.addHeaderEntry('COOKIE', sSecurityValue)
    #oRequestHandler.request()


def showSearch():
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue("securityCookie")
    sSearchUrl = oInputParameterHandler.getValue("siteUrl")

    oGui = cGui()
    # Show the keyboard and test if anything was entered
    sSearchText = oGui.showKeyBoard()
    if not sSearchText:
        oGui.setEndOfDirectory()
        return
    # Create the request with the search value
    sFullSearchUrl = sSearchUrl + ("?q=%s" % sSearchText)

    logger.info("Search URL: %s" % sFullSearchUrl)

    sHtmlContent = __getHtmlContent(sFullSearchUrl, sSecurityValue)

    # Display all items returned...
    __displayItems(sHtmlContent)


def __displayItems(sHtmlContent):
    # Test if a cookie was set, else define the default empty one
    sSecurityValue = ""
    oInputParameterHandler = cInputParameterHandler()
    if oInputParameterHandler.exist("securityCookie"):
        sSecurityValue = oInputParameterHandler.getValue("securityCookie")
    # The pattern to filter every item of the list
    sPattern = '<td class="Icon"><img width="16" height="11" src="/gr/sys/lng/(\d+).png" ' + \
        'alt="language"></td>.*?<td class="Title">.*?<a href="([^\"]+)" onclick="return false;">([^<]+)</a>'
    # Parse to get all items of the list
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0]:
        logger.error("Could not find an item")
        return
    # Go throught all items and create a gui element for them.
    oGui = cGui()
    for aEntry in aResult[1]:
        sTitle = __createTitleWithLanguage(aEntry[0], aEntry[2])
        sUrl = URL_MAIN + aEntry[1]
        __createMenuEntry(oGui, 'parseMovieEntrySite', sTitle, [['sUrl', sUrl], ["securityCookie", sSecurityValue]])
    oGui.setEndOfDirectory()


def showFavItems():
    sHtmlContent = __getHtmlContent()
    __displayItems(sHtmlContent)


def showNews():
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCookie')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sPattern = '<div class="Opt leftOpt Headlne"><h1>([a-zA-Z0-9\s.]+)' + \
        '</h1></div>\s*<div class="Opt rightOpt Hint">Insgesamt: (.*?)</div>'

    sHtmlContent = __getHtmlContent(sUrl=sUrl, sSecurityValue=sSecurityValue)
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    oGui = cGui()

    if aResult[0]:
        for aEntry in aResult[1]:
            sTitle = __createTitleWithLanguage('', aEntry[0]) + ' (' + str(aEntry[1]) + ')'
            __createMenuEntry(oGui, 'parseNews', sTitle, [['siteUrl', URL_MAIN], ['page', 1], ['mediaType', 'news'], ['sNewsTitle', aEntry[0]], ['securityCookie', sSecurityValue]])
    oGui.setEndOfDirectory()


def parseNews():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCookie')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sNewsTitle = oInputParameterHandler.getValue('sNewsTitle')

    sPattern = '<div class="Opt leftOpt Headlne"><h1>' + sNewsTitle + \
        '</h1></div>(.*?)<div class="ModuleFooter">'
    sHtmlContent = __getHtmlContent(sUrl=sUrl, sSecurityValue=sSecurityValue)
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    oGui = cGui()

    if not aResult[0]:
        logger.info("Can't get any news")
        oGui.setEndOfDirectory()
        return
    sPattern = '<td class="Icon"><img src="/gr/sys/lng/(\d+).png" alt="language" width="16" ' + \
        'height="11".*?<td class="Title">.*?href="([^\"]+)".*?class="OverlayLabel">([^<]+)' + \
        '(<span class="EpisodeDescr">)?([^><]+)'
    oParser = cParser()
    aResult = oParser.parse(aResult[1][0], sPattern)
    if not aResult[0]:
        logger.info("Can't get any news")
        oGui.setEndOfDirectory()
        return
    # Create an entry for every news line
    for aEntry in aResult[1]:
        #if aEntry[3] != '':
        sTitle = __createTitleWithLanguage(aEntry[0], aEntry[2] + aEntry[4])
        #else:
            #sTitle = __createTitleWithLanguage(aEntry[0], aEntry[2])
        sUrl = aEntry[1]
        # If there are several urls, just pick the first one
        aUrl = sUrl.split(",")
        if len(aUrl) > 0:
            sUrl = aUrl[0]
        __createMenuEntry(oGui, 'parseMovieEntrySite', sTitle, [["sUrl", URL_MAIN + sUrl], ["securityCookie", sSecurityValue]])
    oGui.setEndOfDirectory()


def showCharacters():
    logger.info('load showCharacters')
    sPattern = 'class="LetterMode.*?>([^>]+)</a>'
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCookie')

    if (oInputParameterHandler.exist('siteUrl') and oInputParameterHandler.exist('page') and oInputParameterHandler.exist('mediaType')):
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        iPage = oInputParameterHandler.getValue('page')
        sMediaType = oInputParameterHandler.getValue('mediaType')

        # request
        oRequest = cRequestHandler(siteUrl)
        oRequest.addHeaderEntry('Cookie', sSecurityValue)
        oRequest.addHeaderEntry('Referer', 'http://kinox.to/')
        sHtmlContent = oRequest.request()

        # parse content
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('ajaxCall')
                oGuiElement.setTitle(aEntry)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('character', aEntry[0])
                oOutputParameterHandler.addParameter('page', iPage)
                oOutputParameterHandler.addParameter('mediaType', sMediaType)
                oOutputParameterHandler.addParameter('securityCookie', sSecurityValue)
                if oInputParameterHandler.exist('mediaTypePageId'):
                    sMediaTypePageId = oInputParameterHandler.getValue('mediaTypePageId')
                    oOutputParameterHandler.addParameter('mediaTypePageId', sMediaTypePageId)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    logger.info('load displayGenreSite')
    sPattern = '<td class="Title"><a.*?href="/Genre/([^"]+)">([^<]+)</a>.*?Tipp-([0-9]+).html">'

    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCookie')

    # request
    oRequest = cRequestHandler(URL_GENRE_PAGE)
    oRequest.addHeaderEntry('Cookie', sSecurityValue)
    oRequest.addHeaderEntry('Referer', 'http://kinox.to/')
    sHtmlContent = oRequest.request()
    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    oGui = cGui()
    if aResult[0]:
        for aEntry in aResult[1]:
            iGenreId = aEntry[2]
            __createMenuEntry(oGui, 'showCharacters', aEntry[1], [['page', 1], ['mediaType', 'fGenre'], ['mediaTypePageId', iGenreId], ['securityCookie', sSecurityValue], ['siteUrl', URL_MOVIE_PAGE]])
    oGui.setEndOfDirectory()


def showCinemaMovies():
    logger.info('load displayCinemaSite')
    sPattern = '<div class="Opt leftOpt Headlne"><a title="(.*?)" href="(.*?)">.*?src="(.*?)".*?class="Descriptor">(.*?)</div'

    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCookie')

    oRequest = cRequestHandler(URL_CINEMA_PAGE)
    oRequest.addHeaderEntry('Cookie', sSecurityValue)
    oRequest.addHeaderEntry('Referer', 'http://kinox.to/')
    sHtmlContent = oRequest.request()

    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    oGui = cGui()
    # iterated result and create GuiElements
    if aResult[0]:
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('parseMovieEntrySite')
            oGuiElement.setTitle(aEntry[0])
            oGuiElement.setThumbnail(aEntry[2])
            oGuiElement.setDescription(aEntry[3])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sUrl', URL_MAIN + str(aEntry[1]))
            oOutputParameterHandler.addParameter('securityCookie', sSecurityValue)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)
    oGui.setView('movies')
    oGui.setEndOfDirectory()


def parseMovieEntrySite():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCookie')
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        # get movieEntrySite content
        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('Cookie', sSecurityValue)
        oRequest.addHeaderEntry('Referer', 'http://kinox.to/')
        sHtmlContent = oRequest.request()
        sMovieTitle = __createMovieTitle(sHtmlContent)

        bIsSerie = __isSerie(sHtmlContent)
        if (bIsSerie):
            aSeriesItems = parseSerieSite(sHtmlContent)
            if (len(aSeriesItems) > 0):
                __createInfoItem(oGui, sHtmlContent)
                for aSeriesItem in aSeriesItems:
                    __createMenuEntry(oGui, 'showHosters', aSeriesItem[0], [['sUrl', aSeriesItem[1]], ['sMovieTitle', sMovieTitle], ['securityCookie', sSecurityValue]])
        else:
            __createInfoItem(oGui, sHtmlContent)
            showHosters(sHtmlContent, sMovieTitle)
    oGui.setEndOfDirectory()


def __createMovieTitle(sHtmlContent):
    sPattern = '<h1><span style="display: inline-block">(.*?)</h1>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sTitle = cUtil().removeHtmlTags(str(aResult[1][0]))
        return sTitle
    return False


def __createInfoItem(oGui, sHtmlContent):
    sThumbnail = __getThumbnail(sHtmlContent)
    sDescription = __getDescription(sHtmlContent)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setTitle('info (press Info Button)')
    oGuiElement.setThumbnail(sThumbnail)
    oGuiElement.setFunction('dummyFolder')
    oGuiElement.setDescription(sDescription)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
    oOutputParameterHandler.addParameter('sDescription', sDescription)

    oGui.addFolder(oGuiElement, oOutputParameterHandler)


def dummyFolder():
    oGui = cGui()
    oGui.setEndOfDirectory()


def showHosters(sHtmlContent='', sTitle=False):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCookie')
    if sTitle:
        sTitle = oInputParameterHandler.getValue('sTitle')

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('Cookie', sSecurityValue)
    oRequest.addHeaderEntry('Referer', 'http://kinox.to/')
    sHtmlContent = oRequest.request()
    sPattern = '<li id="Hoster.*?rel="([^"]+)".*?<div class="Named">(.*?)</div>(.*?)</div></li>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        for aEntry in aResult[1]:
            sHoster = aEntry[1]
            oHoster = cHosterHandler().getHoster2(sHoster.lower())
            if oHoster:
                # check for additional mirrors
                sPattern = '<b>Mirror</b>: [1-9]/([1-9])<br />'
                oParser = cParser()
                aResult = oParser.parse(aEntry[2], sPattern)
                mirrors = 1
                if (aResult[0]):
                    mirrors = int(aResult[1][0])
                for i in range(1, mirrors + 1):
                    sUrl = URL_MIRROR + urllib.unquote_plus(aEntry[0])
                    mirrorName = ""
                    if (mirrors > 1):
                        mirrorName = "  Mirror " + str(i)
                        sUrl = re.sub(r'Mirror=[1-9]', 'Mirror=' + str(i), sUrl)
                    __createMenuEntry(oGui, 'getHosterUrlandPlay', sHoster+mirrorName, [['siteUrl', sUrl], ['sTitle', sTitle], ['securityCookie', sSecurityValue]])
    oGui.setEndOfDirectory()


def parseSerieSite(sHtmlContent):
    aSeriesItems = []

    sPattern = 'id="SeasonSelection" rel="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        aSeriesUrls = aResult[1][0].split("&amp;")
        sSeriesUrl = '&' + str(aSeriesUrls[0]) + '&' + str(aSeriesUrls[1])

        sPattern = '<option.*?rel="([^"]+)".*?>Staffel ([^<]+)</option'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                aSeriesIds = aEntry[0].split(",")
                for iSeriesIds in aSeriesIds:
                    aSeries = []
                    iSeriesId = iSeriesIds
                    iSeasonId = aEntry[1]

                    sTitel = 'Staffel ' + str(iSeasonId) + ' - ' + str(iSeriesId)
                    sUrl = URL_EPISODE_URL + sSeriesUrl + '&Season=' + str(iSeasonId) + '&Episode=' + str(iSeriesId)

                    aSeries.append(sTitel)
                    aSeries.append(sUrl)
                    aSeriesItems.append(aSeries)

    return aSeriesItems


def __isSerie(sHtmlContent):
    sPattern = 'id="SeasonSelection" rel="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        return True
    return False


def parseHosterSnippet():
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCookie')

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('hosterName') and oInputParameterHandler.exist('hosterUrlSite') and oInputParameterHandler.exist('hosterParserMethode') and oInputParameterHandler.exist('hosterFileName')):
        sHosterName = oInputParameterHandler.getValue('hosterName')
        sHosterUrlSite = oInputParameterHandler.getValue('hosterUrlSite')
        sHosterParserMethode = oInputParameterHandler.getValue('hosterParserMethode')
        sHosterFileName = oInputParameterHandler.getValue('hosterFileName')
        sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
        if sHosterName == 'videozer.com' or sHosterName == 'videobb.com':
            sPattern = '<param name=\\\\"movie\\\\" value=\\\\"(.*?)\\\\"'
            __parseHosterDefault(sHosterUrlSite, sHosterName, sHosterFileName, sPattern, sSecurityValue, sMovieTitle)
        elif sHosterName == 'megavideo.com':
            sPattern = '<param value=\\\\"(.*?)\\\\" name=\\\\"movie\\\\"'
            __parseHosterDefault(sHosterUrlSite, sHosterName, sHosterFileName, sPattern, sSecurityValue, sMovieTitle)
        elif (sHosterParserMethode == 'parseHosterDefault'):
            __parseHosterDefault(sHosterUrlSite, sHosterName, sHosterFileName, False, sSecurityValue, sMovieTitle)


def ajaxCall():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCookie')

    if (oInputParameterHandler.exist('page') and oInputParameterHandler.exist('mediaType')):
        iPage = oInputParameterHandler.getValue('page')
        sMediaType = oInputParameterHandler.getValue('mediaType')
    iMediaTypePageId = False
    if (oInputParameterHandler.exist('mediaTypePageId')):
        iMediaTypePageId = oInputParameterHandler.getValue('mediaTypePageId')
    sCharacter = 'A'
    if (oInputParameterHandler.exist('character')):
        sCharacter = oInputParameterHandler.getValue('character')

    logger.info('MediaType: ' + sMediaType + ' , Page: ' + str(iPage) + ' , iMediaTypePageId: ' + str(iMediaTypePageId) + ' , sCharacter: ' + str(sCharacter))

    sAjaxUrl = __createAjaxUrl(sMediaType, iPage, iMediaTypePageId, sCharacter)
    logger.info(sAjaxUrl)

    sHtmlContent = __getHtmlContent(sUrl=sAjaxUrl)
    aData = loads(sHtmlContent)['aaData']

    for aEntry in aData:
        sPattern = '<a href="([^"]+)".*?onclick="return false;">([^<]+)'
        oParser = cParser()
        aResult = oParser.parse(aEntry[2], sPattern)
        if aResult[0]:
            sTitle = __createTitleWithLanguage(aEntry[0], aResult[1][0][1]).encode('utf-8')
        sUrl = URL_MAIN + str(aResult[1][0][0])
        sUrl = sUrl.replace('\\', '')
        __createMenuEntry(oGui, 'parseMovieEntrySite', sTitle, [['sUrl', sUrl], ["securityCookie", sSecurityValue]])

    # check for next site
    sPattern = '"iTotalDisplayRecords":"([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            iTotalCount = aEntry[0]
            iNextPage = int(iPage) + 1
            iCurrentDisplayStart = __createDisplayStart(iNextPage)
            if (iCurrentDisplayStart < iTotalCount):
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('ajaxCall')
                oGuiElement.setTitle('next ..')

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('page', iNextPage)
                oOutputParameterHandler.addParameter('character', sCharacter)
                oOutputParameterHandler.addParameter('mediaType', sMediaType)
                oOutputParameterHandler.addParameter('securityCookie', sSecurityValue)
            if iMediaTypePageId:
                oOutputParameterHandler.addParameter('mediaTypePageId', iMediaTypePageId)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)
    oGui.setView('movies')
    oGui.setEndOfDirectory()


def __createDisplayStart(iPage):
    return (25 * int(iPage)) - 25


def __createAjaxUrl(sMediaType, iPage, iMediaTypePageId, sCharacter='A'):
    iDisplayStart = __createDisplayStart(iPage)

    oRequestHandler = cRequestHandler(URL_AJAX)
    if not iMediaTypePageId:
        oRequestHandler.addParameters('additional', '{"fType":"' + str(sMediaType) + '","fLetter":"' + str(sCharacter) + '"}')
    else:
        oRequestHandler.addParameters('additional', '{"foo":"bar","' + str(sMediaType) + '":"' + iMediaTypePageId + '","fType":"movie","fLetter":"' + str(sCharacter) + '"}')

    oRequestHandler.addParameters('bSortable_0', 'true')
    oRequestHandler.addParameters('bSortable_1', 'true')
    oRequestHandler.addParameters('bSortable_2', 'true')
    oRequestHandler.addParameters('bSortable_3', 'false')
    oRequestHandler.addParameters('bSortable_4', 'false')
    oRequestHandler.addParameters('bSortable_5', 'false')
    oRequestHandler.addParameters('bSortable_6', 'true')
    oRequestHandler.addParameters('iColumns', '7')
    oRequestHandler.addParameters('iDisplayLength', '25')
    oRequestHandler.addParameters('iDisplayStart', iDisplayStart)
    oRequestHandler.addParameters('iSortCol_0', '2')
    oRequestHandler.addParameters('iSortingCols', '1')
    oRequestHandler.addParameters('sColumns', '')
    oRequestHandler.addParameters('sEcho', iPage)
    oRequestHandler.addParameters('sSortDir_0', 'asc')
    #oRequestHandler.addParameters('ListMode', 'cover')
    return oRequestHandler.getRequestUri()


def getHosterUrlandPlay():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    #sHoster = oInputParameterHandler.getValue('hosterName')
    sSecurityValue = oInputParameterHandler.getValue('securityCookie')
    sTitle = oInputParameterHandler.getValue('sTitle')

    sUrl = sUrl.replace('&amp;', '&')
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('Cookie', sSecurityValue)
    oRequest.addHeaderEntry('Referer', 'http://kinox.to/')
    sHtmlContent = oRequest.request()
    #pattern for stream url
    sPattern = '<a rel=\\\\"(.*?)\\\\"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        aMovieParts = aResult[1]
        if (len(aMovieParts) > 1):
            iCounter = 0
            for sPartUrl in aMovieParts:
                #sPartUrl = sPartUrl.replace('\\/', '/')
                iCounter = iCounter + 1

                #oHoster = cHosterHandler().getHoster2(sPartUrl)
                #if (oHoster != False):
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('multiPartMovie')
                oGuiElement.setTitle("Part "+str(iCounter))
                #oGuiElement.setThumbnail(sThumbnail)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', URL_MIRROR + sPartUrl)
                oOutputParameterHandler.addParameter('sTitle', sTitle + " Part " + str(iCounter))
                oOutputParameterHandler.addParameter('securityCookie', sSecurityValue)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    else:
        #pattern for stream url
        sPattern = '<a\shref=\\\\"(.*?)\\\\"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            aMovieParts = aResult[1]
            sPartUrl = aMovieParts[0].replace('\\/', '/')
            oHoster = cHosterHandler().getHoster2(sPartUrl)
            cHosterGui().showHosterMenuDirect(oGui, oHoster, sPartUrl, sFileName=sTitle)
    oGui.setEndOfDirectory()


def multiPartMovie():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('sUrl')
    sTitle = oInputParameterHandler.getValue('sTitle')
    sSecurityValue = oInputParameterHandler.getValue('securityCookie')

    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('Cookie', sSecurityValue)
    oRequest.addHeaderEntry('Referer', 'http://kinox.to/')
    sHtmlContent = oRequest.request()

    #pattern for single part
    sPattern = '<a\shref=\\\\"(.*?)\\\\"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        aMovieParts = aResult[1]
        sPartUrl = aMovieParts[0].replace('\\/', '/')
        oHoster = cHosterHandler().getHoster2(sPartUrl)
    cHosterGui().showHosterMenuDirect(oGui, oHoster, sPartUrl, sFileName=sTitle)
    oGui.setEndOfDirectory()


def __getDescription(sHtmlContent):
    sRegex = '<div class="Descriptore">([^<]+)<'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sRegex, 1)
    if aResult[0]:
        return aResult[1][0]
    return ''


def __getThumbnail(sHtmlContent):
    sRegex = '<div class="Grahpics">.*? src="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sRegex)
    if aResult[0]:
        return aResult[1][0]
    return ''


def __getDetails(sHtmlContent):
    sRegex = '<li class="DetailDat" title="Director"><span class="Director"></span>(.*?)</li><li class="DetailDat" title="Country"><span class="Country"></span>(.*?)</li><li class="DetailDat" title="Runtime"><span class="Runtime"></span>(.*?)</li><li class="DetailDat" title="Genre"><span class="Genre"></span>(.*?)</li><li class="DetailDat" title="Views"><span class="Views"></span>(.*?)</li>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sRegex)

    aDetails = {}

    if aResult[0]:
        aDetails['writer'] = aResult[1][0][0]
        aDetails['country'] = aResult[1][0][1]
        aDetails['duration'] = aResult[1][0][2]
        aDetails['genre'] = aResult[1][0][3]
        aDetails['playcount'] = oParser.getNumberFromString(aResult[1][0][4])

    return aDetails
