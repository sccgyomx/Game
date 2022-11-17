class Player:
    playerShotList = []
    PositionX = None
    playerPositionY = None
    state = True
    def __init__(self, positionX, positionY):
        self.PositionX = positionX
        self.PositionY = positionY

    def addShot(self):
        pass

    def isLife(self):
        return self.state
