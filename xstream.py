from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
import logger


# Main starting function
def run():
    parseUrl()


def parseUrl():
    oInputParameterHandler = cInputParameterHandler()

    # If no function is set, we set it to the default "load" function
    if oInputParameterHandler.exist("function"):
        sFunction = oInputParameterHandler.getValue("function")
    else:
        sFunction = "load"

  # Test if we should run a function on a special site
    if oInputParameterHandler.exist('site'):
        sSiteName = oInputParameterHandler.getValue('site')
        logger.info(oInputParameterHandler.getAllParameter())
        logger.info("Call function '%s' from '%s'" % (sFunction, sSiteName))

        # If the hoster gui is called, run the function on it and return
        if isHosterGui(sSiteName, sFunction):
            return

        # If the about gui is called, run the function on it and return
        if isAboutGui(sSiteName, sFunction):
            return

        # If the urlresolver settings are called
        if isResolverGui(sSiteName, sFunction):
            return

        # Else load any other site as plugin and run the function
        exec "import %s as plugin" % sSiteName
        exec "plugin.%s()" % sFunction

    else:
        # As a default if no site was specified, we run the default starting gui with all plugins
        oGui = cGui()
        oPluginHandler = cPluginHandler()

        aPlugins = oPluginHandler.getAvailablePlugins()

        if len(aPlugins) <= 0:
            logger.info("No Plugins found")

            # Open the settings dialog to choose a plugin that could be enable
            oGui.openSettings()
            oGui.updateDirectory()
        else:
            # Create a gui element for every plugin found
            for aPlugin in aPlugins:
                oGuiElement = cGuiElement()
                oGuiElement.setTitle(aPlugin[0])
                oGuiElement.setSiteName(aPlugin[1])
                oGuiElement.setFunction(sFunction)
                if aPlugin[2] != '':
                    oGuiElement.setThumbnail(aPlugin[2])
                oGui.addFolder(oGuiElement)

            # Create a gui element for urlresolver settings
            oGuiElement = cGuiElement()
            oGuiElement.setTitle("Resolver Settings")
            oGuiElement.setSiteName("urlresolver")
            oGuiElement.setFunction("urlresolver.display_settings()")
            oGuiElement.setThumbnail("DefaultAddonService.png")
            oGui.addFolder(oGuiElement)

        oGui.setEndOfDirectory()


def isHosterGui(sSiteName, sFunction):
    if sSiteName == "cHosterGui":
        oHosterGui = cHosterGui()
        exec "oHosterGui.%s()" % sFunction

        return True

    return False


def isAboutGui(sSiteName, sFunction):
    if sSiteName == "cAboutGui":
        oAboutGui = cAboutGui()
        exec "oAboutGui.%s()" % sFunction
        return True

    return False


def isResolverGui(sSiteName, sFunction):
    if sSiteName == "urlresolver":
        exec sFunction
        return True

    return False
