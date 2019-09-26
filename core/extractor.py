import os

class extractor(object):
    def __init__(self, ffmpeg):

        self.ffmpegFormatCode = ffmpeg + ' -i {0} -f {1} -vn {2}'
        self.videoFolder = os.path.join(os.getcwd(), "videos")
        self.audioFolder = os.path.join(os.getcwd(), "audios")

        for path in [self.videoFolder, self.audioFolder]:
            if not os.path.exists(path):
                os.makedirs(path)


    def extract(self, videoname):

        vFilename = videoname
        audioType = "mp3"
        aFilename = "%s.%s" % (vFilename.split('.')[0], audioType)

        vFullFilename = os.path.join(self.videoFolder, vFilename)
        aFullFilename = os.path.join(self.audioFolder, aFilename)

        if os.path.exists(aFullFilename):
            return aFullFilename
        
        cmd = self.ffmpegFormatCode.format(vFullFilename, audioType, aFullFilename)
        os.system(cmd)
        print("Finish conversion to {0}".format(aFullFilename))

        return aFullFilename


if __name__ == '__main__':

    e = extractor("F:\\tool\\ffmpeg\\bin\\ffmpeg")

    a = e.extract("gbqq.mp4")

    print(a)
    