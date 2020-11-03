# 计算名字间的汉明距离
def name2ascii(name):
    s = 0
    for n in name:
        num = ord(n)
        s += int(num)
    return s


name_1 = '潘韦伯'
name_2 = '潘韦伯'

n1 = name2ascii(name_1)
n2 = name2ascii(name_2)
print(bin(n1).count('1'), bin(n2).count('1'))
print(bin(n1 ^ n2).count('1'))





