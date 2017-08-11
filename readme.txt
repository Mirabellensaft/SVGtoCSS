Readme

In order for this program to work, the polygons in the .svg have to have certain
properties.

Coordinates in the .svg need to be absolute.
    Edit > Preferences > SVG output > Path data
        Path string format needs to be set to 'Absolute'.
        'Force repeat commands' has to be activated.

You need two files: one for the beginning, and one for the end of the animation.
Corresponding polygons in both files need to have the same stroke color.
The stroke will not be shown in the animation, but the hexadecimal is used as an
object ID.

Set the workspace size to 100px * 100px. This way, the coordinates can be used
as %.
