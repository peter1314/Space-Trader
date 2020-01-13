from .bandit import Bandit

class SuperBandit(Bandit):

    def set_demand(self, player):
        """Sets the demand for the super bandit"""
        #demand is influenced by karma
        self.credit_demand = player.get_credits() * (.5 + player.get_karma())

    def give_flea_punishment(self, player):
        """Determines what happens if the player fails to flee"""
        super(SuperBandit, self).give_flea_punishment(player)
        player.ship.lose_health(15)
        self.outcome = "The Super Bandit caught you and took your credits!"

    def give_fight_punishment(self, player):
        """Determines what happens if the player fails to fight"""
        super(SuperBandit, self).give_fight_punishment(player)
        player.ship.lose_health(30)
        self.outcome = "The Super Bandit outgunned you and took your credits!"
