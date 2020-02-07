import os
import re
import subprocess

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

        # {0: input mp4}; {2: output file}
        self.extractCode = P + 'ffmpeg -i {0} -vn {2} -loglevel quiet'

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

    def matchCover(self, name):
        
        path = os.path.join(self.picFolder, '%s.jpg' % name)

        if os.path.exists(path):

            return path
        
        return None

    def getAudio(self, realname):

        dfaudioType = "mp3"

        audiofile = "%s.%s" % (realname, dfaudioType)

        audiopath = os.path.join(self.audioFolder, audiofile)

        # if audio exists
        if os.path.exists(audiopath):
            return audiofile
        
        return None

    '''
    interface for extract audio from local video file, and set cover img if exists
    '''
    def extract_from_local(self, videoname, meta = None, cover = None):

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
            return audiofile
        
        # if cover prepared
        if not (cover and os.path.exists(cover)):
            # try to match cover automatically
            cover = self.matchCover(realname)
        
        self.extract(videopath, meta, cover, audiopath)

        # successfully extract out audio
        if os.path.exists(audiopath):
            os.remove(audiopath)
            return audiofile

        return "error"

    def extract_from_url(self, video_url, meta, music_name = None, cover_url = None):
        
        if not music_name:
            music_name = "%s.mp3" % meta['title']

        music_name = music_name.replace(" ","")
        output = os.path.join(self.audioFolder, music_name)

        # successfully extract out audio
        if os.path.exists(output):
            return music_name

        self.extract(video_url, meta, cover_url, output)

        # successfully extract out audio
        if os.path.exists(output):
            return music_name

        return "error"

    def extract(self, in_put, meta, cover, output):
        # if has metadata
        if meta:
            metadata = self.__metadataFormat(meta)

            if cover:
                cover = "-i {0}".format(cover)
                cmd = self.extractCoverMetaCode.format(in_put, cover, metadata, output)
            
            else:
                cmd = self.extractMetaCode.format(in_put, metadata, output) 
        else:
            cmd = self.extractCode.format(in_put, output)

        print(cmd)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()  

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
        
        p = subprocess.Popen(cmd, shell=True)
        p.wait()  
        
        return newaudio

    '''
    show metadata of a local mp3 file
    '''
    def showmeta(self, mp3):

        cmd = self.metadataCode.format(mp3)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()

    '''
    read only version info
    '''
    @property
    def version(self):

        return self.__version


def single_test():
    
    e = Extractor("D:/tool/ffmpeg/bin/", "D:/Project/Relaxion/files")

    metadata = {
        'title': "晴天",
        'album': "晴天",
        'artist': "周杰伦"
    }

    # video = "D:/Project/Relaxion/files/videos/晴天.mp4"
    # pic = "D:/Project/Relaxion/files/pics/default.jpg"

    # a = e.extract_from_local(video, metadata, pic)
    video = "http://117.169.112.218/mv.music.tc.qq.com/AF7aJMH6V8nmxiSHCIW-Qhyi3XtqxEYnsIFc62e_mlz0/80CA627E10F1F8E395D4EE57FD382C55A11B6A0CABD35F4AF18D08CC03F65BC1DA480E8ABF2D171B562B92FFD03DDE33ZZqqmusic_default/1049_M0100549000F3mmR15zesk1000055326.f20.mp4?fname=1049_M0100549000F3mmR15zesk1000055326.f20.mp4"
    pic = "https://y.gtimg.cn/music/photo_new/T002R300x300M000000MkMni19ClKG.jpg?max_age=2592000"
    a = e.extract_from_url(video, metadata, cover_url = pic)

    print(a)


if __name__ == '__main__':

    import time

    now = lambda: time.time()

    start = now()

    single_test()

    print('TIME: ', now() - start)

