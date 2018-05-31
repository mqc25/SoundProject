#st = "insert your text here"
#output = ' '.join(format(ord(x), 'b') for x in st)
#chr(int('1101000',2))



#text to Binary
def text2binary(text):
    return bin(int.from_bytes(text.encode(), 'big'))


#Binary to text
#n = int(Binary, 2)
#text=n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()