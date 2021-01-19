import time
from datetime import timedelta

class Timer:
    def __init__(self):
        self.start = time.time()
        self.deltaTime = 0
        self.paused = True

    def getPlayTime(self):
        if not self.paused:
            return str(timedelta(seconds = self.deltaTime + (time.time() - self.start))).split(".")[0]
        else:
            return str(timedelta(seconds = self.deltaTime)).split(".")[0]

    def pause(self):
        if not self.paused:
            self.paused = True
            self.deltaTime += time.time() - self.start
        else:
            raise Exception("Can't pause timer when already paused")

    def play(self):
        if self.paused:
            self.paused = False
            self.start = time.time()
        else:
            raise Exception("Can't start timer when already running")

    def isPaused(self):
        return self.paused