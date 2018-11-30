from ledrgbstrip import LedRGBStrip
class Ring:
    number = 0

    LED_COUNT = 16  # Number of LED pixels.

    def __init__(self, strip: LedRGBStrip, number: int):
        super().__init__()
        self.strip = strip
        self.number = number

    def setColor(self, r, g, b):
        for i in range(self.LED_COUNT):
            self.strip.setLED(self.number*self.LED_COUNT + i, r, g, b)
        self.strip.show();

    def clear(self):
        for i in range(self.LED_COUNT):
            self.strip.setLED(self.number * self.LED_COUNT + i, 0, 0, 0)
        self.strip.show();