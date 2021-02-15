# Detected Object Class


class DetectedObject:

    def getValueOf(className):
        if className == 'exuvia':
            return 0

        if className == 'instar1':
            return 1

        if className == 'instar2':
            return 2

        if className == 'instar3':
            return 3

        if className == 'instar4':
            return 4

        if className == 'adulta':
            return 5

        if className == 'ovo':
            return 6

        if className == 'instar1ou2':
            return 7

        if className == 'instar3ou4':
            return 8

        return 99
