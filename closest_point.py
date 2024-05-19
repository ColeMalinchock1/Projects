def get_lookahead(current_x, current_y, waypoints):

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

def main():
    get_lookahead()

if __name__ == "__main__":
    main()
