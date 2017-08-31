def make_raw_coordinates_list():
    """Takes data from a file and returns a
       list with all raw coordinates as floats"""

    raw_coordinates_list = []

    f = open('dump.txt','r')
    for l in f:
        line = str(l)
        data_raw = line.split(" ")
        print (data_raw, len(data_raw))

        if len(data_raw) == 7:
            for i in range(6):
                item = float(data_raw[i])
                raw_coordinates_list.append(item)

    return raw_coordinates_list


def make_coordinates_percent(raw_coordinates, factor, zero_diff):
    """Takes the raw coordinates as floats and returns them in their percent value"""

    coordinates_list = []
    x_min = zero_diff[0]
    y_min = zero_diff[1]

    #set_coordinates zero
    Liste = []
    for i in range(len(raw_coordinates)):
        if i%2 == 0:
            item = raw_coordinates[i] - x_min
            Liste.append(item)
        else:
            item = raw_coordinates[i] - y_min
            Liste.append(item)

    for i in range(len(Liste)):
        item = Liste[i] * factor
        item = round(item, 3)
        coordinates_list.append(item)

    return coordinates_list


def make_factor(raw_coordinates_list, zero_diff):
    """returns the factor, to convert coordinates from px to percent"""

    max_value = 0
    x_min = zero_diff[0]
    y_min = zero_diff[1]
    zeroed_raw_coordinates =[]

    for i in range(len(raw_coordinates_list)):
        if i%2 == 0:
            item = raw_coordinates_list[i] - x_min
            zeroed_raw_coordinates.append(item)
        else:
            item = raw_coordinates_list[i] - y_min
            zeroed_raw_coordinates.append(item)

    for i in range(len(zeroed_raw_coordinates)):
        if zeroed_raw_coordinates[i] > max_value:
            max_value = zeroed_raw_coordinates[i]

    factor = 100/max_value

    return factor

def set_zero_factor(raw_coordinates_list):
    """Finds the smalles x- and y-value for
       setting them zero. Returns a tuple"""

    x_min = 1000
    y_min = 1000

    for i in range(len(raw_coordinates_list)):
        # find max
        if i%2 == 0:
            if raw_coordinates_list[i] < x_min:
                x_min = raw_coordinates_list[i]
        else:
            if raw_coordinates_list[i] < y_min:
                y_min = raw_coordinates_list[i]

    print ("x_min", x_min)
    print ("y_min", y_min)

    min_values = (x_min, y_min)

    return min_values
