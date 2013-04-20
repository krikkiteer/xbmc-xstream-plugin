# -*- coding: utf-8 -*-
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
import logger
import urlresolver
from urlresolver.types import HostedMediaFile


class cHosterHandler:

    def getUrl(self, oHoster):
        sUrl = oHoster.getUrl()
        if (oHoster.checkUrl(sUrl)):
            oRequest = cRequestHandler(sUrl)
            sContent = oRequest.request()
            pattern = oHoster.getPattern()
            if isinstance(pattern, str):
                aMediaLink = cParser().parse(sContent, oHoster.getPattern())
                if aMediaLink[0] is True:
                    logger.info('hosterhandler: ' + aMediaLink[1][0])
                    return True, aMediaLink[1][0]
            else:
                for p in pattern:
                    aMediaLink = cParser().parse(sContent, p)
                    if aMediaLink[0] is True:
                        logger.info('hosterhandler: ' + aMediaLink[1][0])
                        return True, aMediaLink[1][0]

        return False, ''

    def getHoster2(self, sHoster):
        return self.getHoster(sHoster)

    def getHoster(self, sHosterFileName):
        """
        interfaces urlresolver to find supported hoster..

        :param sHosterFileName: str, link to media as scraped from page
        :returns str: the hostname of the hoster or False
        """
        if sHosterFileName != '':
            source = [HostedMediaFile(url=sHosterFileName)]
            valid_sources = urlresolver.filter_source_list(source)
            if valid_sources:
                return valid_sources[0].get_host()
        return False
