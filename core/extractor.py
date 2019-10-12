import os
import re
import asyncio
from functools import wraps, partial

class Extractor(object):
    '''
        params: P is the path of ffmpeg in your computer

        requirement: ffmpeg

        aim: this class is for extract audio from video, and set metadata, album cover to audio
    '''
    def __init__(self, P, mediafolder = None):

        self.__version = "1.0"

        self.__initffmpegcmd(P)

        self.__initFolders(mediafolder)

        print('[ok] init extractor based on ffmpeg in %s' % P)

    '''
    init ffmpeg command code
    '''
    def __initffmpegcmd(self, P):

        # extract audio from video --------------

        # {0: input mp4}; {1: output file type}; {2: output file}
        self.extractCode = P + 'ffmpeg -i {0} -f {1} -vn {2} -loglevel quiet'

        # {0: input mp4}; {1: input cover img}; {2: -metadata}; {3: output file}
        self.extractCoverMetaCode = P + 'ffmpeg -i {0} {1} -map 0:1 -map 1:0 -acodec libmp3lame -id3v2_version 3 {2} {3} -loglevel quiet'
        
        # {0: input mp4}; {1: -metadata}; {2: output file}
        self.extractMetaCode = P + 'ffmpeg -i {0} -acodec libmp3lame -id3v2_version 3 {1} {2} -loglevel quiet'

        # set metadata --------------------------

        # {0: input mp3}; {1: input cover img}; {2: -metadata}; {3: output file}
        self.setcoverCode = P + 'ffmpeg -i {0} {1} -map 0:0 -map 1:0 -c copy -id3v2_version 3 {2} {3} -loglevel quiet'

        # {0: input mp4}; {1: -metadata}; {2: output file}
        self.setmetaCode = P + 'ffmpeg -i {0} -c copy -id3v2_version 3 {1} {2} -loglevel quiet'

        # show metadata -------------------------

        # {0: file}
        self.metadataCode = P + 'ffprobe {0} -hide_banner'

    
    '''
    init local folders
    '''
    def __initFolders(self, mediafolder = None):
        
        if not mediafolder:
            mediafolder = os.getcwd()
        
        elif not os.path.exists(mediafolder):
            os.makedirs(mediafolder)
        
        self.videoFolder = os.path.join(mediafolder, "videos")
        self.audioFolder = os.path.join(mediafolder, "audios")
        self.picFolder = os.path.join(mediafolder, "pics")

        for path in [self.videoFolder, self.audioFolder, self.picFolder]:
            if not os.path.exists(path):
                os.makedirs(path)

    '''
    format args for ffmpeg command line
    '''
    def __metadataFormat(self, meta):

        metadata = ""
        for data in meta.items():

            metadata += "-metadata {0}={1} ".format(data[0], data[1].replace(" ",""))

        return metadata

    
    def async_wrap(func):

        @wraps(func)
        async def run(*args, loop=None, executor=None, **kwargs):

            if loop is None:
                loop = asyncio.get_event_loop()

            pfunc = partial(func, *args, **kwargs)
            return await loop.run_in_executor(executor, pfunc)

        return run

    
    @async_wrap
    def asyn_extract(self, videoname, meta = None, cover = None):
        
        return self.extract(videoname, meta, cover)

    '''
    interface for extract audio from local video file, and set cover img if exists
    '''
    def extract(self, videoname, meta = None, cover = None):

        if os.path.exists(videoname):
            # user path
            videopath = videoname
        
        else:
            # default folder
            videopath = os.path.join(self.videoFolder, videoname)

        # if no video file
        if not os.path.exists(videopath):
            return 'error: no video file'

        realname = re.findall(r'([^<>/\\\|:""\*\?]+)\.\w+$',videoname)[0]

        dfaudioType = "mp3"

        audiofile = "%s.%s" % (realname, dfaudioType)

        audiopath = os.path.join(self.audioFolder, audiofile)

        # if audio exists
        if os.path.exists(audiopath):
            return (audiopath, audiofile)
        
        # if has metadata
        if meta:
            metadata = self.__metadataFormat(meta)

            if cover and os.path.exists(cover):
                
                cover = "-i {0}".format(cover)
                cmd = self.extractCoverMetaCode.format(videopath, cover, metadata, audiopath)
            
            else:
                cmd = self.extractMetaCode.format(videopath, metadata, audiopath) 
        else:
            cmd = self.extractCode.format(videopath, audioType, audiopath)

        os.system(cmd)

        # if successfully extract audio out
        if os.path.exists(audiopath):
            
            return  (audiopath, audiofile)
        
        return "error"

    '''
    change metadata or cover image of a local mp3 file
    '''
    def setinfo(self, audio, meta, cover = None):

        newaudio = audio.replace('.mp3', '-new.mp3')

        metadata = self.__metadataFormat(meta)

        if cover and os.path.exists(cover):

            cover = "-i {0}".format(cover)
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


def single_test():
    
    e = Extractor("F:/tool/ffmpeg/bin/", "F:/Project/Relaxion/files")

    metadata = {
        'title': "说好不哭（with 五月天阿信）",
        'album': "说好不哭（with 五月天阿信）",
        'artist': "周杰伦"
    }

    video = "F:/Project/Relaxion/files/videos/说好不哭（with五月天阿信）.mp4"
    pic = "F:/Project/Relaxion/files/pics/说好不哭（with五月天阿信）.jpg"

    a = e.extract(video, metadata, pic)
    
    # audio = "F:/Project/Relaxion/files/audios/说好不哭（with五月天阿信）.mp3"
    # e.setinfo(audio, metadata)

def async_tests():

    e = Extractor("F:/tool/ffmpeg/bin/", "F:/Project/Relaxion/files")

    folder = "F:/Project/Relaxion/files/videos"

    files= os.listdir(folder)

    tasks = []

    for f in files:

        fullpath = os.path.join(folder, f)
        
        metadata = {
            'title': f,
            'album': f,
            'artist': "周杰伦"
        }

        task = e.asyn_extract(fullpath, metadata)

        tasks.append(task)


    loop = asyncio.get_event_loop()
    
    done, _ = loop.run_until_complete(asyncio.wait(tasks))

    for fut in done:
        print("return value is {}".format(fut.result()))

    loop.close()



if __name__ == '__main__':

    import time

    now = lambda: time.time()

    start = now()

    async_tests()
    # single_test()

    print('TIME: ', now() - start)

