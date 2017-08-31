Readme

In order for this program to work, the polygons in the .svg have to have certain
properties.

Coordinates in the .svg need to be absolute.
    Edit > Preferences > SVG output > Path data
        Path string format needs to be set to 'Absolute'.
        'Force repeat commands' has to be activated.

You need two files: one for the beginning, and one for the end of the animation.
A Triangle in one file will morph into a triangle of the other file. They are
matched according to how close they are. The files need to have the same number
of triangles

Coordinates of the triangles will be converted in percent values

So far, the program has only been tested with triangles.
