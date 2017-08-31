import xml.sax
import math
import itertools

""" This parser reads .svg files. The output are coordinates, formatted to
    CSS clip-paths for polygons."""

class raw_Coordinates(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""


    def startElement(self, tag, attributes):

        self.CurrentData = tag

        # This section adds layer information
        # In the future, the program can identify animation stages by layer information
        # if tag == "g":
            # layer = attributes["inkscape:label"]
            # if layer == "" string aus eingabe! oder hardcode?
            # target.write("***{}***\n" .format(layer))
            # target.write("\n")

        if tag == "path":
            identity = attributes["id"]
            if identity[0:4] == "path":

                # parsing the coordinates
                content = attributes["d"]

                # coordinates for calculating in percent
                polygon_coordinates_raw = make_coordinates_raw(content)

                # Data is written into a file, as the parser cannot return things? wtf?
                dump.write("{}\n" .format(polygon_coordinates_raw))


    def endElement(self, tag):
      self.CurrentData = ""


class Coordinates(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""


    def startElement(self, tag, attributes):

        self.CurrentData = tag

        # This section adds layer information
        # In the future, the program can identify animation stages by layer information
        # if tag == "g":
            # layer = attributes["inkscape:label"]
            # if layer == "" string aus eingabe! oder hardcode?
            # target.write("***{}***\n" .format(layer))
            # target.write("\n")

        if tag == "path":
            identity = attributes["id"]
            if identity[0:4] == "path":
                polygon_id = identity
                style = attributes["style"]

                style_dictionary = make_style_dictionary(style)
                background = style_dictionary['fill']

                # parsing the coordinates
                content = attributes["d"]

                # coordinates for calculating in percent
                polygon_coordinates_raw = make_coordinates_raw(content)

                # triangle_data = [polygon_id, background, polygon_coordinates]
                # Data is written into a file, as the parser cannot return things? wtf?
                dump.write("{} {} {}\n" .format(polygon_id, background, polygon_coordinates_raw))


    def endElement(self, tag):
      self.CurrentData = ""


class divGenerator(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""

    def startElement(self, tag, attributes):
        self.CurrentData = tag

        if tag == "path":
            if tag == "path":
                identity = attributes["id"]
                if identity[0:4] == "path":
                    polygon_id = identity

                # writes the dic classes in order of appearance
                # the one that's on the bottom of the html will be displayed on top
                target.write('      <div class="object{}"></div>\n' .format(polygon_id))

    def endElement(self, tag):
      self.CurrentData = ""


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


def make_style_dictionary(path_style):
    """Takes in a string "style" from the path data
       Returns a dictionary of style properties"""

    style_dict = {}

    path_style = path_style.replace(":", " ")
    path_style = path_style.replace(";", " ")
    path_style_list = path_style.split()

    for i in range(len(path_style_list)):
        if i%2 == 0:
            style_dict[path_style_list[i]] = path_style_list[i+1]

    return style_dict


def make_coordinates_raw(path_coordinates):
    """takes in coordinates from svg-path data
       and returns as string of numbers"""

    numbers = ('1234567890.,- ')
    raw_coordinates = ""
    coordinates = ""

    # to make css-coordinates from the svg-path, characters other then
    # numbers and commas have to be omitted
    for char in path_coordinates:
        if char in numbers:
            raw_coordinates += char

    raw_coordinates = raw_coordinates.replace(',', ' ')
    Liste = raw_coordinates.split()

    # the pixel number is reduced to 3 places and used as%
    for i in range(len(Liste)):
        if i%2 == 0:
            coordinates += Liste[i][0:4] + " "
        else:
            coordinates += Liste[i][0:4] + " "

    return coordinates


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


def triang_magic(polygon_coordinates, other_coordinates):
    """Changes the order of the coordinates in the second
       triangle set, in a way that the triangle will not
       dissappear while morphing."""

    first_centroid = make_centroid(polygon_coordinates)
    second_centroid = make_centroid(other_coordinates)

    print ("first", first_centroid, "second", second_centroid)

    diff_x = second_centroid[0] - first_centroid[0]
    diff_y = second_centroid[1] - first_centroid[1]

    print ("diffs", diff_x, diff_y)

    ListeA = first_centroid[2]
    ListeB = second_centroid[2]



    # "moving" points onto the other centroid
    #Coord_names = [A1X, A1Y, B1X, B1Y, C1X, C1Y, A2X, A2Y, B2X, B2Y, C2X, C2Y]
    #Coord_dict = {}

    provisional_coordsB = []


    for i in range(len(ListeB)):
        if i%2 == 0:
            item = ListeB[i] - diff_x
            provisional_coordsB.append(item)
        else:
            item = ListeB[i] - diff_y
            provisional_coordsB.append(item)

    testcentroid = make_centroid(provisional_coordsB)
    # shortest distances between points
    # stationary triangle points: A B C
    # moving triangle points: D E F

    i = 0
    distances = {}
    while i < 5:
        distance_to_D = math.sqrt((ListeA[i] - provisional_coordsB[0])**2 + (ListeA[i+1] - provisional_coordsB[1])**2)
        distance_to_E = math.sqrt((ListeA[i] - provisional_coordsB[2])**2 + (ListeA[i+1] - provisional_coordsB[3])**2)
        distance_to_F = math.sqrt((ListeA[i] - provisional_coordsB[4])**2 + (ListeA[i+1] - provisional_coordsB[5])**2)
        distances[i] = [distance_to_D, distance_to_E, distance_to_F]
        i += 2

    print ("distances", distances)
    print ("ListeB", ListeB)
    min_avrg_distance = 100
    min_avrg_abweichung = 100
    abweichung = 0
    distance_sum = 0
    distance_list = []
    permutations = list(itertools.permutations([1,2,0]))
    print (permutations)
    # [(1, 2, 0), (1, 0, 2), (2, 1, 0), (2, 0, 1), (0, 1, 2), (0, 2, 1)]

    for i in range(len(permutations)):
        distance_sum += distances[0][permutations[i][0]]
        distance_list.append(distances[0][permutations[i][0]])

        distance_sum += distances[2][permutations[i][1]]
        distance_list.append(distances[2][permutations[i][1]])

        distance_sum += distances[4][permutations[i][2]]
        distance_list.append(distances[4][permutations[i][2]])

        avrg_distance = distance_sum/3

        # abweichung vom durchschnitt

        abweichung = 0
        distance_sum = 0

        for j in range(len(distance_list)):
            abweichung += avrg_distance - distance_list[j]

        avrg_abweichung = abweichung/3
        print ("avrg_abweichung", avrg_abweichung)

        if avrg_abweichung < 0:
            avrg_abweichung = avrg_abweichung * -1
            print ("avrg_abweichung", avrg_abweichung)
            print ("avrg_min", min_avrg_abweichung)


        if avrg_abweichung < min_avrg_abweichung:
            min_avrg_abweichung = avrg_abweichung
            marker = i
            print ("avrg_abweichung", avrg_abweichung)
            print ("avrg_min", min_avrg_abweichung)


        print ("avrg_min", min_avrg_abweichung)


    print ("minmum", min_avrg_abweichung, marker)

    D = str(ListeB[0])+"% "+ str(ListeB[1])+"%, "
    E = str(ListeB[2])+"% "+ str(ListeB[3])+"%, "
    F = str(ListeB[4])+"% "+ str(ListeB[5])+"%, "
    point_list = [D, E, F]

    new_other_coordinates = point_list[permutations[marker][0]]+point_list[permutations[marker][1]]+point_list[permutations[marker][2]]
    new_other_coordinates = new_other_coordinates[:-2]


    return new_other_coordinates


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


def make_triangle_dict(factor, zero_diff):
    "Generates a dictionary with all triangle date, coordinates in percent"

    triangle_dict = {}
    triangle_data = []

    f = open('dump.txt','r')
    for l in f:
        line = str(l)
        data_raw = line.split(" ")

        polygon_id = data_raw[0]
        background = data_raw[1]
        # -1 to get rid of /n
        polygon_coordinates = [float(data_raw[2]), float(data_raw[3]), float(data_raw[4]), float(data_raw[5]), float(data_raw[6]), float(data_raw[7])]

        percent_coordinates = make_coordinates_percent(polygon_coordinates, factor, zero_diff)
        print("percent_coordinates:", percent_coordinates, len(percent_coordinates))

        centroid = make_centroid(percent_coordinates)
        centroid_x = centroid[0]

        css_coordinates = ""


        for i in range(len(percent_coordinates)):
            if i%2 == 0:
                css_coordinates += str(percent_coordinates[i])[0:5] + "% "
            else:
                css_coordinates += str(percent_coordinates[i])[0:5] + "%, "

        #....to get rid of the final comma
        css_coordinates = css_coordinates[0:-2]
        print ("css_coordinates:" , css_coordinates)

        triangle_data = [polygon_id, background, percent_coordinates, centroid, css_coordinates]
        triangle_dict[centroid_x] = triangle_data

    return triangle_dict


def make_combination_list(polygon_dict, other_dict):
    """takes in two dictionaries with polygon data
       and returns a dictionary combining triangles
       that will morph into each other"""

    first_list = []
    second_list = []
    combination_list = []

    for key in sorted(polygon_dict):
        first_list.append(key)

    for key in sorted(other_dict):
        second_list.append(key)

    if len(first_list)%2 == 1:
        for i in range(len(first_list)//2 +1):
            if i == 0:
                key = first_list[i]
                value = second_list[i]
                combination_list.append((key, value))
            else:
                key = first_list[i]
                value = second_list[i]
                combination_list.append((key, value))

                key = first_list[-i]
                value = second_list[-i]
                combination_list.append((key, value))
    else:
        for i in range(len(first_list)//2):
            if i == 0:
                key = first_list[i]
                value = second_list[i]
                combination_list.append((key, value))
            else:
                key = first_list[i]
                value = second_list[i]
                combination_list.append((key, value))

                key = first_list[-i]
                value = second_list[-i]
                combination_list.append((key, value))

        key = first_list[i+1]
        value = second_list[i+1]
        combination_list.append((key, value))

    return combination_list


def wrap_css(polygon_dict, other_dict, combination_list):

    wrap = ""
    delay = 0

    for key in sorted(polygon_dict):

        polygon_id = polygon_dict[key][0]
        background = polygon_dict[key][1]
        polygon_coordinates = polygon_dict[key][4]
        centroid_x = polygon_dict[key][3][0]
        centroid_y = polygon_dict[key][3][1]

        for i in range(len(combination_list)):
            if combination_list[i][0] == key:
                value = combination_list[i][1]

                other_background = other_dict[value][1]
                raw_coordinates = other_dict[value][2]
                other_coordinates = triang_magic(polygon_coordinates, raw_coordinates)


        string = """
      .object{} {{
        background: {};
        position: absolute;
        height: 800px;
        width: 800px;
        animation: make_elephant{} 3s {}ms forwards;
        clip-path: polygon({});
        }}

        @keyframes make_elephant{} {{
          0% {{
          background: {};
          clip-path: polygon({});
          }}

          100% {{
          background: {};
          clip-path: polygon({});
          }}
        }}
        """.format(polygon_id, background, polygon_id, delay, polygon_coordinates, polygon_id, background, polygon_coordinates, other_background, other_coordinates)

        wrap += string
        delay += 71

    return wrap

def start_parser(Handler, file_):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    parser.setContentHandler(Handler)

    parser.parse(file_)




# File operations
print ("index.html is generated...")
filename_target = "index.html"
target = open(filename_target, "w")


# this wraps the html/css scaffolding
target.write('<!DOCTYPE html>\n')
target.write('\n')
target.write('<html>\n')
target.write('  <head>\n')
target.write('    <meta charset="UTF-8">\n')
target.write('    <title>Mirabellencode</title>\n')
target.write('    <style type="text/css">\n')
target.write('\n')
target.write('      body {\n')
target.write('      font-family: Proxima-Nova, Helvetica, sans-serif;\n')
target.write('      background-color: white;\n')
target.write('      text-align: center;\n')
target.write('      }\n')
target.write('\n')
target.write('      div {\n')
target.write('      }\n')
target.write('      }\n')
target.write('      }\n')
target.write('\n')

target.close()

# css objects and @keyframes are generated from svg
filename_origin = input("Name of the .svg file (Beginning of animation): ")
origin = open(filename_origin, "r")

filename_origin2 = input("Name of the .svg file (End of animation): ")
origin2 = open(filename_origin2, "r")

filename_target = "index.html"
target = open(filename_target, "a")

filename_dump = "dump.txt"
dump = open(filename_dump, "a")

print("Generating animation...")

# starting xml parser
start_parser(raw_Coordinates(), origin)

origin.close()
dump.close()

dump = open(filename_dump, "a")

start_parser(raw_Coordinates(), origin2)

origin2.close()
dump.close()

raw_coordinates_list = make_raw_coordinates_list()
print ("raw_coordinates_list:", raw_coordinates_list)
min_values = set_zero_factor(raw_coordinates_list)
print ("min_values:", min_values)
factor = make_factor(raw_coordinates_list, min_values)


dump = open(filename_dump, "w")
origin = open(filename_origin, "r")

start_parser(Coordinates(), origin)

origin.close()
dump.close()

triangle1_dictionary = make_triangle_dict(factor, min_values)
print ("triangle1_dictionary:", triangle1_dictionary)
print ("")

dump = open(filename_dump, "w")
origin2 = open(filename_origin2, "r")

start_parser(Coordinates(), origin2)

origin2.close()
dump.close()

triangle2_dictionary = make_triangle_dict(factor, min_values)
print("triangle2_dictionary:", triangle2_dictionary)
print ("")

combination_dictionary = make_combination_list(triangle1_dictionary, triangle2_dictionary)

print("combination_dictionary:", combination_dictionary)

css_wrapping = wrap_css(triangle1_dictionary, triangle2_dictionary, combination_dictionary)

target.write(css_wrapping)


# start of html body
target.write('\n')
target.write('    </style>\n')
target.write('  </head>\n')
target.write('\n')
target.write('  <body>\n')
target.write('    <div>\n')

# Here, the div classes are generated from the polygon_id
origin = open(filename_origin, "r")

# xml parser
start_parser(divGenerator(), origin)

# writes end of index.html
target.write('    </div>\n')
target.write('  </body>\n')
target.write('</html>\n')

# files are closed!
target.close()
origin.close()

# open second second svg file and index for search and replace.
dump = open(filename_dump, "w")

print("Generating animation...")

# starting xml parser
target.close()
origin.close()

print("The parser has finished parsing.")
