from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.inputWindow import cInputWindow
from resources.lib import recaptcha
from xbmc import log, LOGERROR
import json
import HTMLParser

SITE_IDENTIFIER = 'serienjunkies_org'
SITE_NAME = 'Serienjunkies.org'
SITE_ICON = 'serienjunkies.jpg'

URL_MAIN = 'http://serienjunkies.org'


def load():
    __showCharacters(URL_MAIN)


def __createMenuEntry(oGui, sFunction, sLabel, lOutputParameter, sThumb=False):
    oOutputParameterHandler = cOutputParameterHandler()

    try:
        for outputParameter in lOutputParameter:
            oOutputParameterHandler.addParameter(outputParameter[0], outputParameter[1])
    except Exception, e:
        log("Can't add parameter to menu entry with label: %s: %s" % (sLabel, e), LOGERROR)
        oOutputParameterHandler = ""

    # Create the gui element
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    if sThumb is not False:
        oGuiElement.setThumbnail(sThumb)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)


def showCharacters():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    __showCharacters(sUrl)


def __showCharacters(sUrl):
    oGui = cGui()

    sHtmlContent = cRequestHandler(sUrl).request()
    sPattern = '<div class="apz_container">(.*?)</div>'
    aResult = cParser().parse(sHtmlContent, sPattern)
    hParser = HTMLParser.HTMLParser()
    if aResult[0]:
        sHtmlContent = aResult[1][0]
        sPattern = '<a class="letter"\s*href="([^"]+)">([^<]+)</a>'
        aResult = cParser().parse(sHtmlContent, sPattern)
        if aResult[0]:
            for sUrl, sTitle in aResult[1]:
                sUrl = hParser.unescape(sUrl.strip())
                if not sUrl.startswith('http'):
                    sUrl = URL_MAIN + sUrl
                sTitle = hParser.unescape(sTitle)

                __createMenuEntry(oGui, 'showSeries', sTitle, [['siteUrl', sUrl]])

    oGui.setEndOfDirectory()


def showSeries():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    __showSeries(sUrl)


def __showSeries(sUrl):
    oGui = cGui()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<ul>(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    hParser = HTMLParser.HTMLParser()
    if aResult[0]:
        sHtmlContent = aResult[1][0]
        sPattern = '<li>\s*<a href="([^"]+)">([^<]+)</a>\s*</li>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            for sUrl, sTitle in aResult[1]:
                sUrl = hParser.unescape(sUrl.strip())
                if not sUrl.startswith('http'):
                    sUrl = URL_MAIN + sUrl
                sTitle = hParser.unescape(sTitle)

                __createMenuEntry(oGui, 'showSeasons', sTitle, [['siteUrl', sUrl]])

    oGui.setEndOfDirectory()


def showSeasons():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    __showSeasons(sUrl)


def __showSeasons(sUrl):
    oGui = cGui()
    oParser = cParser()

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addParameters('', '')
    sHtmlContent = oRequestHandler.request()

    # get Series ID
    sPattern = '{s:seasonNum,ids:\'([^\']+)\'}'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0] is True:
        oGui.showInfo('Info', 'Keine Streams vorhanden', 3)
        return
    sSeriesId = aResult[1][0]
    if sSeriesId.find(',') > -1:
        sSeriesId = sSeriesId.split(',')[1]
    sPattern = '<select id="season_list">(.*?)</select>'
    aResult = cParser().parse(sHtmlContent, sPattern)
    if aResult[0]:
        sSeasons = aResult[1][0]
        sPattern = '<option value="([^"]+)"[^>]*>([^<]+)</option>'
        aResult = cParser().parse(sSeasons, sPattern)
        for aEntry in aResult[1]:
            sSeasonId = aEntry[0]
            sTitle = aEntry[1]

            sUrl = 'http://serienjunkies.org/media/ajax/getStreams.php?s=' + sSeasonId + '&ids=' + sSeriesId

            __createMenuEntry(oGui, 'showEpisodes', sTitle, [['siteUrl', sUrl], ['sSeasonId', sSeasonId]])

    oGui.setEndOfDirectory()


def showEpisodes():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    __showEpisodes(sUrl)


def __showEpisodes(sUrl):
    oGui = cGui()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    hParser = HTMLParser.HTMLParser()
    try:
        data = json.loads(sHtmlContent)
    except:
        data = []

    if data:
        for sId, sTitle, sLanguage, sEpisode, sHosters, sDunno in data:
            sTitle = hParser.unescape(sTitle)
            __createMenuEntry(oGui, 'showHosters', sTitle, [['siteUrl', sUrl], ['sTitle', sTitle], ['sHosters', sHosters]])

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sTitle')
    sHosters = oInputParameterHandler.getValue('sHosters')

    # hosterName:hosterId
    sPattern = "u'(.+?)': u'(.+?)'"
    oParser = cParser()
    aResult = oParser.parse(sHosters, sPattern)
    if aResult[0]:
        for sHoster, sHosterId in aResult[1]:

            sUrl = 'http://crypt2.be/file/' + sHosterId
            sThumbnail = 'http://serienjunkies.org/media/img/stream/'+sHoster+'.png'

            __createMenuEntry(oGui, 'getHosterUrlandPlay', sHoster, [['siteUrl', sUrl], ['sTitle', sTitle]], sThumb=sThumbnail)

    oGui.setEndOfDirectory()


def getHosterUrlandPlay():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sUrl = oRequestHandler.getRealUrl()

    # take care of recaptcha-forms
    while(recaptcha.checkForReCaptcha(sHtmlContent)):
        aCaptchaParams = recaptcha.getCaptcha(sHtmlContent)
        oSolver = cInputWindow(captcha=aCaptchaParams[0])
        userresponse = oSolver.get()
        if not userresponse:
            break
        params = recaptcha.buildResponse(userresponse, aCaptchaParams[1])
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        for param in params.split('&'):
            param = param.split('=')
            oRequestHandler.addParameters(param[0], param[1])
        oRequestHandler.addParameters('submit', 'true')
        sHtmlContent = oRequestHandler.request()

    # if the videolink is in an iframe
    sPattern = '<iframe id="iframe" src="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sStreamUrl = aResult[1][0]
        oHoster = cHosterHandler().getHoster(sStreamUrl)
        cHosterGui().showHosterMenuDirect(oGui, oHoster, sStreamUrl, sFileName=sTitle)
        oGui.setEndOfDirectory()
        return

    # if its in a flash-container
    sPattern = '<param name="movie" value="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sStreamUrl = aResult[1][0]
        oHoster = cHosterHandler().getHoster(sStreamUrl)
        cHosterGui().showHosterMenuDirect(oGui, oHoster, sStreamUrl, sFileName=sTitle)
        oGui.setEndOfDirectory()
        return

    # if its done by simple redirects
    else:
        sStreamUrl = oRequestHandler.getRealUrl()
        oHoster = cHosterHandler().getHoster(sStreamUrl)
        cHosterGui().showHosterMenuDirect(oGui, oHoster, sStreamUrl, sFileName=sTitle)
        oGui.setEndOfDirectory()
