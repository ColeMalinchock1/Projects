# import math
# import matplotlib.pyplot as plt

# def user_input():
#     waypoints = []
#     clean_x_input = clean_y_input = False

#     # Continue getting inputs until x is input
#     while True:
#         x = input("X: ")
#         if x == "x":
#             break
#         else:
#             try:
#                 x = float(x)
#                 clean_x_input = True
#             except ValueError:
#                 clean_x_input = False

#         y = input("Y: ")
#         if y == "x":
#             break
#         else:
#             try:
#                 y = float(y)
#                 clean_y_input = True
#             except ValueError:
#                 clean_y_input = False
        
#         if clean_x_input and clean_y_input:
#             waypoints.append(x)
#             waypoints.append(y)
#             print("Points added")
#         else:
#             print("Invalid input")

#     # Double check that the waypoints are correct
#     print(waypoints)
#     all_good = input("Enter x if the points are incorrect: ")
#     if all_good == "x":
#         waypoints = []
#         user_input()
    
#     return waypoints

# def generate_plot(waypoints):

#     plt.plot(waypoints)

# def main():
#     waypoints = user_input()
#     print(waypoints)
#     generate_plot()

#     get_lookahead()

# if __name__ == "__main__":
#     main()


import tkinter as tk
import math

class PointClickerApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=400, height=400, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.waypoints = []
        self.click_num = 0

    def get_lookahead(self, current_x, current_y, waypoints):

        # Sets the closest point as none to start
        closest_point = (None, None)

        m1 = m2 = None

        # If it is the first time the closest point is being found
        for i in range(len(waypoints) - 1):
            waypoint_start = waypoints[i]
            waypoint_end = waypoints[i + 1]

            # Get the slope between the two waypoints
            try:
                m1 = (waypoint_end[1] - waypoint_start[1]) / (waypoint_end[0] - waypoint_start[0])
            except ZeroDivisionError:
                x = waypoint_start[0]
                y = (waypoint_start[1] + waypoint_end[1]) / 2

            # The slope for the perpendicular line to the vehicle is the reciprical
            try:
                m2 = -1.0 / m1
            except ZeroDivisionError:
                x = (waypoint_start[0] + waypoint_end[0]) / 2
                y = waypoint_start[1]

            if m1 is not None and m2 is not None:
                # Calculate the b value for y = mx + b equation between the two waypoints
                b1 = waypoint_start[1] - m1 * waypoint_start[0]

                # Calculate the b value for the y = mx + b equation from the vehicle to the perpendicular point between the two waypoints
                b2 = current_x - m2 * current_y

                # Calculate the x value
                x = (b2 - b1) / (m1 - m2)

                # Calculate the y value
                y = m1 * x + b1
        
            # Minimum and maximum x
            x_min = min(waypoint_start[0], waypoint_end[0])
            x_max = max(waypoint_start[0], waypoint_end[0])

            # Check that they are within the range
            if x < x_min:
                if waypoint_start[0] > waypoint_end[0]:
                    x = waypoint_end[0]
                    y = waypoint_end[1]
                else:
                    x = waypoint_start[0]
                    y = waypoint_start[1]
            elif x > x_max:
                if waypoint_start[0] < waypoint_end[0]:
                    x = waypoint_end[0]
                    y = waypoint_end[1]
                else:
                    x = waypoint_start[0]
                    y = waypoint_start[1]
        
            # Check for the first iteration
            if closest_point[0] is None:
                closest_point = (x, y)

            if (math.sqrt((x - current_x)**2 + (y - current_y)**2) 
                < math.sqrt((closest_point[0] - current_x)**2 + (closest_point[1] - current_y)**2)):
                closest_point = (x, y)
            
        return closest_point

    def on_click(self, event):
        if (self.click_num > 0):
            self.click_num = 0
            self.reset_plot(self.waypoints)

        x, y = event.x, event.y
        print("Clicked point:", x, y)

        # Get the interception points
        int_x, int_y = self.get_lookahead(x, y, self.waypoints)
        self.add_point(x, y)
        self.add_point(int_x, int_y)
        self.add_line(x, y, int_x, int_y)
        self.click_num += 1
    
    def add_point(self, x, y):
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill = "red")

    def add_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, fill="blue")  # Connect waypoints with blue lines
        

    def reset_plot(self, waypoints):
        self.canvas.delete("all")
        self.waypoints = waypoints

        # Plot the original plot
        for i in range(len(self.waypoints) - 1):
            x1, y1 = self.waypoints[i]
            x2, y2 = self.waypoints[i + 1]
            self.add_line(x1, y1, x2, y2)
            self.add_point(x1, y1)

        # Plot the last waypoint
        x_last, y_last = self.waypoints[-1]
        self.add_point(x_last, y_last)

def main():
    root = tk.Tk()
    app = PointClickerApp(root)

    # Define a list of waypoints
    waypoints = [(100, 100), (200, 200), (300, 300)]

    # Plot the waypoints with lines connecting them
    app.reset_plot(waypoints)

    root.mainloop()

if __name__ == "__main__":
    main()

