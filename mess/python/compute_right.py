old_file = "tbl.split.test"
new_file = "test.res"


def main():
    old_file_list = []
    new_file_list = []
    right = 0
    wrong = 0
    for line in open(old_file):
        old_file_list.append(line)
    for line in open(new_file):
        new_file_list.append(line)
    for i in len(old_file_list):
        if old_file_list[i] != new_file_list[i]:
            if "E" in new_file_list[i] or "S" in new_file_list[i]:
                items = new_file_list[i].split(" ")
                if (items[2] == items[3]):
                    right += 1
                else:
                    wrong += 1

if __name__ == '__main__':
    main()
