from Filename import *

class History():

    def __call__(self):
        return(self.getObj)

    def __init__(self, title, path_video, path_audio):
        self.title = cleansing(title)
        self.path_video = rcleansing(path_video)
        self.path_audio = rcleansing(path_audio)
    
    def __str__(self):
        obj = {
            self.title : {
                "path_video" : self.path_video,
                "path_audio" : self.path_audio
            }
        }
        return str(obj)
    
    @property
    def getObj(self):
        return {
            self.title : {
                "path_video" : self.path_video,
                "path_audio" : self.path_audio
            }
        }
    
    @property
    def getKey(self):
        key = [key for key in self.getObj]
        return key[0]
    
    @property
    def getValue(self):
        value = self.getObj[self.getKey]
        return value
