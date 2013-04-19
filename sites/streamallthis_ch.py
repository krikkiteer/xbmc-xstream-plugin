# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.hoster import cHosterGui
from ParameterHandler import *
import logger
import re
import os.path
import time

SITE_IDENTIFIER = 'streamallthis_ch'
SITE_NAME = 'streamallthis.ch'
SITE_ICON = 'streamallthis.png'

URL_REFERER = 'http://streamallthis.ch'
URL_MAIN = 'http://streamallthis.ch/'
URL_SERIES = 'http://streamallthis.ch/tv-shows-list.html'
URL_LASTEPISODES = str(URL_MAIN)
CACHE_FILE_SERIES = '/tmp/streamallthis_ch_shows'
CACHE_TIME_SERIES = 3600*6  # cache for 6 hours by default..
CACHE_FILE_LASTEPISODES = '/tmp/streamallthis_ch_lastepisodes'
CACHE_TIME_LASTEPISODES = 3600*2  # cache for 2 hours by default..


def load():
    oGui = cGui()

    oParams = ParameterHandler()
    oParams.setParam('siteUrl', URL_SERIES)
    oGui.addFolder(cGuiElement('All Shows', SITE_IDENTIFIER, 'showSeries'), oParams)
    oGui.addFolder(cGuiElement('A-Z', SITE_IDENTIFIER, 'showCharacters'), oParams)
    oGui.addFolder(cGuiElement('Last Episodes', SITE_IDENTIFIER, 'showLastEpisodes'), oParams)
    oGui.addFolder(cGuiElement('Search', SITE_IDENTIFIER, 'showSearch'), oParams)

    oGui.setEndOfDirectory()


def __getSeries(siteUrl=None):
    refetch = True
    if os.path.exists(CACHE_FILE_SERIES):
        ctime = os.path.getctime(CACHE_FILE_SERIES)
        if time.time() - ctime < CACHE_TIME_SERIES:
            logger.info('reading shows from cache')
            f = file(CACHE_FILE_SERIES)
            sHtmlContent = f.read()
            f.close()
            refetch = False

    if refetch:
        logger.info('getting shows from website')
        if siteUrl is None:
            siteUrl = URL_SERIES
        # request
        oRequest = cRequestHandler(siteUrl)
        oRequest.addHeaderEntry('Referer', URL_REFERER)
        sHtmlContent = oRequest.request()
        f = file(CACHE_FILE_SERIES, 'wb')
        f.write(sHtmlContent)
        f.close()

    # parse content and sort it
    sorting = []
    sPattern = 'href="/watch/(.+?)" class="lc"> (.+?) </a>'
    match = re.compile(sPattern).findall(sHtmlContent)
    for sURL, sTitle in match:
        sURL = '%s/watch/%s' % (URL_MAIN, sURL)
        sorting.append((sURL, sTitle))
    sorting.sort(sortBy2nd)

    return sorting


def __listSeries(series=[]):
    oGui = cGui()
    for sURL, sTitle in series:
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showEpisodes')
        oGuiElement.setTitle(sTitle)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sURL', sURL)
        oOutputParameterHandler.addParameter('sTitle', sTitle)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)
    oGui.setEndOfDirectory()


def sortBy2nd(a, b):
    return cmp(a[1], b[1])


def showLastEpisodes():
    refetch = True
    if os.path.exists(CACHE_FILE_LASTEPISODES):
        ctime = os.path.getctime(CACHE_FILE_LASTEPISODES)
        if time.time() - ctime < CACHE_TIME_LASTEPISODES:
            logger.info('reading last episodes from cache')
            f = file(CACHE_FILE_LASTEPISODES)
            sHtmlContent = f.read()
            f.close()
            refetch = False

    if refetch:
        logger.info('getting last episodes from website')

        # request
        oRequest = cRequestHandler(URL_LASTEPISODES)
        oRequest.addHeaderEntry('Referer', URL_REFERER)
        sHtmlContent = oRequest.request()
        f = file(CACHE_FILE_LASTEPISODES, 'wb')
        f.write(sHtmlContent)
        f.close()

    # parse content and sort it
    episodes = []
    sPattern = '<tr class="fc">.*?<td>.*?</td>.*?<td>.*?<a href="/watch/(.*?)" class="lc">(.*?)</a>.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?</tr>'
    match = re.compile(sPattern).findall(sHtmlContent)
    for sURL, sTitle, sSeason, sEpisode in match:
        sSeason = sSeason.strip().replace('&nbsp;', '').zfill(2)
        sEpisode = sEpisode.strip().replace('&nbsp;', '').zfill(2)
        sTitle = sTitle.strip()
        sURL = '%s/watch/%s/s%se%s.html' % (URL_MAIN, sURL, sSeason, sEpisode)
        sTitle = '%s - s%se%s' % (sTitle, sSeason, sEpisode)
        episodes.append((sURL, sTitle))
    episodes.sort(sortBy2nd)
    __listEpisodes(episodes)


def showCharacters():
    oGui = cGui()
    for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showCharacter')
        oGuiElement.setTitle(char)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sChar', char)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showCharacter():
    oInputParameterHandler = cInputParameterHandler()
    sChar = oInputParameterHandler.getValue('sChar')
    series = [s for s in __getSeries() if s[1][0].lower() == sChar.lower()]
    __listSeries(series)


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        series = [x for x in __getSeries() if x[1].lower().find(sSearchText.lower()) != -1]
        __listSeries(series)


def showSeries():
    __listSeries(__getSeries())


def __listEpisodes(episodes):
    oGui = cGui()
    for sURL, sTitle in episodes:
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('playEpisode')
        oGuiElement.setTitle(sTitle)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sURL', sURL)
        oOutputParameterHandler.addParameter('sTitle', sTitle)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    logger.info('showEpisodes()')
    sPattern = '<tr class="fc">.*?<td>.*?</td>.*?<td>(.+?)</td>.*?<td>(.+?)</td>.*?<td>.*?<a href="(.+?)" class="la">WATCH</a>.*?</td>.*?</tr>'
    oInputParameterHandler = cInputParameterHandler()

    siteUrl = oInputParameterHandler.getValue('sURL')
    oRequest = cRequestHandler(siteUrl)
    oRequest.addHeaderEntry('Referer', URL_REFERER)
    sHtmlContent = oRequest.request()

    episodes = []
    # parse content and sort it
    sHtmlContent.replace('\n', '').replace('\t', '')
    match = re.compile(sPattern).findall(sHtmlContent)
    for season, episode, url in match:
        season = season.strip().replace('&nbsp;', '')
        episode = episode.strip().replace('&nbsp;', '')
        sTitle = 's%se%s' % (season.zfill(2), episode.zfill(2))
        sURL = '%s%s' % (URL_MAIN, url)
        episodes.append((sURL, sTitle))
    episodes.sort(sortBy2nd)

    __listEpisodes(episodes)


def playEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sURL = oInputParameterHandler.getValue('sURL')
    sTitle = oInputParameterHandler.getValue('sTitle')

    oRequest = cRequestHandler(sURL)
    oRequest.addHeaderEntry('Referer', URL_REFERER)
    sHtmlContent = oRequest.request()

    sFileName = re.compile('<iframe src="http://www.putlocker.com/embed/(.+?)"').findall(sHtmlContent)[0]
    sUrl = 'http://www.putlocker.com/embed/%s' % sFileName
    oHoster = cHosterHandler().getHoster(sUrl)
    if oHoster is not False:
        cHosterGui().showHosterMenuDirect(oGui, oHoster, sUrl, bGetRedirectUrl=False, sFileName=sTitle)

    oGui.setEndOfDirectory()
