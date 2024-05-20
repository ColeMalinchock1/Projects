import tkinter as tk
import numpy as np

# Define the hard-coded path points
start = (50, 50)
goal = (550, 50)

# RRT parameters
step_size = 10
max_iterations = 1000

class RRT:
    def __init__(self, start, goal, obstacle_list, step_size, max_iterations):
        self.start = np.array(start)
        self.goal = np.array(goal)
        self.obstacle_list = obstacle_list
        self.step_size = step_size
        self.max_iterations = max_iterations
        self.nodes = [self.start]
        self.node_parent = {tuple(self.start): None}

    def plan(self):
        for i in range(self.max_iterations):
            rnd_point = self.get_random_point()
            nearest_node = self.get_nearest_node(rnd_point)
            new_node = self.steer(nearest_node, rnd_point)
            
            if not self.check_collision(nearest_node, new_node):
                self.nodes.append(new_node)
                self.node_parent[tuple(new_node)] = nearest_node
                if np.linalg.norm(new_node - self.goal) < self.step_size:
                    return self.reconstruct_path(new_node)
        
        return None

    def get_random_point(self):
        return np.random.rand(2) * [600, 400]

    def get_nearest_node(self, rnd_point):
        distances = [np.linalg.norm(node - rnd_point) for node in self.nodes]
        return self.nodes[np.argmin(distances)]

    def steer(self, from_node, to_point):
        direction = to_point - from_node
        distance = np.linalg.norm(direction)
        direction = direction / distance
        new_node = from_node + direction * self.step_size
        return new_node

    def check_collision(self, from_node, to_node):
        for (ox, oy, w, h) in self.obstacle_list:
            if self.line_intersects_rect(from_node, to_node, (ox - w / 2, oy - h / 2, w, h)):
                return True
        return False

    def line_intersects_rect(self, p1, p2, rect):
        (rx, ry, rw, rh) = rect
        lines = [
            ((rx, ry), (rx + rw, ry)),
            ((rx, ry), (rx, ry + rh)),
            ((rx + rw, ry), (rx + rw, ry + rh)),
            ((rx, ry + rh), (rx + rw, ry + rh))
        ]
        for (l1, l2) in lines:
            if self.check_line_intersection(p1, p2, l1, l2):
                return True
        return False

    def check_line_intersection(self, p1, p2, q1, q2):
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
        
        return ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2)

    def reconstruct_path(self, node):
        path = []
        while node is not None:
            path.append(node)
            node = self.node_parent[tuple(node)]
        path.reverse()
        return path

class RRTApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=600, height=400)
        self.canvas.pack()

        self.obstacles = []
        self.canvas.bind("<Button-1>", self.add_obstacle)

        self.draw_path([start, goal])

    def add_obstacle(self, event):
        print("Adding obstacle")
        x, y = event.x, event.y
        size = 40
        self.canvas.create_rectangle(x - size / 2, y - size / 2, x + size / 2, y + size / 2, fill="red")
        self.obstacles.append((x, y, size, size))
        self.recalculate_path()

    def draw_path(self, path):
        self.canvas.delete("path")
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2, tags="path")

    def recalculate_path(self):
        print("Recalculating path with obstacles:", self.obstacles)
        rrt = RRT(start, goal, self.obstacles, step_size, max_iterations)
        new_path = rrt.plan()
        if new_path:
            print("New path found:", new_path)
            self.canvas.delete("all")
            for (x, y, w, h) in self.obstacles:
                self.canvas.create_rectangle(x - w / 2, y - h / 2, x + w / 2, y + h / 2, fill="red")
            self.draw_path(new_path)
        else:
            print("No path found")

if __name__ == "__main__":
    root = tk.Tk()
    app = RRTApp(root)
    root.mainloop()
