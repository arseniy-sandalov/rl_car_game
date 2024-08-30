import pygame
from grid_map import create_map, draw_map
from objects import *
from logic import Counter, Controller, StepCounter
from ai import *
from restart import *
import time
import visual 



AI = 1

pygame.font.init()
font_path = 'arial.ttf'  
font = pygame.font.Font(font_path, 36)
 
frame_duration = 0.0001


pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1000, 1000
ROWS, COLS = 10, 10
GRID_SIZE = WIDTH // COLS
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Map")
map_width = 10  
map_height = 10 
map_grid = create_map(map_width, map_height)






existing_objects = []

car = Car( GRID_SIZE, 'car_on_grass.png', map_width, map_height, existing_objects)  
parking = Parking(5,4,GRID_SIZE, 'parking.jpg', map_width, map_height, existing_objects)
existing_objects.append(parking)

people_list = []
num_people = 3  

animals_list = []
num_animals = 3

walls_list = []
num_walls = 6

for _ in range(num_people):
    #person = People(random.randint(0, map_width - 1), random.randint(0, map_height - 1), GRID_SIZE, existing_objects)
    person = People(map_width, map_height, GRID_SIZE, existing_objects)
    people_list.append(person)
    existing_objects.append(person)

#person = People(map_width, map_height, GRID_SIZE)
for _ in range(num_animals):
    #person = People(random.randint(0, map_width - 1), random.randint(0, map_height - 1), GRID_SIZE, existing_objects)
    animal = Animals(map_width, map_height, GRID_SIZE, existing_objects)
    animals_list.append(animal)
    existing_objects.append(animal)

for _ in range(num_walls):
    #person = People(random.randint(0, map_width - 1), random.randint(0, map_height - 1), GRID_SIZE, existing_objects)
    wall = Wall(map_width, map_height, GRID_SIZE, existing_objects)
    walls_list.append(wall)
    existing_objects.append(wall)



#animals = Animals (map_width, map_height, GRID_SIZE, existing_objects)

car_on_parking_texture = pygame.image.load('car_on_parking.jpg')  # Load car on parking texture
car_on_parking_texture = pygame.transform.scale(car_on_parking_texture, (GRID_SIZE, GRID_SIZE)) 

q_table = np.zeros((12, 12, 4))

actions = {
    pygame.K_UP: 0,
    pygame.K_DOWN: 1,
    pygame.K_LEFT: 2,
    pygame.K_RIGHT: 3
}


counter = Counter()
step_counter = StepCounter(car)
controller = Controller(car,step_counter)


q_table = create_q_val_matrix(map_width+2,map_height+2,len(actions))

score = 0
ai = AI



running = True
while running:

    
    draw_map(win, map_grid, car, parking , animals_list, people_list, walls_list)  
    counter.start_counting(car,parking)

    if ai is 1:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_state = (car.x, car.y)
        
        action = choose_action(current_state, q_table, actions )

        if action == actions[pygame.K_UP]:
            controller.handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}), existing_objects, parking, ai)
        elif action == actions[pygame.K_DOWN]:
            controller.handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}), existing_objects, parking, ai)
        elif action == actions[pygame.K_LEFT]:
            controller.handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT}), existing_objects, parking, ai)
        elif action == actions[pygame.K_RIGHT]:
            controller.handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT}), existing_objects, parking, ai)

        next_state = (car.x, car.y)
        reward = calculate_reward(car, parking, animals_list, people_list, walls_list)
        score =+  reward
    
        q_learning(current_state, reward, next_state, action, q_table)

      
            

        

        game_matrix = create_game_matrix(car, parking, animals_list, people_list, walls_list, map_width, map_height)
        update_game_matrix(game_matrix, car, parking, animals_list, people_list, walls_list) 
        # reward_matrix = create_reward_matrix(car, parking, animals_list, people_list, walls_list, map_width, map_height )
        # update_reward_matrix(car, parking, animals_list, people_list, walls_list, reward_matrix)
        #updated_reward_matrix = create_updated_reward_matrix(car, parking, animals_list, people_list, walls_list)

        print() 
        for i in range(len(game_matrix)):
            print(' '.join(game_matrix[i]) + "  |")


        print('-' * (len(game_matrix[0]) * 2 + 3))


        # for i in range(len(updated_reward_matrix)):
        #     print(' '.join(str(cell) for cell in updated_reward_matrix[i]) + "  |")
    
    else:

        # # TODO: СДЕЛАТЬ РАЗНЫЕ ТЕКСТУРКИ КОГДА МАШИНА ПОДЪЕЗЖАЕТ С РАЗНЫХ СТОРОН....
        # if car.x == parking.x and car.y == parking.y:
        #     parking.texture = car_on_parking_texture
        
            
        
        parking.texture = pygame.image.load('parking.jpg')
        parking.texture = pygame.transform.scale(parking.texture, (GRID_SIZE, GRID_SIZE))
        counter.is_parked = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            controller.handle_event(event, existing_objects, parking, ai)  
       
        
        


    score_text = font.render(f'AI Reward: {score}', True, (255, 255, 255)) 
    score_rect = score_text.get_rect()
    score_rect.topright = (WIDTH - 20, 20)  

    win.blit(score_text, score_rect)
    
    time.sleep(frame_duration)
    pygame.display.update()
    #clock.tick(FPS)

successful_parkings = counter.get_count()
total_steps = step_counter.get_steps()
print(f"Number of successful parkings: {successful_parkings}")
print(f"Total steps taken: {total_steps}")

step_history = step_counter.get_history()

for step, position in step_history.items():
    step_number = step
    x, y = position
    print(f"At step {step_number}, car was at position: ({x}, {y})")

if ai == 1:
    visual.plot_heatmap(car, step_history, animals_list, walls_list, people_list, parking)
counter.clear_count_file()

pygame.quit()


