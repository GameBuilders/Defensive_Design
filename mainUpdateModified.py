"""
Handles any updating of game objects. This is called
once per game loop.
"""
def update():
    global GameState
    if(GameState == "GAME"):
        # Update the enemies
        livesLost, gainedPoints = EnemyManager.update(Map)
        Data.lives -= livesLost
        Data.score += gainedPoints
        # Update the UI
        UI.update(Data)
        # Check if the game is over
        if(Data.lives <= 0):
            GameState = "GAME_LOST" # The game is over
            UI.showDefeat()
