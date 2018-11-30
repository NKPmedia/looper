from I2C_LCD_driver import lcd

class BootScreen:

    def __init__(self, lcd:lcd):
        self.lcd = lcd
        self.lcd.lcd_clear()
        self.text = "Hello World!"
        self.lcd.lcd_display_string(self.text, 1)


    def write(self, text, text2 = ""):
        self.text = text
        self.text2 = text2
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string(self.text, 1)
        self.lcd.lcd_display_string(self.text2, 2)