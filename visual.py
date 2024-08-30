import matplotlib.pyplot as plt
import numpy as np

def plot_heatmap(car, step_history, animals_list, walls_list, people_list, parking):
    x = [coords[0] for coords in step_history.values()]
    y = [coords[1] for coords in step_history.values()]

    plt.figure(figsize=(8, 8))

    for obstacle_list in [animals_list, walls_list, people_list]:
        for obstacle in obstacle_list:
            plt.scatter(obstacle.x, 9 - obstacle.y, color='red', marker='s', s=100)

    plt.scatter(parking.x, parking.y, color='green', marker='P', s=150, label='Parking Position')
    plt.scatter(car.initial_x, 9 - car.initial_y, color='blue', marker='o', s=200, label='Initial Car Position')

   
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=(10, 10))
    extent = [xedges[0], xedges[-1], yedges[-1], yedges[0]]

    plt.imshow(heatmap.T, extent=extent, cmap='coolwarm', alpha=0.7, interpolation='gaussian')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Car Movement Heatmap')
    plt.colorbar(label='Number of Visits')
    plt.legend()

    plt.xlim(0, 12)
    plt.ylim(0, 12)
    plt.grid(True)
    plt.show()