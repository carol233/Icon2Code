
if __name__ == '__main__':
    all = 0
    num = 0
    sampls = 47827
    with open("runtime.txt") as fr:
        content = fr.readlines()
        for line in content:
            num += 1
            all += float(line.strip())
    single = all / (num * sampls)
    print(single)

"""
3742.563326
3750.020156
3756.943687
3774.2662139999998
3802.02245
3805.155222
3810.5037549999997
3820.78872
3834.439797
3851.804782
"""