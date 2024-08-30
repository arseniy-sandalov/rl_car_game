import numpy as np 
import math

alpha = 0.2 
gamma = 0.9  
epsilon = 0.3 

def get_state(car, parking, animals_list, people_list, walls_list):
    for obj in animals_list + people_list + walls_list:
        if (car.x, car.y) == (obj.x, obj.y):
            return 'obstacle_collision'

    if (car.x, car.y) == (parking.x, parking.y):
        return 'parked'

   
    if car.x == 0 or car.x == 11 or car.y == 0 or car.y == 11:
        return 'wall_collision'

    return 'normal'


def create_game_matrix(car, parking, animals_list, people_list, walls_list, map_width, map_height):
    game_matrix = [['.' for _ in range(map_width)] for _ in range(map_height)]

    
    game_matrix[car.y][car.x] = 'c'

    game_matrix[parking.y][parking.x] = 'p'

    
    for animal in animals_list:
        game_matrix[animal.y][animal.x] = 'o'

    for person in people_list:
        game_matrix[person.y][person.x] = 'o'

    for wall in walls_list:
        game_matrix[wall.y][wall.x] = 'o'

    return game_matrix

def update_game_matrix(game_matrix, car, parking, animals_list, people_list, walls_list):
    for row in range(len(game_matrix)):
        for col in range(len(game_matrix[0])):
            game_matrix[row][col] = '.'  

   
    game_matrix[car.y][car.x] = 'c'

    
    game_matrix[parking.y][parking.x] = 'p'

    
    for animal in animals_list:
        game_matrix[animal.y][animal.x] = 'o'

    for person in people_list:
        game_matrix[person.y][person.x] = 'o'

    for wall in walls_list:
        game_matrix[wall.y][wall.x] = 'o'




# def create_updated_reward_matrix(car, parking, animals_list, people_list, walls_list):
#     reward_matrix = [[-10 if i == 0 or i == 11 or j == 0 or j == 11 else -1 for i in range(12)] for j in range(12)]

    
#     reward_matrix[car.y + 1][car.x + 1] = 1

    
#     reward_matrix[parking.y + 1][parking.x + 1] = 100

    
#     for animal in animals_list:
#         reward_matrix[animal.y + 1][animal.x + 1] = -10

#     for person in people_list:
#         reward_matrix[person.y + 1][person.x + 1] = -10

#     for wall in walls_list:
#         reward_matrix[wall.y + 1][wall.x + 1] = -10

#     return reward_matrix







def create_q_val_matrix (environment_rows, environment_colomns, actions):
    # map_width, map_lenght, actions like car.go_north() and etc...
    q_table = np.zeros ((environment_rows, environment_colomns, actions)) 
    
    return q_table


def q_learning(state, reward, next_state, action, q_table):
    current_q = q_table[state[0]][state[1]][action]

    
    max_future_q = np.max(q_table[next_state[0]][next_state[1]])
    new_q = (1 - alpha) * current_q + alpha * (reward + gamma * max_future_q)
    
    q_table[state[0]][state[1]][action] = new_q


def choose_action(state, q_table, actions):
    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice(list(actions.values()))
    else:
        return np.argmax(q_table[state[0]][state[1]])
    

def initialize_reward_matrix(width, height, obstacles):
    reward_matrix = np.random.randint(0, 11, size=(height, width))

    # Assign -10 to obstacle positions
    for obstacle in obstacles:
        reward_matrix[obstacle.y][obstacle.x] = -10

    return reward_matrix



# def calculate_reward(car, parking, animals_list, people_list, walls_list):
#     car_pos = (car.x, car.y)
#     reward = -1  # Default reward

#     # Check if the car is parked
#     if car_pos == (parking.x, parking.y):
#         return +100  # Positive reward when the car is parked

#     # Check distances from obstacles
#     for obj in animals_list + people_list + walls_list:
#         obj_pos = (obj.x, obj.y)
#         distance = max(abs(obj_pos[0] - car_pos[0]), abs(obj_pos[1] - car_pos[1]))

#         if distance == 1:
#             reward = -5  # Within 1 step range
#         elif distance == 2:
#             reward = -2  # Within 2 step range

#         if (car.x, car.y) == (obj.x, obj.y):
#             return -50 # Negative reward for collision with obstacles

#     # Check proximity to the parking space
#     parking_pos = (parking.x, parking.y)
#     parking_distance = max(abs(parking_pos[0] - car_pos[0]), abs(parking_pos[1] - car_pos[1]))

#     if parking_distance == 3:
#         reward += 5  # Parking is 1 step near
#     elif parking_distance == 2:
#         reward += 10  # Parking is 2 steps near
#     elif parking_distance == 1:
#         reward += 15  # Parking is 3 steps near
#     elif parking_distance == 4: 
#         reward += 0

#     # Increase positive reward for alignment with parking without obstacles in between
#     if car.x == parking.x:
#         obstacles_between = any(obj.x == car.x and obj.y in range(min(car.y, parking.y), max(car.y, parking.y) + 1) for obj in animals_list + people_list + walls_list)
#         if not obstacles_between:
#             reward += 20
#     elif car.y == parking.y:
#         obstacles_between = any(obj.y == car.y and obj.x in range(min(car.x, parking.x), max(car.x, parking.x) + 1) for obj in animals_list + people_list + walls_list)
#         if not obstacles_between:
#             reward += 20

#     # Increase negative reward for hitting the wall
#     if car.x == 0 or car.x == 11 or car.y == 0 or car.y == 11:
#         return -100  # Negative reward for hitting the wall

#     return reward





GRID_SIZE = 12 

def calculate_reward(car, parking, animals_list, people_list, walls_list):
    car_pos = (car.x, car.y)
    parking_pos = (parking.x, parking.y)
    distance_to_parking = np.sqrt((car_pos[0] - parking_pos[0])**2 + (car_pos[1] - parking_pos[1])**2)    
    distance_reward = -np.exp(0.5 * distance_to_parking)

    
    if car_pos == parking_pos:
        return 100 + distance_reward  

    reward = -3 + distance_reward  # - 3 is the default reward for a step. 

    for obj in animals_list + people_list + walls_list:
        obj_pos = (obj.x, obj.y)
        distance = np.sqrt((obj_pos[0] - car_pos[0])**2 + (obj_pos[1] - car_pos[1])**2)

        if distance < 2.0:
            reward -= 5 * np.exp(0.1 * distance)  

        if car_pos == obj_pos:
            return -50
    
    parking_distance = np.sqrt((parking_pos[0] - car_pos[0])**2 + (parking_pos[1] - car_pos[1])**2)
   
    if parking_distance == 1.0:
        reward += 15 
    elif parking_distance == 2.0:
        reward += 10  
    elif parking_distance == 3.0:
        reward += 5  

   
    if car.x == parking.x:
        obstacles_between = any(obj.x == car.x and obj.y in range(min(car.y, parking.y), max(car.y, parking.y) + 1) for obj in animals_list + people_list + walls_list)
        if not obstacles_between:
            reward += 20
    elif car.y == parking.y:
        obstacles_between = any(obj.y == car.y and obj.x in range(min(car.x, parking.x), max(car.x, parking.x) + 1) for obj in animals_list + people_list + walls_list)
        if not obstacles_between:
            reward += 20

    
    if car.x == 0 or car.x == 11 or car.y == 0 or car.y == 11:
        return -100  

    return reward