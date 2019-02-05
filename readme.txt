Readme

In order for this program to work, the polygons in the .svg have to have certain
properties.

Coordinates in the .svg need to be absolute.
    Edit > Preferences > SVG output > Path data
        Path string format needs to be set to 'Absolute'.
        'Force repeat commands' has to be activated.

You need two files: one for the beginning, and one for the end of the animation.
In order for the triangles of one file to be able to morph into triangles of the other file, both files need to have the same number of triangles. A triangle is matched to another triangle based how similar their position on the canvas is. 

Coordinates of the triangles will be converted in percent values

So far, the program has only been tested with triangles.
                                                                                    
