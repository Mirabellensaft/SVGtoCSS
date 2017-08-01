import xml.sax

""" This parser reads .svg files. The output are coordinates, formatted to
    CSS clip-paths for polygons."""


class divGenerator( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""

    def startElement(self, tag, attributes):

        self.CurrentData = tag
        if tag == "path":
            style = attributes["style"]
            if style[5] == '#':
                target.write('<div class="object{}"></div>\n' .format(style[6:12]))

    def endElement(self, tag):
      self.CurrentData = ""


filename_target = input("Name the file your coordinates will be saved in:")
target = open(filename_target, "w")

filename_origin = input("Name of the .svg file:")
origin = open(filename_origin, "r")


if ( __name__ == "__main__"):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = divGenerator()
    parser.setContentHandler(Handler)

    parser.parse(origin)

target.close()
origin.close()

print ("The parser has finished parsing.")



#in layer 1, path1,
#schreibe coordinaten in css form

#suche path mit gleichem fill,
#schreibe coordinaten in css form
