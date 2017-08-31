import xml.sax

import coordinates_converter
import parser_helper
import animation_maker


""" This parser reads .svg files. The output are coordinates, formatted to
    CSS clip-paths for polygons."""

class raw_Coordinates(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""


    def startElement(self, tag, attributes):

        self.CurrentData = tag
        dump = open(filename_dump, "a")
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
                polygon_coordinates_raw = parser_helper.make_coordinates_raw(content)

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

                style_dictionary = parser_helper.make_style_dictionary(style)
                background = style_dictionary['fill']

                # parsing the coordinates
                content = attributes["d"]

                # coordinates for calculating in percent
                polygon_coordinates_raw = parser_helper.make_coordinates_raw(content)

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
parser_helper.start_parser(raw_Coordinates(), origin)

origin.close()
dump.close()

dump = open(filename_dump, "a")

parser_helper.start_parser(raw_Coordinates(), origin2)

origin2.close()
dump.close()

raw_coordinates_list = coordinates_converter.make_raw_coordinates_list()
print ("raw_coordinates_list:", raw_coordinates_list)
min_values = coordinates_converter.set_zero_factor(raw_coordinates_list)
print ("min_values:", min_values)
factor = coordinates_converter.make_factor(raw_coordinates_list, min_values)


dump = open(filename_dump, "w")
origin = open(filename_origin, "r")

parser_helper.start_parser(Coordinates(), origin)

origin.close()
dump.close()

triangle1_dictionary = animation_maker.make_triangle_dict(factor, min_values)
print ("triangle1_dictionary:", triangle1_dictionary)
print ("")

dump = open(filename_dump, "w")
origin2 = open(filename_origin2, "r")

parser_helper.start_parser(Coordinates(), origin2)

origin2.close()
dump.close()

triangle2_dictionary = animation_maker.make_triangle_dict(factor, min_values)
print("triangle2_dictionary:", triangle2_dictionary)
print ("")

combination_dictionary = animation_maker.make_combination_list(triangle1_dictionary, triangle2_dictionary)

print("combination_dictionary:", combination_dictionary)

css_wrapping = animation_maker.wrap_css(triangle1_dictionary, triangle2_dictionary, combination_dictionary)

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
parser_helper.start_parser(divGenerator(), origin)

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
