# -*- coding: utf-8 -*-
from resources.lib.util import cUtil
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.config import cConfig
import logger

SITE_IDENTIFIER = 'gstream_in'
SITE_NAME = 'G-Stream.in'
SITE_ICON = 'gstream.png'

URL_MAIN = 'http://g-stream.in'
URL_SHOW_MOVIE = 'http://g-stream.in/showthread.php?t='
URL_CATEGORIES = 'http://g-stream.in/forumdisplay.php?f='
URL_HOSTER = 'http://g-stream.in/secure/'
URL_SEARCH = 'http://g-stream.in/search.php'

def load():
    oGui = cGui()

    sSecurityValue = __getSecurityCookieValue()

    __createMainMenuEntry(oGui, 'Aktuelle KinoFilme', 542, sSecurityValue)
    __createMainMenuEntry(oGui, 'Action', 591, sSecurityValue)
    __createMainMenuEntry(oGui, 'Horror', 593, sSecurityValue)
    __createMainMenuEntry(oGui, 'Komoedie', 592, sSecurityValue)
    __createMainMenuEntry(oGui, 'Thriller', 595, sSecurityValue)
    __createMainMenuEntry(oGui, 'Drama', 594, sSecurityValue)
    __createMainMenuEntry(oGui, 'Fantasy', 655, sSecurityValue)
    __createMainMenuEntry(oGui, 'Abenteuer', 596, sSecurityValue)
    __createMainMenuEntry(oGui, 'Animation', 677, sSecurityValue)
    __createMainMenuEntry(oGui, 'Dokumentation', 751, sSecurityValue)
    #__createMainMenuEntry(oGui, 'Serien', 543, sSecurityValue)
  
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('displaySearch')
    oGuiElement.setTitle('Suche Filme')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('securityCookie', sSecurityValue)
    oOutputParameterHandler.addParameter('searchType', '528')
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
    # Serien parsing nicht implementiert
    #oGuiElement = cGuiElement()
    #oGuiElement.setSiteName(SITE_IDENTIFIER)
    #oGuiElement.setFunction('displaySearch')
    #oGuiElement.setTitle('Suche Serien')
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('securityCookie', sSecurityValue)
    #oOutputParameterHandler.addParameter('searchType', '532')
    #oGui.addFolder(oGuiElement, oOutputParameterHandler)
    if showAdult():
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showXXX')
        oGuiElement.setTitle('XXX')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('securityCookie', sSecurityValue)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def __createMainMenuEntry(oGui, sMenuName, iCategoryId, sSecurityValue):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setTitle(sMenuName)
    oGuiElement.setFunction('parseMovieResultSite')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('normalySiteUrl', URL_CATEGORIES + str(iCategoryId) + '&order=desc&page=')
    oOutputParameterHandler.addParameter('siteUrl', URL_CATEGORIES + str(iCategoryId) + '&order=desc&page=1')
    oOutputParameterHandler.addParameter('iPage', 1)
    oOutputParameterHandler.addParameter('securityCookie', sSecurityValue)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
    
def __getSecurityCookieValue():
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = "<HTML><HEAD><SCRIPT language=\"javascript\" src=\"([^\"]+)\">"+\
    "</SCRIPT></HEAD><BODY onload=\"scf\('(.*?)'\+'(.*?)','/'\);\"></BODY></HTML>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] == False:
        return ''
    sScriptFile = URL_MAIN + str(aResult[1][0][0])
    sHashSnippet = str(aResult[1][0][1])+str(aResult[1][0][2])

    oRequestHandler = cRequestHandler(sScriptFile)
    oRequestHandler.addHeaderEntry('Referer', 'http://g-stream.in/')
    sHtmlContent = oRequestHandler.request()

    sPattern = "escape\(hsh \+ \"([^\"]+)\"\)"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    sHash = aResult[1][0]
    sHash = sHashSnippet + sHash
    sSecurityCookieValue = 'sitechrx=' + str(sHash)
    logger.info('Token: '+sSecurityCookieValue)
    return sSecurityCookieValue 

def __getHtmlContent(sUrl = None, sSecurityValue=None):
    oInputParameterHandler = cInputParameterHandler()

    # Test if a url is available and set it
    if sUrl is None and not oInputParameterHandler.exist('siteUrl'):
        logger.info("There is no url we can request.")
        return False
    else:
        if sUrl is None:
            sUrl = oInputParameterHandler.getValue('siteUrl')

    # Test if a security value is available
    if sSecurityValue is None:
        if oInputParameterHandler.exist('securityCookie'):
            sSecurityValue = oInputParameterHandler.getValue('securityCookie')
        else :
            sSecurityValue = ''

    # Make the request
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('Cookie', sSecurityValue)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry('Host', 'g-stream.in')

    return oRequest.request()
    
def showXXX():
    oInputParameterHandler = cInputParameterHandler()
    sSecurityValue = oInputParameterHandler.getValue('securityCookie')
    oGui = cGui()
    __createMainMenuEntry(oGui, 'Alle Pornos', 661, sSecurityValue)
    #__createMainMenuEntry(oGui, 'Clips', 669, sSecurityValue) #im Moment können keine Clips abgespielt werden da die Cliphoster nicht aufgelöst werden können
    
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('displaySearch')
    oGuiElement.setTitle('Suche XXX Streams')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('securityCookie', sSecurityValue)
    oOutputParameterHandler.addParameter('searchType', '530')
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
    
    __createMainMenuEntry(oGui, 'Amateure', '661&prefixid=Amateure1', sSecurityValue)
    __createMainMenuEntry(oGui, 'Anal', '661&prefixid=Anal', sSecurityValue)
    __createMainMenuEntry(oGui, 'Asia', '661&prefixid=Asia', sSecurityValue)
    __createMainMenuEntry(oGui, 'Black', '661&prefixid=Ebony', sSecurityValue)
    __createMainMenuEntry(oGui, 'Blowjob', '661&prefixid=Blowjob', sSecurityValue)
    __createMainMenuEntry(oGui, 'Deutsch', '661&prefixid=Deutsch', sSecurityValue)
    __createMainMenuEntry(oGui, 'Fetish', '661&prefixid=Fetish', sSecurityValue)
    __createMainMenuEntry(oGui, 'Große Brüste', '661&prefixid=GrosseBrueste', sSecurityValue)
    __createMainMenuEntry(oGui, 'Gruppensex', '661&prefixid=Gruppensex', sSecurityValue)
    __createMainMenuEntry(oGui, 'Gay', '661&prefixid=Gay', sSecurityValue)
    __createMainMenuEntry(oGui, 'Hardcore', '661&prefixid=Hardcore', sSecurityValue)
    __createMainMenuEntry(oGui, 'International', '661&prefixid=International', sSecurityValue)
    __createMainMenuEntry(oGui, 'Lesben', '661&prefixid=Lesben', sSecurityValue)
    __createMainMenuEntry(oGui, 'Masturbation', '661&prefixid=Masturbation', sSecurityValue)
    __createMainMenuEntry(oGui, 'Teens', '661&prefixid=Teens', sSecurityValue)
    oGui.setEndOfDirectory()    

def displaySearch():
    oGui = cGui()
    
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        __search(sSearchText)
    return
    oGui.setEndOfDirectory()

def __search(sSearchText):
    oInputParameterHandler = cInputParameterHandler()
    sSearchType = oInputParameterHandler.getValue('searchType')
    sUrl = URL_SEARCH+'?do=process&childforums=1&do=process&exactname=1&forumchoice[]='+sSearchType+\
    '&query=' + str(sSearchText) + '&quicksearch=1&s=&securitytoken=guest&titleonly=1'
    
    oRequest = cRequestHandler(sUrl)
    sUrl = oRequest.getHeaderLocationUrl()
    __parseMovieResultSite(sUrl, sUrl, 1)

def parseMovieResultSite():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('siteUrl')):
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        normalySiteUrl = oInputParameterHandler.getValue('normalySiteUrl')
        iPage = oInputParameterHandler.getValue('iPage')
        __parseMovieResultSite(siteUrl, normalySiteUrl, iPage)


def __parseMovieResultSite(siteUrl, normalySiteUrl, iPage):
    oInputParameterHandler = cInputParameterHandler()
    if oInputParameterHandler.exist('securityCookie'):
        sSecurityValue = oInputParameterHandler.getValue('securityCookie')
    

    sPattern = '<a class="p1" href="[^"]+" >.*?<img class="large" src="(http://[^"]+)".*?<a href="([^"]+)" id="([^"]+)">([^<]+)<'
    #sPattern = 'class="alt1Active".*?<a href="(forumdisplay.php[^"]+)".*?>([^<]+)<.*?(src="([^"]+)|</td>).*?</tr>' #Serien
    # request
    sHtmlContent = __getHtmlContent(sUrl = siteUrl)

    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False):
        return
    oGui = cGui()
    for aEntry in aResult[1]:
        sMovieTitle = aEntry[3].replace('&amp;','&')
        sUrl = URL_SHOW_MOVIE + str(aEntry[2]).replace('thread_title_', '')
        
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('parseMovie')
        oGuiElement.setTitle(sMovieTitle)
        oGuiElement.setThumbnail(aEntry[0])
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('movieUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('securityCookie', sSecurityValue)
        
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    # check for next site
    sPattern = '<td class="thead">Zeige Themen .*?von ([0-9]+)</td>'
    if (__checkNextPage(iPage,sPattern,sHtmlContent)):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('parseMovieResultSite')
        oGuiElement.setTitle('next ..')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('iPage', int(iPage)+1)
        oOutputParameterHandler.addParameter('normalySiteUrl', normalySiteUrl)
        oOutputParameterHandler.addParameter('siteUrl', normalySiteUrl+str(int(iPage)+1))
        oOutputParameterHandler.addParameter('securityCookie', sSecurityValue)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)
        
    if (__checkNextPage(iPage,sPattern,sHtmlContent,5)):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('parseMovieResultSite')
        oGuiElement.setTitle('next ..5..')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('iPage', int(iPage)+5)
        oOutputParameterHandler.addParameter('normalySiteUrl', normalySiteUrl)
        oOutputParameterHandler.addParameter('siteUrl', normalySiteUrl+ str(int(iPage)+5))
        oOutputParameterHandler.addParameter('securityCookie', sSecurityValue)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)
        
    oGui.setView('movies')            
    oGui.setEndOfDirectory()
    
def __checkNextPage(iPage, sPattern, sHtml, iJump = 1):
    sPattern = '<td class="thead">Zeige Themen .*?von ([0-9]+)</td>'
    oParser = cParser()
    aResult = oParser.parse(sHtml, sPattern)
    if (aResult[0] == True):
        iTotalCount = int(aResult[1][0])
        iNextPage = int(iPage) + iJump
        iCurrentDisplayStart = __createDisplayStart(iNextPage)
        if (iCurrentDisplayStart < iTotalCount):
            return True
    return False


def __createDisplayStart(iPage):
    return (20 * int(iPage)) - 20

def __createInfo(oGui, sHtmlContent):
    sPattern = '<td class="alt1" id="td_post_.*?<img src="([^"]+)".*?<b>Inhalt:</b>(.*?)<br />'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sThumbnail = str(aEntry[0])
            sDescription = cUtil().removeHtmlTags(str(aEntry[1])).replace('\t', '').strip()
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle('info (press Info Button)')
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setFunction('dummyFolder')
            oGuiElement.setDescription(sDescription)
            oGui.addFolder(oGuiElement)
            
def showAdult():
    oConfig = cConfig()
    if oConfig.getSetting('showAdult')=='true':    
        return True
    return False

def dummyFolder():
    oGui = cGui()
    oGui.setEndOfDirectory()

def parseMovie():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('movieUrl') and oInputParameterHandler.exist('sMovieTitle')):
        sSiteUrl = oInputParameterHandler.getValue('movieUrl')
        sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')    
    if oInputParameterHandler.exist('securityCookie'):
        sSecurityValue = oInputParameterHandler.getValue('securityCookie') 
        sHtmlContent = __getHtmlContent(sUrl = sSiteUrl)

        __createInfo(oGui, sHtmlContent)
        
        Urls = []
        
        #Mehrteiler (nicht sicher ob noch korrekt)
        sPatternMehrteiler = '</div>CD(\d+):<br />\s*<div style="display: none;" id="[^"]+">\s*<a href="([^"]+)" title="[^"]+" target="_blank">([^<]+)</a>'
        aResult = cParser().parse(sHtmlContent, sPatternMehrteiler)
        if aResult[0] == True:
            for aEntry in aResult[1]:
                sNum = aEntry[0]
                sUrl = aEntry[1]
                sHoster = aEntry[2]
                
                Urls.append(sUrl)
                if sUrl.find('sockshare') > -1:             
                    oHoster = cHosterHandler().getHoster2('sockshare')
                elif sUrl.find('putlocker') > -1:
                    oHoster = cHosterHandler().getHoster2('putlocker')
                else:
                    oHoster = cHosterHandler().getHoster2(sHoster)
                
                if oHoster != False:
                    oHoster.setFileName(sMovieTitle)
                    oHoster.setDisplayName("Teil " + sNum + " - " + oHoster.getDisplayName())
                    cHosterGui().showHoster(oGui, oHoster, sUrl, True)
        
        #Einteiler
        sPattern = 'id="ame_noshow_post.*?<a href="([^"]+)" title="[^"]+" target="_blank">([^<]+)</a>'
        aResult = cParser().parse(sHtmlContent, sPattern)
        if aResult[0] == True:
            for aEntry in aResult[1]:
                sUrl = aEntry[0]
                sHoster = aEntry[1]
                
                if sUrl in Urls:
                    continue
                if 'g-stream.in/secure/' in sUrl :
                    oRequest = cRequestHandler(sUrl)
                    oRequest.addHeaderEntry('Cookie', sSecurityValue)
                    try:
                        oRequest.request()
                        sUrl = oRequest.getRealUrl()
                    except:
                        continue
                
                sHost = cHosterHandler().getHoster(sUrl)                   
                if sHost != False:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('showHoster')
                    if 'youtube' in sHost:
                        oGuiElement.setTitle(sHost + ' Trailer')
                    else:    
                        oGuiElement.setTitle(sHost)

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', sUrl)
                    oOutputParameterHandler.addParameter('sHoster', sHost)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    oOutputParameterHandler.addParameter('securityCookie', sSecurityValue)
                    oGui.addFolder(oGuiElement,oOutputParameterHandler)

            
    oGui.setEndOfDirectory()

def showHoster():
    oInputParameterHandler = cInputParameterHandler()
    oGui = cGui()                

    sUrl = oInputParameterHandler.getValue('sUrl')
    sHoster = oInputParameterHandler.getValue('sHoster')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
   
    cHosterGui().showHosterMenuDirect(oGui, sHoster, sUrl, sFileName=sMovieTitle)
            
    oGui.setEndOfDirectory() 

def __parseHosterSiteFromSite(aHosters, sHtmlContent, sHosterIdentifier, sHosterId):
    aHoster = []
    sRegex = '<div style="display: none;" id="ame_noshow_post_.*?<a href="' + URL_HOSTER + sHosterId + '([^ ]+)" target="_blank" rel="nofollow" >'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sRegex)    
    if (aResult[0] == True):
        for aEntry in aResult[1]:            
            sUrl = URL_HOSTER + sHosterId + aEntry

            oHoster = cHosterHandler().getHoster2(sHosterIdentifier)
            aHoster.append(oHoster)
            aHoster.append(str(sUrl).replace(' ', '+'))
            aHosters.append(aHoster)
      
    return True
