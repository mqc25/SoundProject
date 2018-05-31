#Binary to text
def binary2text(Binary):
    n = int(Binary, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()