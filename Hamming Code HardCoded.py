#tell us how many parity bits are needed

def noOfParityBits(noOfBits):
	i=0
	while 2.**i <= noOfBits+i: # (power of 2 + parity bits laready  counted) that is for 4 bit of dataword requires 3 bit of parity bits
		i+=1
	return i
#function to genrate no of parity bits in while correction of hamming codes returns no of parity bits in given size of code word
def noOfParityBitsInCode(noOfBits):
	i=0
	while 2.**i <= noOfBits:
		i+=1

	return i
#parameter:data
#returns a list with parity bits position is 0 that is position which are power of 2 are 0

def appendParityBits(data):
	n=noOfParityBits(len(data)) #no of parity bits required for given length of data
	i=0 #loop counter
	j=0 #no of parity bits
	k=0 #no of data bits
	list1=list()
	while i <n+len(data):
		if i== (2.**j -1):
			list1.insert(i,0)
			j+=1
		else:
			list1.insert(i,data[k])
			k+=1
		i+=1
	return list1



def HamingCode(data):
    R1=0
    R2=0
    R4=0
    R8=0
    n=noOfParityBits(len(data))
    list1=appendParityBits(data)
    if list1[2]=='1':
        R1+=1
        R2+=1
    if list1[4]=='1':
        R1+=1
        R4+=1
    if list1[5]=='1':
        R2+=1
        R4+=1
    if list1[6]=='1':
        R1+=1
        R2+=1
        R4+=1
    if list1[8]=='1':
        R1+=1
        R8+=1
    if list1[9]=='1':
        R2+=1
        R8+=1
    if list1[10]=='1':
        R1+=1
        R2+=1
        R8+=1
    if list1[11]=='1':
        R4+=1
        R8+=1
    if R1%2 :
        list1[0]=1
    if R2%2 :
        list1[1]=1
    if R4%2 :
        list1[3]=1
    if R8%2 :
        list[7]=1
    return list1,R1,R2,R4,R8





    












