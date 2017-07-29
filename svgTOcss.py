import xml.sax

""" This parser reads .svg files. The output are coordinates, formatted to
    CSS clip-paths for polygons."""

class Coordinates( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""


    def startElement(self, tag, attributes):

        numbers = ('1234567890.-')
        coordinates = ""
        self.CurrentData = tag

        if tag == "g":
            layer = attributes["id"]
            target.write("***{}***\n" .format(layer))
            target.write("\n")

        if tag == "path":
            style = attributes["style"]

            if style[5] == '#':
                target.write(".object{} {{\n" .format(style[6:12]))
                target.write("  background: {};\n" .format(style[5:12]))
                target.write("  position: absolute;\n")
                target.write("  height: 800px;\n")
                target.write("  width: 800px;\n")

            content = attributes["d"]
            for char in content[2:]:
                if char in numbers:
                    coordinates += char
                elif char is ',':
                    coordinates += '% '
                elif char is 'L':
                    coordinates += '%, '
                elif char is 'Z':
                    coordinates += '%'


            target.write("  clip-path: polygon({});\n" .format(coordinates))
            target.write("  }\n")
            target.write("\n")

    def endElement(self, tag):
      self.CurrentData = ""


filename_target = input("Name the file your coordinates will be saved in: ")
target = open(filename_target, "w")

filename_origin = input("Name of the .svg file, contaning path data:  ")
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



#in layer 1, path1,
#schreibe coordinaten in css form

#suche path mit gleichem fill,
#schreibe coordinaten in css form
