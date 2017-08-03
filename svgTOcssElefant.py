import xml.sax
import fileinput

""" This parser reads .svg files. The output are coordinates, formatted to
    CSS clip-paths for polygons."""

class Coordinates( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""


    def startElement(self, tag, attributes):

        numbers = ('1234567890.,- ')
        raw_coordinates = ""
        coordinates = ""
        Platzhalter = ""
        style = ""
        self.CurrentData = tag


        if tag == "path":

            # only if the # is in the line, the path belongs to a polygon
            style = attributes["style"]

            # polygon_id is the hexadecimal code of the stroke
            # polygons of the same id are different animation stages of the same polygon
            polygon_id = style[54:61]
            background = style[5:12]

            # parsing the coordinates
            content = attributes["d"]

            # to make css-coordinates from the svg-path, characters other then
            # numbers and commas have to be omitted
            for char in content:
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

        Platzhalter = style[5:12]+"replace"

        # wrapping css
        # first line is a comment to identify the polygon
        target.write("/*object{}*/\n".format(polygon_id))
        target.write("    100% {{\n")
        target.write("      background: {};\n".format(background))
        target.write("      clip-path: polygon({});\n" .format(coordinates))
        target.write("    }\n")
        target.write("  }\n")
        target.write("\n")

print("Creator for coordinates for the End of the Animation")

# file operations

filename_target = input("Name the final file: ")
target = open(filename_target, "w")

filename_origin_css = input("Name of the .css file:  ")
origin_css = open(filename_origin_css, "r")

filename_origin_svg = input("Name of the .svg file, containing path data:  ")
origin_svg = open(filename_origin_svg, "r")


if ( __name__ == "__main__"):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = Coordinates()
    parser.setContentHandler(Handler)

    parser.parse(origin_svg)

origin_svg.close()
origin_css.close()
target.close()

print ("The parser has finished parsing.")





#in layer 1, path1,
#schreibe coordinaten in css form

#suche path mit gleichem fill,
#schreibe coordinaten in css form
