import xml.sax

""" This parser reads .svg files. The output are coordinates, formatted to
    CSS clip-paths for polygons."""

class Coordinates( xml.sax.ContentHandler ):
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
            style = attributes["style"]

            style_dictionary = make_style_dictionary(style)

            # polygon_id is the hexadecimal code of the stroke
            # polygons of the same id are different animation stages of the same polygon
            polygon_id = style_dictionary['stroke'][1:8]

            background = style_dictionary['fill']

            content = attributes["d"]

            polygon_coordinates = make_coordinates(content)

            # wrapping css
            target.write("{}\n" .format(polygon_coordinates))

    def endElement(self, tag):
      self.CurrentData = ""

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

def make_coordinates(path_coordinates):
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
            coordinates += Liste[i][0:4] + "% "
        else:
            coordinates += Liste[i][0:4] + "%, "

    # ....to get rid of the final comma
    coordinates = coordinates[0:-2]

    return coordinates

def make_centroid(coordinates):

    x_values = 0
    y_values = 0

    Liste = coordinates.split()

    # makes clean coordinates as float
    for i in range(len(Liste)):
        Liste[i] = float(Liste[(i)][0:4])

        if i%2 == 0:
            x_values += Liste[i]
        else:
            y_values += Liste[i]
    # calculates x- and y-values of the centroid
    x_value = x_values/3
    y_value = y_values/3

    centroid = (x_value, y_value)

    return centroid

def mergeSort(L, compare = operator.lt):
    if len(L) < 2:
        return L[:]
    else:
        middle = int(len(L)/2)
        left = mergeSort(L[:middle], compare)
        right = mergeSort(L[middle:], compare)
        return merge(left, right, compare)

def merge(left, right, compare):
    result = []
    i,j = 0, 0
    while i < len(left) and j < len(right):
        if compare(left[i], right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while (i < len(left)):
        result.append(left[i])
        i += 1
    while (j < len(right)):
        result.append(right[j])
        j += 1
    return result


# File operations
# This new file will be generated.

# generate this file as temp, so the order of items can be sorted. Once the order
# is complete, substitute in the index.html.

print ("so you wand to animate polygons?")
filename_target = input("Name the file where your css will be saved in: >")
target = open(filename_target, "w")

# This is the File containing the coordinates of the polygons
filename_origin = input("Name of the .svg file, contaning path data: >")
origin = open(filename_origin, "r")



if ( __name__ == "__main__"):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = Coordinates()
    parser.setContentHandler(Handler)

    parser.parse(origin)


target.close()
origin.close()

print ("The parser has finished parsing.")
