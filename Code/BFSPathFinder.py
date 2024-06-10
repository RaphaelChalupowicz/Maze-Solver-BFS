import colorsys

from Point import *
import matplotlib.pyplot as plt
import numpy as np
import cv2

""" DIRECTIONS 

This var represent all directions that BFS needs to know in order to make the search.

Point(0, -1) -> UP
Point(0, 1) -> DOWN
Point(1, 0) -> RIGHT
Point(-1, 0) -> LEFT

"""


class BFSPathFinder:  # Define a class for BFS path finding
    seeBfs = False  # For Debugging

    def __init__(self, img, h, w):
        self.img = img  # setting image
        self.height = h  # setting image height pixels
        self.width = w  # setting image width pixels
        self.dir4 = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]  # setting all possible moving directions

    def find_path(self, start, end):  # Method to find a path between two points using BFS
        const = 10000
        found = False
        q = []  # Queue for BFS
        v = [[0 for j in range(self.width)] for i in range(self.height)]  # Visited array
        parent = [[Point() for j in range(self.width)] for i in range(self.height)]  # Parent array

        q.append(start)  # Add the start point to the queue
        v[start.y][start.x] = 1  # Mark the start point as visited

        while len(q) > 0:  # Loop until queue is empty
            current_point = q.pop(0)  # Pop the front element of the queue
            for d in self.dir4:  # Check all directions from the current point
                cell = current_point + d  # Calculate the next cell
                if (self.is_valid(cell) and v[cell.y][cell.x] == 0 and
                        (self.is_valid_color(self.img[cell.y][cell.x]))):  # Check if the cell is valid and not visited and has valid color
                    q.append(cell)  # Add the cell to the queue
                    v[cell.y][cell.x] = v[current_point.y][current_point.x] + 1  # Mark the cell as visited

                    if self.seeBfs:  # if debug is ture then show where searched
                        self.img[cell.y][cell.x] = list(reversed([i * 255 for i in colorsys.hsv_to_rgb(v[cell.y][cell.x] / const, 1, 1)]))  # coloring the searched cell

                    parent[cell.y][cell.x] = current_point
                    if cell == end:  # Check if the end point is reached
                        found = True
                        del q[:]  # Clear the queue
                        break  # Exit the loop if end point is found
                    elif(len(q) % 50 == 0 and self.seeBfs == True):
                        cv2.waitKey(1)
                        cv2.imshow("Image", self.img)  # update changes


        path = [] # List to store the path
        if found:
            current_point = end  # Start from the end point
            while current_point != start:  # Reconstruct the path by backtracking from end to start
                path.append(current_point)  # Add the current point to the path
                current_point = parent[current_point.y][current_point.x]  # Move to the parent
            path.append(current_point)  # Add the start point to the path
            path.reverse()  # Reverse the path to get it in correct order

            for point in path:  # Mark the path on the image
                for i in range(-1, 1):
                    self.img[point.y + i][point.x + i] = [170, 178, 32]  # Path Color

            print("Path Found")
        else:
            print("Path Not Found")

    def is_valid(self, point):  # Method to check if a point is valid (inside the image bounds)
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def is_valid_color(self, color):  # Method to check if a color is valid (not black)
        return color[0] != 0 or color[1] != 0 or color[2] != 0
