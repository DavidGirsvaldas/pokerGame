class Player:

    def __init__(self):
        self.cards = []
        self.stack = 0
        self.money_in_pot = 0
        def raise_(ex):
            raise ex
        self.act = lambda x: raise_(NotImplemented())


