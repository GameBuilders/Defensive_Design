import pygame
import enemy
import Queue

class TowerManager:

   
    spritegroup = pygame.sprite.Group()

    SPAWN_EVENT_BASIC = pygame.USEREVENT


    def __init__(self, size):
        self.last_wave_time = pygame.time.get_ticks()
        self.last_update_time = pygame.time.get_ticks()
        self.size = size

    def draw(self, surface):
        TowerManager.spritegroup.draw(surface)
        

    def spawnTower(self, event, coordinates):
        if(event.type == TowerManager.SPAWN_EVENT_BASIC):
            TowerManager.towers.append(towers.Tower(coordinates[0],coordinates[1], TowerManager.spritegroup, self.size))


if __name__ == '__main__':
    execfile("main.py")
