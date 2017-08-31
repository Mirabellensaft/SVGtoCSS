import triangle_magic
import triangle_math
import coordinates_converter

def make_combination_list(polygon_dict, other_dict):
    """takes in two dictionaries with polygon data
       and returns a dictionary combining triangles
       that will morph into each other"""

    first_list = []
    second_list = []
    combination_list = []

    for key in sorted(polygon_dict):
        first_list.append(key)

    for key in sorted(other_dict):
        second_list.append(key)

    if len(first_list)%2 == 1:
        for i in range(len(first_list)//2 +1):
            if i == 0:
                key = first_list[i]
                value = second_list[i]
                combination_list.append((key, value))
            else:
                key = first_list[i]
                value = second_list[i]
                combination_list.append((key, value))

                key = first_list[-i]
                value = second_list[-i]
                combination_list.append((key, value))
    else:
        for i in range(len(first_list)//2):
            if i == 0:
                key = first_list[i]
                value = second_list[i]
                combination_list.append((key, value))
            else:
                key = first_list[i]
                value = second_list[i]
                combination_list.append((key, value))

                key = first_list[-i]
                value = second_list[-i]
                combination_list.append((key, value))

            key = first_list[i+1]
            value = second_list[i+1]
            combination_list.append((key, value))

    return combination_list


def wrap_css(polygon_dict, other_dict, combination_list):

    wrap = ""
    delay = 0

    for key in sorted(polygon_dict):

        polygon_id = polygon_dict[key][0]
        background = polygon_dict[key][1]
        polygon_coordinates = polygon_dict[key][4]
        centroid_x = polygon_dict[key][3][0]
        centroid_y = polygon_dict[key][3][1]

        for i in range(len(combination_list)):
            if combination_list[i][0] == key:
                value = combination_list[i][1]

                other_background = other_dict[value][1]
                raw_coordinates = other_dict[value][2]
                other_coordinates = triangle_magic.triang_magic(polygon_coordinates, raw_coordinates)


        string = """
      .object{} {{
        background: {};
        position: absolute;
        height: 800px;
        width: 800px;
        animation: make_elephant{} 3s {}ms forwards;
        clip-path: polygon({});
        }}

        @keyframes make_elephant{} {{
          0% {{
          background: {};
          clip-path: polygon({});
          }}

          100% {{
          background: {};
          clip-path: polygon({});
          }}
        }}
        """.format(polygon_id, background, polygon_id, delay, polygon_coordinates, polygon_id, background, polygon_coordinates, other_background, other_coordinates)

        wrap += string
        delay += 71

    return wrap


def make_triangle_dict(factor, zero_diff):
    "Generates a dictionary with all triangle date, coordinates in percent"

    triangle_dict = {}
    triangle_data = []

    f = open('dump.txt','r')
    for l in f:
        line = str(l)
        data_raw = line.split(" ")

        polygon_id = data_raw[0]
        background = data_raw[1]
        # -1 to get rid of /n
        polygon_coordinates = [float(data_raw[2]), float(data_raw[3]), float(data_raw[4]), float(data_raw[5]), float(data_raw[6]), float(data_raw[7])]

        percent_coordinates = coordinates_converter.make_coordinates_percent(polygon_coordinates, factor, zero_diff)
        print("percent_coordinates:", percent_coordinates, len(percent_coordinates))

        centroid = triangle_math.make_centroid(percent_coordinates)
        centroid_x = centroid[0]

        css_coordinates = ""


        for i in range(len(percent_coordinates)):
            if i%2 == 0:
                css_coordinates += str(percent_coordinates[i])[0:5] + "% "
            else:
                css_coordinates += str(percent_coordinates[i])[0:5] + "%, "

        #....to get rid of the final comma
        css_coordinates = css_coordinates[0:-2]
        print ("css_coordinates:" , css_coordinates)

        triangle_data = [polygon_id, background, percent_coordinates, centroid, css_coordinates]
        triangle_dict[centroid_x] = triangle_data

    return triangle_dict
