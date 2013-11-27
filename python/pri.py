
def pri(file_path):
    counts = [int(line.split(' ')[-2]) for line in open(file_path)]
    types  = [line.split(' ')[-1].strip() for line in open(file_path)]
    total = sum(counts)
    return dict(zip(types, [count/total for count in counts]))

if __name__ == '__main__':
    print (pri('/home/qin/Desktop/type_uniq'))
