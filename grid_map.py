import pygame

GRID_SIZE = 100  

def create_map(width, height):
    grid = []
    for row in range(height):
        grid.append([])
        for _ in range(width):
            grid[row].append(0) 

    return grid

def draw_map(surface, grid, car, parking, animals_list, people_list, walls_list):
    texture = pygame.image.load('grass_texture_50x50.jpg')  
    texture = pygame.transform.scale(texture, (GRID_SIZE, GRID_SIZE))


    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            surface.blit(texture, (x * GRID_SIZE, y * GRID_SIZE))

            pygame.draw.rect(surface, (0, 0, 0), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
           
    car.draw(surface) 
    parking.draw(surface)
    #animals.draw(surface)
    
    for animal in animals_list:
        animal.draw(surface)

    for person in people_list:
        person.draw(surface)

    for wall in walls_list:
        wall.draw(surface)
    
