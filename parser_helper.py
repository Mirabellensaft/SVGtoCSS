import xml.sax


def start_parser(Handler, file_):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    parser.setContentHandler(Handler)

    parser.parse(file_)


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
