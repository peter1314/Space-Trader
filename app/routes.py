"""File for routes"""
# import requests
from flask import render_template, request
from app import app
from .py.player import Player
from .py.game import Game

#file scope player and game variables
player = None
game = None


@app.route('/')
@app.route('/index')
def index():
    """Default route to welcome page"""
    return render_template("WelcomePage.html")

@app.route('/restart', methods=["GET", "POST"])
def restart():
    """Route to restart game"""
    global player
    global game
    player = None
    game = None
    return index()

@app.route('/CharacterCreation')
def character_creation():
    """Route to character creation page"""
    return render_template("CharacterCreation.html")

@app.route("/CharacterDisplay", methods=["POST"])
def character_display():
    """Route to character display page"""
    global player
    #sets the player to a new player created from character creation
    player = Player.create_player_from_form(request.form)

    return render_template("CharacterDisplay.html", playerData=player.to_dict())

@app.route("/Map", methods=["GET", "POST"])
def display_map():
    """Rout to main display page"""
    global game
    global player

    if game is None:
        game = Game(player)
        game.start_game()

    npc_dict = {'id': 0}
    if(player.currentNPC is not None):
        npc_dict = player.currentNPC.to_dict()

    return render_template("Map.html",
                           playerData=player.to_dict(),
                           regionData=player.region.to_dict(player.region, player.pilot_skill, player.merchant_skill),
                           universeData=game.universe.to_dict(player.region, player.pilot_skill, player.merchant_skill),
                           currentNPC=npc_dict)

@app.route("/Map/Travel", methods=["POST"])
def travel():
    global player
    form = request.form
    nextRegion = game.universe.regions[form["nextRegion"]]
    fuelCost = float(form["nextFuelCost"])

    if(not player.check_encounter(nextRegion, fuelCost)):
        player.move_to_region(nextRegion, fuelCost)
        player.region.market.update()
        
    return display_map()

@app.route("/Map/Refuel", methods=["POST"])
def refuel():
    global player

    player.refuel()
    return display_map()

@app.route("/Map/Repair", methods=["POST"])
def repair():
    global player

    player.repair()
    return display_map()

@app.route("/Map/Buy", methods=["POST"])
def buy():
    global player
    form = request.form
    
    for i in range(11):
        player.add_item(player.inventory.types[i], int(form["buyCount" + str(i)]))
        player.region.market.remove_item(player.inventory.types[i],
                                                 int(form["buyCount" + str(i)]))
    player.spend_credits(int(form["buyCost"]))

    return display_map()

@app.route("/Map/Sell", methods=["POST"])
def sell():
    global player
    form = request.form
    
    for i in range(10):
        player.remove_item(player.inventory.types[i], int(form["sellCount" + str(i)]))
        player.region.market.add_item(player.inventory.types[i],
                                              int(form["sellCount" + str(i)]))
    player.add_credits(int(form["sellCost"]))
    return display_map()

@app.route("/Map/NPCFlee", methods=["POST"])
def npc_flee():
    global player

    player.currentNPC.flee(player)
    return display_map()

@app.route("/Map/NPCFight", methods=["POST"])
def npc_fight():
    global player

    player.currentNPC.fight(player)
    return display_map()

@app.route("/Map/NPCForfeit", methods=["POST"])
def npc_forfeit():
    global player

    player.currentNPC.forfeit(player)
    return display_map()

@app.route("/Map/NPCTrade", methods=["POST"])
def npc_trade():
    global player

    player.currentNPC.trade(player)
    return display_map()

@app.route("/Map/NPCHaggle", methods=["POST"])
def npc_haggle():
    global player

    player.currentNPC.haggle(player)
    return display_map()

@app.route("/Map/NPCDismiss", methods=["POST"])
def npc_dismiss():
    global player

    player.currentNPC = None
    return display_map()
