import triangle_math
import math
import itertools

def triang_magic(polygon_coordinates, other_coordinates):
    """Changes the order of the coordinates in the second
       triangle set, in a way that the triangle will not
       dissappear while morphing."""

    first_centroid = triangle_math.make_centroid(polygon_coordinates)
    second_centroid = triangle_math.make_centroid(other_coordinates)

    print ("first", first_centroid, "second", second_centroid)

    diff_x = second_centroid[0] - first_centroid[0]
    diff_y = second_centroid[1] - first_centroid[1]

    print ("diffs", diff_x, diff_y)

    ListeA = first_centroid[2]
    ListeB = second_centroid[2]



    # "moving" points onto the other centroid
    #Coord_names = [A1X, A1Y, B1X, B1Y, C1X, C1Y, A2X, A2Y, B2X, B2Y, C2X, C2Y]
    #Coord_dict = {}

    provisional_coordsB = []


    for i in range(len(ListeB)):
        if i%2 == 0:
            item = ListeB[i] - diff_x
            provisional_coordsB.append(item)
        else:
            item = ListeB[i] - diff_y
            provisional_coordsB.append(item)

    testcentroid = triangle_math.make_centroid(provisional_coordsB)
    # shortest distances between points
    # stationary triangle points: A B C
    # moving triangle points: D E F

    i = 0
    distances = {}
    while i < 5:
        distance_to_D = math.sqrt((ListeA[i] - provisional_coordsB[0])**2 + (ListeA[i+1] - provisional_coordsB[1])**2)
        distance_to_E = math.sqrt((ListeA[i] - provisional_coordsB[2])**2 + (ListeA[i+1] - provisional_coordsB[3])**2)
        distance_to_F = math.sqrt((ListeA[i] - provisional_coordsB[4])**2 + (ListeA[i+1] - provisional_coordsB[5])**2)
        distances[i] = [distance_to_D, distance_to_E, distance_to_F]
        i += 2

    print ("distances", distances)
    print ("ListeB", ListeB)
    min_avrg_distance = 100
    min_avrg_abweichung = 100
    abweichung = 0
    distance_sum = 0
    distance_list = []
    permutations = list(itertools.permutations([1,2,0]))
    print (permutations)
    # [(1, 2, 0), (1, 0, 2), (2, 1, 0), (2, 0, 1), (0, 1, 2), (0, 2, 1)]

    for i in range(len(permutations)):
        distance_sum += distances[0][permutations[i][0]]
        distance_list.append(distances[0][permutations[i][0]])

        distance_sum += distances[2][permutations[i][1]]
        distance_list.append(distances[2][permutations[i][1]])

        distance_sum += distances[4][permutations[i][2]]
        distance_list.append(distances[4][permutations[i][2]])

        avrg_distance = distance_sum/3

        # abweichung vom durchschnitt

        abweichung = 0
        distance_sum = 0

        for j in range(len(distance_list)):
            abweichung += avrg_distance - distance_list[j]

        avrg_abweichung = abweichung/3
        print ("avrg_abweichung", avrg_abweichung)

        if avrg_abweichung < 0:
            avrg_abweichung = avrg_abweichung * -1
            print ("avrg_abweichung", avrg_abweichung)
            print ("avrg_min", min_avrg_abweichung)


        if avrg_abweichung < min_avrg_abweichung:
            min_avrg_abweichung = avrg_abweichung
            marker = i
            print ("avrg_abweichung", avrg_abweichung)
            print ("avrg_min", min_avrg_abweichung)


        print ("avrg_min", min_avrg_abweichung)


    print ("minmum", min_avrg_abweichung, marker)

    D = str(ListeB[0])+"% "+ str(ListeB[1])+"%, "
    E = str(ListeB[2])+"% "+ str(ListeB[3])+"%, "
    F = str(ListeB[4])+"% "+ str(ListeB[5])+"%, "
    point_list = [D, E, F]

    new_other_coordinates = point_list[permutations[marker][0]]+point_list[permutations[marker][1]]+point_list[permutations[marker][2]]
    new_other_coordinates = new_other_coordinates[:-2]


    return new_other_coordinates
