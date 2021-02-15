# Ground Truth Data Class


class GroundTruthData:
    def __init__(self, id, exuvia, instar1, instar2, instar3, instar4, adultas):
        self.id = id
        self.exuvia = exuvia
        self.instar1 = instar1
        self.instar2 = instar2
        self.instar3 = instar3
        self.instar4 = instar4
        self.adultas = adultas

    def toString(self):
        text = 'id: ' + str(self.id) \
               + 'exuvia: ' + str(self.exuvia) \
               + '  instar1: ' + str(self.instar1) \
               + '  instar2: ' + str(self.instar2) \
               + '  instar3: ' + str(self.instar3) \
               + '  instar4: ' + str(self.instar4) \
               + '  adultas: ' + str(self.adultas)
        return text

    def hasJustOneClass(self):
        return True if str(self.getJustOneClass()) == '' else False

    def getJustOneClass(self):
        classCounter = 0
        className = ''
        if self.exuvia > 0:
            hasExuvia = True
            classCounter += 1
            className = 'exuvia'

        if self.instar1 > 0:
            hasInstar1 = True
            classCounter += 1
            className = 'instar1'

        if self.instar2 > 0:
            hasInstar2 = True
            classCounter += 1
            className = 'instar2'

        if self.instar3 > 0:
            hasInstar3 = True
            classCounter += 1
            className = 'instar3'

        if self.instar4 > 0:
            hasInstar4 = True
            classCounter += 1
            className = 'instar4'

        # evaluating if has just one class
        if classCounter == 1:
            return className
        else:
            return ''
