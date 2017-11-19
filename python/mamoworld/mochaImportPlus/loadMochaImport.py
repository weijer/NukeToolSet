import imp, os, sys
import nuke


## adds the correct plugin path for this version of NUKE

def load():
    supportedMagicNumbers = ['03f30d0a', 'd1f20d0a']

    try:
        magicNumberOfThisVersion = imp.get_magic().encode('hex')
        if magicNumberOfThisVersion in supportedMagicNumbers:
            pathToThisVersion = "python/mamoworld/mochaImportPlus/version_" + magicNumberOfThisVersion
            nuke.pluginAddPath(pathToThisVersion)
        else:
            raise Exception(
                "MochaImport+ for NUKE: unsupported version of Python:" + sys.version + "(magic number:" + magicNumberOfThisVersion + ")")

    except Exception as e:
        import traceback
        nuke.tprint(traceback.format_exc())  # Just in case
        msg = 'ERROR: %s' % e
        if nuke.GUI:
            nuke.message(msg)
        else:
            nuke.tprint(msg)


def addIconPath(base_dir):
    """
    @param base_dir:
    @return:
    """
    icons_mocha_dir = replace_path(os.path.join(base_dir, "python/mamoworld/mochaImportPlus/icons"))
    nuke.pluginAddPath(icons_mocha_dir)

def replace_path(path):
    """
    replace path
    :param path:
    :return:
    """
    final_path = path.replace('\\', '/')
    return final_path