from resources.lib.util import cUtil
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler

# our own ecostream resolver
import urllib2
import urllib
import re


SITE_IDENTIFIER = 'kinokiste_com'
SITE_NAME = 'KinoKiste.com'
SITE_ICON = 'kinokiste.png'

URL_MAIN = 'http://www.kkiste.to'
URL_CINEMA = 'http://www.kkiste.to/aktuelle-kinofilme/'
URL_NEW = 'http://www.kkiste.to/neue-filme/'
URL_BLOCKBUSTER = 'http://www.kkiste.to/blockbuster/'
URL_GENRE = 'http://www.kkiste.to/genres/'
URL_ALL = 'http://www.kkiste.to/film-index/'
URL_SEARCH = 'http://kkiste.to/search/'


def load():
    oGui = cGui()
    __createMenuEntry(oGui, 'showMovieEntries', 'Aktuelle Kinofilme', URL_CINEMA, 1)
    __createMenuEntry(oGui, 'showMovieEntries', 'Neue Filme', URL_NEW, 1)
    __createMenuEntry(oGui, 'showCharacters', 'Filme A-Z', URL_ALL)
    __createMenuEntry(oGui, 'showGenre', 'Genre', URL_GENRE)
    __createMenuEntry(oGui, 'showSearch', 'Suche', URL_MAIN)
    oGui.setEndOfDirectory()


def __createMenuEntry(oGui, sFunction, sLabel, sUrl, iPage=False):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    if iPage:
        oOutputParameterHandler.addParameter('page', iPage)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sSearchText = sSearchText.replace(' ', '+')
        oRequestHandler = cRequestHandler(URL_SEARCH)
        oRequestHandler.addParameters('q', sSearchText)
        sHtmlContent = oRequestHandler.request()

        sPattern = '<li class="mbox list" onclick=".+?"><a href="/(.+?)\.html" title=".+?" class="title">(.+?)</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for sUrl, sTitle in aResult[1]:
                sUrl = '%s/%s.html' % (URL_MAIN, sUrl)
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showHosters')
                oGuiElement.setTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieEntries():
    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('siteUrl')
    __showMovieEntries(sSiteUrl)


def __showMovieEntries(sSiteUrl, iPage=False):
    if iPage:
        sUrl = str(sSiteUrl) + '?page='+str(iPage) + '/'
    else:
        sUrl = sSiteUrl

    oGui = cGui()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)" title="Jetzt (.*?) Stream ansehen".*?><img src="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showHosters')
            sThumbnail = URL_MAIN + str(aEntry[2])
            idx = sThumbnail.find('&')
            if idx > -1:
                sThumbnail = sThumbnail[:idx] + '&w=150&zc=0&a=t'
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setDescription(str(aEntry[1]))
            sTitle = cUtil().removeHtmlTags(str(aEntry[1]))
            oGuiElement.setTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    if iPage:
        bNextPage = __checkForNextSite(sHtmlContent)
        if bNextPage:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showMovieEntries')
            oGuiElement.setTitle('next..')
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sSiteUrl)
            oOutputParameterHandler.addParameter('page', int(iPage) + 1)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextSite(sHtmlContent):
    sPattern = '<div class="pager bottom">(.*?)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHtmlContent = aResult[1][0]
        sPattern = '<a href="([^"]+)" title="N.*?" class="next">'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            return True

    return False


def showCharacters():
    oGui = cGui()

    AbisZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for char in AbisZ:
        __createCharacters(oGui, char)
    oGui.setEndOfDirectory()


def __createCharacters(oGui, sCharacter):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('showAllMovies')
    oGuiElement.setTitle(sCharacter)

    oOutputParameterHandler = cOutputParameterHandler()
    sUrl = URL_ALL + sCharacter + "/"
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)


def showAllMovies():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    __showAllMovies(sUrl)


def __showAllMovies(sUrl):
    oGui = cGui()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)" title="Jetzt (.*?) Stream ansehen"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showHosters')
            sTitle = cUtil().removeHtmlTags(str(aEntry[1]))
            oGuiElement.setTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li><a href="/(.+?)/" title=".+?">(.+?) <span>.+?</span></a><ul>.*?</ul></li>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for gUrl, gTitle in aResult[1]:
            if gUrl not in ['aktuelle-kinofilme']:  # some fuck with the re.. dunno why right now.
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showMovieEntries')
                oGuiElement.setTitle(gTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', '%s/%s/' % (URL_MAIN, gUrl))
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __createInfo(oGui, sHtmlContent):
    sPattern = '<div class="cover"><img src="([^"]+)".*?<div class="excerpt".*?<strong>(.*?)<div class="fix">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle('info (press Info Button)')
            sThumbnail = URL_MAIN + str(aEntry[0])
            idx = sThumbnail.find('&')
            if idx > -1:
                sThumbnail = sThumbnail[:idx]
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setFunction('dummyFolder')
            oGuiElement.setDescription(cUtil().removeHtmlTags(str(aEntry[1])).replace('\t', ''))
            oGui.addFolder(oGuiElement)


def dummyFolder():
    oGui = cGui()
    oGui.setEndOfDirectory()


def __parseMovieLinks(sHtmlContent):
    sPattern = '<li class=".+?"><a href="(.+?)" target="_blank">(.+?) <small>\[(.+?)\]</small></a></li>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        aResult[1].reverse()
        return aResult[1]
    return []


def __addHosterLinks(oGui, movieLinks, sMovieTitle):
    for streamUrl, hosterTitle, part in movieLinks:
        if hosterTitle == 'Ecostream':
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('playEcoStream')
            oGuiElement.setTitle('Ecostream, %s' % part)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sURL', streamUrl)
            oOutputParameterHandler.addParameter('sTitle', sMovieTitle)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)
        else:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('playSupportedHoster')
            oGuiElement.setTitle(hosterTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sURL', streamUrl)
            oOutputParameterHandler.addParameter('sTitle', sMovieTitle)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    """
    list all hosters for a stream
    """
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oGui = cGui()
    __createInfo(oGui, sHtmlContent)
    movieLinks = __parseMovieLinks(sHtmlContent)
    __addHosterLinks(oGui, movieLinks, sMovieTitle)


def playSupportedHoster():
    """
    generic display for any other hoster than ecostream so far..
    we assume the plugins work
    """
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMediaUrl = oInputParameterHandler.getValue('sURL')
    sMovieTitle = oInputParameterHandler.getValue('sTitle')
    oHoster = cHosterHandler().getHoster(sMediaUrl)
    if oHoster:
        cHosterGui().showHosterMenuDirect(oGui, oHoster, sMediaUrl, bGetRedirectUrl=False, sFileName=sMovieTitle)
    oGui.setEndOfDirectory()


def playEcoStream():
    """
    display an ecostream hoster link,
    all it does really is prevent the display menu from resolving the medialink itself
    via urlresolver.resolve, but instead use the provided link directly.
    """
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMediaUrl = oInputParameterHandler.getValue('sURL')
    sMovieTitle = oInputParameterHandler.getValue('sTitle')
    oHoster = cHosterHandler().getHoster(sMediaUrl)
    if oHoster:
        sMediaUrl = __resolveEcoStream(sMediaUrl)
        cHosterGui().showHosterMenuDirect(oGui, oHoster, sMediaUrl, bGetRedirectUrl=False, sFileName=sMovieTitle, noResolve=True)
    oGui.setEndOfDirectory()


def __resolveEcoStream(ecoUrl):
    """
    custom ecostream resolver until urlresolver's ecostream-plugin is fixed
    - currently we are at 2.0.9 and it doesnt work.
    """
    ecoUrl += '?ss=1'
    req = urllib2.Request(ecoUrl)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    eco = urllib2.urlopen(req, urllib.urlencode([('ss', 1), ('sss', 1)]))
    cookie = eco.info().getheader('Set-Cookie')
    cookie = cookie.replace(' path=/', '').strip()
    firstPage = eco.read()
    eco.close()
    match = re.compile("""var t=setTimeout\("lc\('(.+?)','(.+?)','(.+?)','(.+?)'\)",5000\);""").findall(firstPage)
    for a, b, t, key in match:

        url = 'http://www.ecostream.tv/lo/mq.php?s=%s&k=%s&t=%s&key=%s' % (a, b, t, key)
        req = urllib2.Request(url, '')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Referer', ecoUrl)
        req.add_header('Origin', 'http://www.ecostream.tv')
        req.add_header('Cookie', cookie)
        req.add_header("Accept", '*/*')
        req.add_header("Connection", 'keep-alive')
        req.add_header("X-Requested-With", 'XMLHttpRequest')
        eco = urllib2.urlopen(req)
        obj_data = eco.read()
        eco.close()
        match = re.compile('/showmobile/media/(.+?)"').findall(obj_data)
        if match:
            url = match[0]
            urlForRedirect = 'http://www.ecostream.tv/showmobile/media/%s' % (url)
            urlForRedirect = urlForRedirect.replace('%26', '&').replace('%3D', '=').replace('%3F', '?')
            req = urllib2.Request(urlForRedirect)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            req.add_header('Referer', ecoUrl)
            req.add_header('Host', 'www.ecostream.tv')
            req.add_header('Cookie', cookie)
            req.add_header("Accept", '*/*')
            req.add_header("Connection", 'keep-alive')
            eco = urllib2.urlopen(req)
            finalUrl = eco.geturl()
            eco.close()
            return finalUrl

    return False
