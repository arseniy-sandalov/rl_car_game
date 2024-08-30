import pygame
import random

class BaseObject:
    def __init__(self, map_width, map_height, grid_size, existing_objects):
        self.map_width = map_width
        self.map_height = map_height
        self.grid_size = grid_size
        while True:
            self.x = random.randint(0, self.map_width - 1)
            self.y = random.randint(0, self.map_height - 1)

            if not any(obj.x == self.x and obj.y == self.y for obj in existing_objects):
             
                break
  
    


class Car(BaseObject):
    
        
    def __init__(self, grid_size, texture_file, map_width, map_height, existing_objects):
        super().__init__(map_width, map_height, grid_size, existing_objects)
        self.grid_size = grid_size
        self.texture = pygame.image.load(texture_file)
        self.texture = pygame.transform.scale(self.texture, (grid_size, grid_size))
        self.direction = "north"

        while True:
            self.x = random.randint(0, map_width - 1)
            self.y = random.randint(0, map_height - 1)

        
            collides = any((self.x, self.y) == (obj.x, obj.y) for obj in existing_objects)

            if not collides:
                self.initial_x = self.x 
                self.initial_y = self.y  
                break

    def draw(self, surface):
        rotated_texture = self._rotate_texture() 
        surface.blit(rotated_texture, (self.x * self.grid_size, self.y * self.grid_size))

    def _rotate_texture(self):
        if self.direction == "north":
            return self.texture
        elif self.direction == "south":
            return pygame.transform.rotate(self.texture, 180)
        elif self.direction == "east":
            return pygame.transform.rotate(self.texture, -90)
        elif self.direction == "west":
            return pygame.transform.rotate(self.texture, 90)

    def go_north(self):
        if self.y > 0:
            self.y -= 1
            self.direction = "north"

    def go_south(self):
        if self.y < self.map_height - 1:
            self.y += 1
            self.direction = "south"

    def go_east(self):
        if self.x < self.map_width - 1:
            self.x += 1
            self.direction = "east"

    def go_west(self):
        if self.x > 0:
            self.x -= 1
            self.direction = "west"

    def reset(self):
        self.x = self.initial_x  
        self.y = self.initial_y



class Parking(BaseObject):
    
    def __init__(self, x, y, grid_size, texture_file, map_width, map_height, existing_objects):
        super().__init__(map_width, map_height, grid_size, existing_objects)
        self.grid_size = grid_size
        self.texture = pygame.image.load('parking.jpg')  
        self.texture = pygame.transform.scale(self.texture, (grid_size, grid_size))  

    def draw(self, surface):
        surface.blit(self.texture, (self.x * self.grid_size, self.y * self.grid_size))


class Obstacle(BaseObject):
  
    def __init__(self, map_width, map_height, grid_size, existing_objects):
        super().__init__(map_width, map_height, grid_size, existing_objects)        

    def draw(self, surface):
        surface.blit(self.texture, (self.x * self.grid_size, self.y * self.grid_size))

class People(Obstacle):
    def __init__(self, map_width, map_height, grid_size , existing_objects):
        super().__init__(map_width, map_height, grid_size, existing_objects)
        self.grid_size = grid_size
        self.texture = pygame.image.load('person_texture.png')
        self.texture = pygame.transform.scale(self.texture, (grid_size, grid_size))

class Wall(Obstacle):
    def __init__(self, map_width, map_height,grid_size, existing_objects):
        super().__init__(map_width, map_height, grid_size, existing_objects)
        self.grid_size = grid_size
        self.texture = pygame.image.load('wall_texture.png')
        self.texture = pygame.transform.scale(self.texture, (grid_size, grid_size))
        

class Animals(Obstacle):
    def __init__(self, map_width, map_height,grid_size, existing_objects):
        super().__init__(map_width, map_height, grid_size, existing_objects)
        self.grid_size = grid_size
        self.texture = pygame.image.load('dog_texture.png')
        self.texture = pygame.transform.scale(self.texture, (grid_size, grid_size))
