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

            if style_dictionary.get('stroke'):
                polygon_id = style_dictionary['stroke'][1:8]

                background = style_dictionary['fill']

            # wrap css
                target.write("      .object{} {{\n" .format(polygon_id))
                target.write("        background: {};\n" .format(background))
                target.write("        position: absolute;\n")
                target.write("        height: 800px;\n")
                target.write("        width: 800px;\n")
                target.write("        animation: make_elephant{} 5s infinite;\n" .format(polygon_id))

            # parsing the coordinates
                content = attributes["d"]

                polygon_coordinates = make_coordinates(content)

            # wrapping css
                target.write("        clip-path: polygon({});\n" .format(polygon_coordinates))
                target.write("        }\n")
                target.write("        @keyframes make_elephant{} {{ \n" .format(polygon_id))
                target.write("          0% {\n")
                target.write("            background: {};\n".format(background))
                target.write("            clip-path: polygon({});\n" .format(polygon_coordinates))
                target.write("          }\n")

            # the following lines will be replaced later in the program
                target.write("          replace{}\n".format(polygon_id))
                target.write("\n")



    def endElement(self, tag):
      self.CurrentData = ""



class divGenerator( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""

    def startElement(self, tag, attributes):

        self.CurrentData = tag

        if tag == "path":
            style = attributes["style"]

            style_dictionary = make_style_dictionary(style)

            # polygon_id is the hexadecimal code of the stroke
            # polygons of the same id are different animation stages of the same polygon
            if style_dictionary.get('stroke'):

                polygon_id = style_dictionary['stroke'][1:8]

                background = style_dictionary['fill']

                # writes the dic classes in order of appearance
                # the one that's on the bottom of the html will be displayed on top
                target.write('      <div class="object{}"></div>\n' .format(polygon_id))

    def endElement(self, tag):
      self.CurrentData = ""

class Animation ( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""

    def startElement(self, tag, attributes):

        self.CurrentData = tag

        if tag == "path":

            # only if the # is in the line, the path belongs to a polygon
            style = attributes["style"]

            style_dictionary = make_style_dictionary(style)

            # polygon_id is the hexadecimal code of the stroke
            # polygons of the same id are different animation stages of the same polygon


            polygon_id = style_dictionary['stroke'][1:8]

            background = style_dictionary['fill']

            # parsing the coordinates
            content = attributes["d"]


            polygon_coordinates = make_coordinates(content)

        # search and replace the replace line in index.html, generating the
        # 100% keyframe.


        # Read in the file
            with open('index.html', 'r') as file :
                filedata = file.read()

        # Replace the target string
            filedata = filedata.replace("replace{}".format(polygon_id), "100% {{\n            background: {};\n            clip-path: polygon({});\n          }}\n        }}" .format(background, polygon_coordinates))

        # Write the file out again
            with open('index.html', 'w') as file:
                file.write(filedata)


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


#File operations
print ("index.html is generated...")
filename_target = "index.html"
target = open(filename_target, "w")


#this wraps the html/css scaffolding
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
target.write('\n')

target.close()

# css objects and @keyframes are generated from svg

filename_origin = input("Name of the .svg file (Beginning of animation): ")
origin = open(filename_origin, "r")

filename_target = "index.html"
target = open(filename_target, "a")

parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = Coordinates()
parser.setContentHandler(Handler)

parser.parse(origin)

origin.close()

# start of html body
target.write('\n')
target.write('    </style>\n')
target.write('  </head>\n')
target.write('\n')
target.write('  <body>\n')
target.write('    <div>\n')

# Here, the div classes are generated from the polygon_id
origin = open(filename_origin, "r")


parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = divGenerator()
parser.setContentHandler(Handler)

parser.parse(origin)

# writes end of index.html
target.write('    </div>\n')
target.write('  </body>\n')
target.write('</html>\n')


#files are closed!
target.close()
origin.close()

#open second second svg file and index for search and replace.

filename_origin = input("Name of the .svg file (End of animation): ")
origin = open(filename_origin, "r")

print("Generating animation...")

# starting parser
parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
Handler = Animation()
parser.setContentHandler(Handler)

parser.parse(origin)



target.close()
origin.close()
print ("The parser has finished parsing.")
