import os

class extractor(object):
    '''
        params: P is the path of ffmpeg in your computer

        requirement: ffmpeg

        aim: this class is for extract audio from video, and set metadata, album cover to audio
    '''
    def __init__(self, P, mediafolder = None):

        self.__version = "1.0"

        self.__initffmpegcmd(P)

        self.__initFolders(mediafolder)

        print('init extractor based on ffmpeg in %s' % P)

    '''
    init ffmpeg command code
    '''
    def __initffmpegcmd(self, P):

        # extract audio from video --------------

        # {0: input mp4}; {1: output file type}; {2: output file}
        self.extractCode = P + 'ffmpeg -i {0} -f {1} -vn {2} -hide_banner'

        # {0: input mp4}; {1: input cover img}; {2: -metadata}; {3: output file}
        self.extractCoverMetaCode = P + 'ffmpeg -i {0} {1} -map 0:1 -map 1:0 -acodec libmp3lame -id3v2_version 3 {2} {3} -hide_banner'
        
        # {0: input mp4}; {1: -metadata}; {2: output file}
        self.extractMetaCode = P + 'ffmpeg -i {0} -acodec libmp3lame -id3v2_version 3 {1} {2} -hide_banner'

        # set metadata --------------------------

        # {0: input mp3}; {1: input cover img}; {2: -metadata}; {3: output file}
        self.setcoverCode = P + 'ffmpeg -i {0} {1} -map 0:0 -map 1:0 -c copy -id3v2_version 3 {2} {3} -hide_banner'

        # {0: input mp4}; {1: -metadata}; {2: output file}
        self.setmetaCode = P + 'ffmpeg -i {0} -c copy -id3v2_version 3 {1} {2} -hide_banner'

        # show metadata -------------------------

        # {0: file}
        self.metadataCode = P + 'ffprobe {0} -hide_banner'

    
    '''
    init local folders
    '''
    def __initFolders(self, mediafolder = None):
        
        if not mediafolder or not os.path.exists(mediafolder):
            mediafolder = os.getcwd()
        
        self.videoFolder = os.path.join(mediafolder, "videos")
        self.audioFolder = os.path.join(mediafolder, "audios")

        for path in [self.videoFolder, self.audioFolder]:
            if not os.path.exists(path):
                os.makedirs(path)

    '''
    format args for ffmpeg command line
    '''
    def __metadataFormat(self, meta):

        cover = ""
        if meta['album']:
            pic = os.path.join(self.videoFolder, meta['album'] + ".jpg")
            
            if os.path.exists(pic):
                cover = "-i {0}".format(pic)

        metadata = ""
        for data in meta.items():

            metadata += "-metadata {0}={1} ".format(data[0], data[1])

        return (cover, metadata)

    '''
    interface for extract audio from local video file, and set cover img if exists
    '''
    def extract(self, videoname, meta = None):

        vFilename = videoname
        audioType = "mp3"
        aFilename = "%s.%s" % (vFilename.split('.')[0], audioType)

        vFullFilename = os.path.join(self.videoFolder, vFilename)
        aFullFilename = os.path.join(self.audioFolder, aFilename)

        # if exists
        if os.path.exists(aFullFilename):
            return aFullFilename
        
        # if has metadata
        if meta:
            cover, metadata = self.__metadataFormat(meta)
            if cover:
                cmd = self.extractCoverMetaCode.format(vFullFilename, cover, metadata, aFullFilename)
            else:
                cmd = self.extractMetaCode.format(vFullFilename, metadata, aFullFilename) 
        else:
            cmd = self.extractCode.format(vFullFilename, audioType, aFullFilename)

        os.system(cmd)

        return aFullFilename

    '''
    change metadata or cover image of a local mp3 file
    '''
    def setinfo(self, audio, meta):

        newaudio = audio.replace('.mp3', '-new.mp3')

        cover, metadata = self.__metadataFormat(meta)

        if cover:
            cmd = self.setcoverCode.format(audio, cover, metadata, newaudio)
        else:
            cmd = self.setmetaCode.format(audio, metadata, newaudio)
        os.system(cmd)
        
        return newaudio

    '''
    show metadata of a local mp3 file
    '''
    def showmeta(self, mp3):

        cmd = self.metadataCode.format(mp3)
        os.system(cmd)

    '''
    read only version info
    '''
    @property
    def version(self):

        return self.__version



if __name__ == '__main__':

    e = extractor("F:\\tool\\ffmpeg\\bin\\")

    metadata = {
        'title': "告白气球",
        'album': "周杰伦的床边故事",
        'artist': "周杰伦"
    }

    # a = e.extract("gbqq.mp4", metadata)