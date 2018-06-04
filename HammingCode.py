from Encoding import bitfield

dataPos = [2, 4, 5, 6, 8, 9, 10, 11]
parPos = [0, 1, 3, 7]

p1 = [2, 4, 6, 8, 10]
p2 = [2, 5, 6, 9, 10]
p3 = [4, 5, 6, 11]
p4 = [8, 9, 10, 11]

p = [p1, p2, p3, p4]

c1 = [0] + p1
c2 = [1] + p2
c3 = [3] + p3
c4 = [7] + p4

#c = [c1, c2, c3, c4]
c = [c4,c3,c2,c1]

def binaryToDec(bin):
    num = 0
    for bit in bin:
        num = (num << 1) | bit
    return num


def generateHammingCode(num):
    seq = bitfield(num)
    #print(num)
    while len(seq) != 8:
        seq.insert(0, 0)
    template = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(8):
        template[dataPos[i]] = seq[i]

    for i in range(4):
        temp = 0
        for j in range(len(p[i])):
            temp ^= template[p[i][j]]
        template[parPos[i]] = temp

    temp = 0
    for i in range(len(template) -1):
        temp ^= template[i]
    template[-1] = temp
    #print(template)
    #print(binaryToDec(template))
    return binaryToDec(template)


def decodeHamingCode(num):
    seq = bitfield(num)
    while len(seq) != 13:
        seq.insert(0, 0)
    errorCheck = []
    for i in range(4):
        temp = 0
        for j in range(len(c[i])):
            temp ^= seq[c[i][j]]
        errorCheck.append(temp)

    if errorCheck != [0, 0, 0, 0]:
        print(errorCheck)
        if seq[12] == 0:
            print("Double bit error")
        else:
            print("Single bit error")
        index = binaryToDec(errorCheck)
        if index < 12:
            seq[index - 1] = 1 - seq[index - 1]

    msg = []

    for i in dataPos:
        msg.append(seq[i])
    #print(seq)
    #print(msg)
    return binaryToDec(msg)

# #
# code = generateHammingCode(196)
# msg = decodeHamingCode(code)
# print(msg)
