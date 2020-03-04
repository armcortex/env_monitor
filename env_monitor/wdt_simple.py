import machine as mc


class WDT:
    def __init__(self, timeout=5000):
        self.timer = mc.Timer(-1)
        self.fed = False

        self.init(msec=timeout)

    def feed(self):
        self.fed = True

    def trig(self):
        mc.reset()

    def wdtcb(self, tmr):
        if not self.fed:
            self.deinit()
            self.trig()
        self.fed = False

    def deinit(self):
        self.timer.deinit()

    def init(self, msec):
        self.fed = False
        self.timer.init(period=msec, mode=mc.Timer.PERIODIC, callback=self.wdtcb)