# coding=utf-8
import os
import bs
import shutil

NEW_MAP_DIRECTORY = 'mapYinYang'  # The directory contains which were described in README
NEW_MAP_NAME = u'Yin Yang'  # ensure unicode
SUPPORTED_PLATFORMS = ['other']  # other means Win, Linux, Mac as they all use .dds


### YOU DONNOT HAVE TO EDIT ANYTHING BELOW ###

class InstallerLanguageEnglish(object):
    installing = u'Installing map [%s]...'
    success = u'Map [%s] installation succeeded, please restart'
    fail = u'Map [%s] installation failed'
    notSupported = u'Map [%s] is not supported on %s'


class InstallerLanguageChinese(object):
    installing = u'正在安装地图[%s], 请稍候...'
    success = u'地图[%s]安装完成！请彻底重启游戏生效'
    fail = u'地图[%s]安装失败'
    notSupported = u'地图[%s]不支持%s平台！'


InstallerLanguage = InstallerLanguageEnglish


class NewMapInstaller(object):
    mapName = NEW_MAP_NAME
    copyDir = NEW_MAP_DIRECTORY
    supportedPlatforms = SUPPORTED_PLATFORMS

    def __init__(self):
        self.mapFilesDir = bs.getEnvironment()['userScriptsDirectory'] + '/' + self.copyDir + '/'
        # osPycDir = os.__file__
        # self.dataDir = '/'.join(osPycDir.split('/')[:-2]) + '/data/'
        self.scriptsDir = bs.getEnvironment()['systemScriptsDirectory'] + '/'
        self.dataDir = self.scriptsDir + '../'
        self.modelsDir = self.dataDir + 'models/'
        self.audioDir = self.dataDir + 'audio/'
        self.texturesDir = self.dataDir + 'textures/'

        self.platform = bs.getEnvironment()['platform']
        self.models = []
        self.textures = []
        self.audio = []
        self.searchFiles()

    def searchFiles(self):
        root, dirs, files = os.walk(self.mapFilesDir).next()
        for fn in files:
            if fn.endswith('.ktx') or fn.endswith('.dds'):
                self.textures.append(fn)
            if fn.endswith('.bob') or fn.endswith('.cob'):
                self.models.append(fn)
            if fn.endswith('.ogg'):
                self.audio.append(fn)

        initFile = self.mapFilesDir + '__init__.py'
        if not os.path.isfile(initFile):
            f = open(initFile, 'w')
            f.close()

    def checkInstalled(self):
        installed = True
        for model in self.models:
            systemModel = self.modelsDir + model
            if not os.path.isfile(systemModel):
                installed = False
                break

        for texture in self.textures:
            if self.platform == 'android':
                if texture.endswith('.dds'):
                    continue
            else:
                if texture.endswith('.ktx'):
                    continue
            systemTexture = self.texturesDir + texture
            if not os.path.isfile(systemTexture):
                installed = False
                break

        for au in self.audio:
            systemAudio = self.audioDir + au
            if not os.path.exists(systemAudio):
                installed = False
                break

        return installed

    def checkSupported(self):
        if self.platform == 'android':
            if 'android' in self.supportedPlatforms:
                return True
        else:
            if 'other' in self.supportedPlatforms:
                return True
        return False

    def install(self):
        if not self.checkSupported():
            bs.screenMessage(InstallerLanguage.notSupported % (self.mapName, self.platform))
            return

        if self.checkInstalled():
            exec 'import ' + NEW_MAP_DIRECTORY + '.bsNewMap'
            return

        bs.screenMessage(InstallerLanguage.installing % self.mapName)

        try:
            for model in self.models:
                systemModel = self.modelsDir + model
                modModel = self.mapFilesDir + model
                shutil.copy(modModel, systemModel)

            for texture in self.textures:
                if self.platform == 'android':
                    if texture.endswith('.dds'):
                        continue
                else:
                    if texture.endswith('.ktx'):
                        continue
                systemTex = self.texturesDir + texture
                modTex = self.mapFilesDir + texture
                shutil.copy(modTex, systemTex)

            for au in self.audio:
                systemAudio = self.audioDir + au
                modAudio = self.mapFilesDir + au
                shutil.copy(modAudio, systemAudio)

            bs.screenMessage(InstallerLanguage.success % self.mapName, color=(0, 1, 0))
        except IOError, e:
            bs.screenMessage(InstallerLanguage.fail % self.mapName, color=(1, 0, 0))
            bs.screenMessage(str(e), color=(1, 0, 0))
            print e


NewMapInstaller().install()
