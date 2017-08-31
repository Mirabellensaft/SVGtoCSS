def make_centroid(polygon_coordinates):
    """Takes in triangle coordinates and returns
       the coordinates of the centroid"""

    x_values = 0
    y_values = 0

    if type(polygon_coordinates) == str:
        polygon_coordinates = polygon_coordinates.replace(',', '')
        polygon_coordinates = polygon_coordinates.replace('%', '')
        polygon_coordinates = polygon_coordinates.split()

        for i in range(len(polygon_coordinates)):
            polygon_coordinates[i] = float(polygon_coordinates[(i)][0:4])


    for i in range(len(polygon_coordinates)):
        if i%2 == 0:
            x_values += polygon_coordinates[i]
        else:
            y_values += polygon_coordinates[i]

    # calculates x- and y-values of the centroid
    x_value = x_values/3
    y_value = y_values/3

    x_value = round(x_value, 2)
    y_value = round(y_value, 2)
    #müssen die coordinaten durchgeschliffen werden?
    centroid = [x_value, y_value, polygon_coordinates]

    return centroid
