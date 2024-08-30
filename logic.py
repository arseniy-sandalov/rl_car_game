import pygame
import sys
import subprocess
import restart

python = sys.executable

class Controller:
    def __init__(self, car, step_counter):
        self.car = car
        self.step_counter = step_counter

    def handle_event(self, event, existing_objects, Parking, ai):
        if event.type == pygame.KEYDOWN:
            prev_x, prev_y = self.car.x, self.car.y 
            if event.key == pygame.K_UP:
                self.car.go_north()
            elif event.key == pygame.K_DOWN:
                self.car.go_south()
            elif event.key == pygame.K_LEFT:
                self.car.go_west()
            elif event.key == pygame.K_RIGHT:
                self.car.go_east()

         
            self.step_counter.increment(self.car, Counter, Parking, ai)
            self.step_counter.check_collision_restart(self.car, Parking, existing_objects, ai)
            
            

            
    
        
    
   



class Counter:
    def __init__(self):
        self.count = self.load_count()  
        self.is_parked = False
        self.temp = 0

    def start_counting(self, car, parking):
        if car.x == parking.x and car.y == parking.y and not self.is_parked:
            self.count += 1
            self.is_parked = True
            self.save_count()  # Save count to file when incremented

    def get_count(self):
        return self.count

    def save_count(self):
        with open("parking_count.txt", "w") as file:
            file.write(str(self.count))

    def load_count(self):
        try:
            with open("parking_count.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0  # Return 0 if the file doesn't exist or count couldn't be loaded

    def clear_count_file(self):
        with open("parking_count.txt", "w") as file:
            file.write("0")  # Write 0 to the file to clear the count






class StepCounter:
    def __init__(self, car):
        self.steps = 0
        self.history = {0: (car.x, car.y)}
        self.counter = Counter()

    def increment(self, car, counter, parking, ai):
        self.steps += 1
        self.history[self.steps] = (car.x, car.y)
        
        if self.steps >= 2:
            current_position = self.history[self.steps]
            previous_position = self.history[self.steps - 1]
            if current_position == previous_position:
                if ai == 1:
                    car.reset()
                else:
                     restart.restart_game_no()

        if car.x == parking.x and car.y == parking.y:
            print("OK OK OK OK OK") 
            self.counter.start_counting(car, parking)  
            successful_parkings = self.counter.get_count()
            if ai == 1:
                    car.reset()
            else:
                restart.restart_game_no()
    
    def check_collision_restart(self, car, parking, existing_objects, ai):
        for obj in existing_objects:
            if (car.x, car.y) == (obj.x, obj.y) and obj != parking:
                print("Collision detected! Restarting game...")

                if ai == 1:
                    car.reset()
                else:
                     restart.restart_game_no()
                
    def get_steps(self):
        return self.steps

    def get_history(self):
        return self.history

    def reset(self):
        self.steps = 0
        self.history.clear()
    

