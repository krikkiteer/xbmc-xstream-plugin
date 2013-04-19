from resources.lib.util import cUtil
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler

SITE_IDENTIFIER = 'kinokiste_com'
SITE_NAME = 'KinoKiste.com'
SITE_ICON = 'kinokiste.png'

URL_MAIN = 'http://www.kkiste.to'
URL_CINEMA = 'http://www.kkiste.to/aktuelle-kinofilme/'
URL_NEW = 'http://www.kkiste.to/neue-filme/'
URL_BLOCKBUSTER = 'http://www.kkiste.to/blockbuster/'
URL_ALL = 'http://www.kkiste.to/film-index/'

def load():
    oGui = cGui()
    __createMenuEntry(oGui, 'showMovieEntries', 'Aktuelle Kinofilme', URL_CINEMA, 1)
    __createMenuEntry(oGui, 'showMovieEntries', 'Neue Filme', URL_NEW, 1)
    #__createMenuEntry(oGui, 'showMovieEntries', 'Blockbuster', URL_BLOCKBUSTER, 1)
    __createMenuEntry(oGui, 'showCharacters', 'Filme A-Z', URL_ALL)
    __createMenuEntry(oGui, 'showGenre', 'Genre', URL_MAIN)
    __createMenuEntry(oGui, 'showSearch', 'Suche', URL_MAIN)
    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, sUrl, iPage = False):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    if (iPage != False):
        oOutputParameterHandler.addParameter('page', iPage)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = sSearchText.replace(' ', '+')
        oRequestHandler = cRequestHandler(URL_MAIN + '/')
        oRequestHandler.addParameters('q', sSearchText)
        sUrl = oRequestHandler.getRequestUri()
        __showAllMovies(sUrl)
        #__showMovieEntries(sUrl)
        return

    oGui.setEndOfDirectory()

def showMovieEntries():    
    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('siteUrl')
    iPage = oInputParameterHandler.getValue('page')    
    __showMovieEntries(sSiteUrl, iPage)

def __showMovieEntries(sSiteUrl, iPage = False):
    if (iPage != False):
        sUrl = str(sSiteUrl) + '?page='+str(iPage) + '/'
    else:
        sUrl = sSiteUrl

    oGui = cGui()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<a href="([^"]+)" title="Jetzt (.*?) Stream ansehen".*?><img src="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
         for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showHosters')
            sThumbnail = URL_MAIN  + str(aEntry[2])
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

    if (iPage != False):
        bNextPage = __checkForNextSite(sHtmlContent)
        if (bNextPage == True):
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
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]
        sPattern = '<a href="([^"]+)" title="N.*?" class="next">'
                
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)        
        if (aResult[0] == True):
            return True

    return False;

def showCharacters():
    oGui = cGui()
    
    AbisZ = [
    'A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
    'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '1', '2', '3', '4', '5', '6', '7', '8','9'
    ]
    
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
    sHtmlContent = oRequestHandler.request();

    #sPattern = '<div class="boxcontent">(.*?)<div class="boxfooter">'
    #oParser = cParser()
    #aResult = oParser.parse(sHtmlContent, sPattern)
    #if (aResult[0] == True):
        #sHtmlContent = aResult[1][0]

    sPattern = '<a href="([^"]+)" title="Jetzt (.*?) Stream ansehen"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('getHosterUrlandPlay')
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
    sHtmlContent = oRequestHandler.request();

    sPattern = '<div class="needle genre"></div>(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = '<a href="([^"]+)" title=".*?">(.*?)</a></li>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showMovieEntries')
                oGuiElement.setTitle(cUtil().removeHtmlTags(str(aEntry[1])))

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
                oOutputParameterHandler.addParameter('page', 1)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __createInfo(oGui, sHtmlContent):
    sPattern = '<div class="cover"><img src="([^"]+)".*?<div class="excerpt".*?<strong>(.*?)<div class="fix">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle('info (press Info Button)')
            sThumbnail = URL_MAIN  + str(aEntry[0])
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

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    
    oHoster = cHosterHandler().getHoster2('ecostream')
    #oHoster.setFileName(sMovieTitle)
    
    __createInfo(oGui, sHtmlContent)

    sPattern = '<div class="streamlist">(.*?)</script>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = 'onclick="getHost\((\d+)\);">([^<]+)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] == True:
            if len(aResult[1]) > 1:
                for aEntry in aResult[1]:
                    if aEntry[1] != 'ecostream':
                        oGuiElement = cGuiElement()
                        oGuiElement.setSiteName(SITE_IDENTIFIER)
                        oGuiElement.setFunction('getHosterUrlandPlay')
                        oGuiElement.setTitle(str(aEntry[1]))
                        
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', sUrl + '?h=' + str(aEntry[0]))
                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                        oGui.addFolder(oGuiElement, oOutputParameterHandler)
            else:
                __getStream(sUrl + '?h=' + str(aResult[1][0][0]), sMovieTitle)
                return
                        
    oGui.setEndOfDirectory()

def getHosterUrlandPlay():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    __getStream(sUrl, sMovieTitle)

def __getStream(sUrl, sMovieTitle):
    oGui = cGui()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
        
    oHoster = cHosterHandler().getHoster2('ecostream')
    #oHoster.setFileName(sMovieTitle)

    sPattern = '"(http://www.ecostream.tv/stream/[^\?]+)\?'
    aResult = cParser().parse(sHtmlContent, sPattern)             
    if (aResult[0] == True):
        sStreamUrl = aResult[1][0]
        sStreamUrl = str(sStreamUrl).replace('"', '').replace("'", '')
        cHosterGui().showHosterMenuDirect(oGui, oHoster, sStreamUrl, sFileName=sMovieTitle)

    oGui.setEndOfDirectory()
