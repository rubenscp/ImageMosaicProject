# Pixel Class
class Pixel:
    def __init__(self, lin, col, red, green, blue):
        self.lin = lin
        self.col = col
        self.red = red
        self.green = green
        self.blue = blue

    def toString(self):
        text = 'RGB: ' + '(' + str(self.lin) + ',' + str(self.col) + ') - (' + str(self.red) + ',' + str(
            self.green) + ',' + str(self.blue) + ')'
        return text

    # checks if the pixel is blue
    def isBlue(self):
        if self.blue >= 60 and self.red <= 20 and self.green <= 40:
            # print('é azul: ' + str(self.lin) + ',' + str(self.col) + ': R>' + str(self.red) + ': G>' + str(
            #     self.green) + ': B>' + str(self.blue))
            return True
        else:
            return False
