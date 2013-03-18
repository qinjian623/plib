file_string = "./tbl.test"
split_ratio = 0.5
file_string_a = "./tbl.split.test"
file_string_b = "./tbl.split.train"


def main():
    cats_count = {}
    pois_list = []
    still_in_one_poi = False
    poi = []
    for line in open(file_string):
        if line == "\n":
            #print "empty line"
            still_in_one_poi = False
            pois_list.append(poi)
            poi = []
            continue
        line_itmes = line.split(" ")

        poi.append(line)
        if not still_in_one_poi:
            if line_itmes[3] not in cats_count:
                cats_count[line_itmes[3]] = 1
            else:
                cats_count[line_itmes[3]] += 1
        still_in_one_poi = True

    cats_split_count = {}
    for key in cats_count.keys():
        cats_split_count[key] = int(cats_count[key] * split_ratio)
        print key, cats_count[key]
    print cats_split_count

    file_a = open(file_string_a, 'w')
    file_b = open(file_string_b, 'w')

    for poi in pois_list:
        if (cats_split_count[poi[0].split(" ")[3]] == 0):
            for line in poi:
                file_a.write(line)
            file_a.write("\n")
        else:
            cats_split_count[poi[0].split(" ")[3]] -= 1
            for line in poi:
                file_b.write(line)
            file_b.write("\n")

if __name__ == '__main__':
    main()
