import os
from Crypto.Cipher import DES


def fillupbyte(ch, padn=8, padchar="0", mode="l"):
    n = len(ch)
    l = n
    while l % padn != 0:
        l += 1
    result = ""
    j = 0
    for i in range(l):
        if i < l - n:
            if mode == "l":
                result = padchar + result
            else:
                result = result + padchar
        else:
            if mode == "l":
                result = result + ch[j]
                j += 1
            else:
                result = ch[::-1][j] + result
                j += 1

    return result


def bytes2binary(input):
    """
    >>> bytes2binary(b'\\x01')
    '00000001'
    >>> bytes2binary(b'\\x03')
    '00000011'
    >>> bytes2binary(b'\\xf0')
    '11110000'
    >>> bytes2binary(b'\\xf0\\x80')
    '1111000010000000'
    """
    return fillupbyte(bin(int.from_bytes(input, byteorder="big"))[2:])


def binary2bytes(input):
    """
    >>> binary2bytes('00000001')
    b'\\x01'
    >>> binary2bytes('00000011')
    b'\\x03'
    >>> binary2bytes('11110000')
    b'\\xf0'
    >>> binary2bytes('1111000010000000')
    b'\\xf0\\x80'
    """
    result = bytearray(b"")
    for item in range(0, len(input), 8):
        tmp = input[item : item + 8]
        result += int.to_bytes(int(tmp, 2), byteorder="big", length=1)
    return bytes(result)


def bin_xor(input, input2):
    """
    >>> bin_xor('1011','0000')
    '1011'
    >>> bin_xor('1','0000')
    '0001'
    >>> bin_xor('1101','1011')
    '0110'
    >>> bin_xor('10101010','01010101')
    '11111111'
    """
    xor = ""
    if len(input) > len(input2):
        input2 = input2.rjust(len(input), "0")

    if len(input) < len(input2):
        input = input.rjust(len(input2), "0")

    for item in range(len(input)):
        if input[item] == input2[item]:
            tmp = "0"
        else:
            tmp = "1"
        xor += tmp

    if len(xor) < len(input):
        xor = xor.rjust(len(input), "0")
    return xor


left_shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

PC1 = [
    57,
    49,
    41,
    33,
    25,
    17,
    9,
    1,
    58,
    50,
    42,
    34,
    26,
    18,
    10,
    2,
    59,
    51,
    43,
    35,
    27,
    19,
    11,
    3,
    60,
    52,
    44,
    36,
    63,
    55,
    47,
    39,
    31,
    23,
    15,
    7,
    62,
    54,
    46,
    38,
    30,
    22,
    14,
    6,
    61,
    53,
    45,
    37,
    29,
    21,
    13,
    5,
    28,
    20,
    12,
    4,
]
PC2 = [
    14,
    17,
    11,
    24,
    1,
    5,
    3,
    28,
    15,
    6,
    21,
    10,
    23,
    19,
    12,
    4,
    26,
    8,
    16,
    7,
    27,
    20,
    13,
    2,
    41,
    52,
    31,
    37,
    47,
    55,
    30,
    40,
    51,
    45,
    33,
    48,
    44,
    49,
    39,
    56,
    34,
    53,
    46,
    42,
    50,
    36,
    29,
    32,
]


def create_DES_subkeys(input):
    """
    >>> create_DES_subkeys('0001001100110100010101110111100110011011101111001101111111110001')
    ['000110110000001011101111111111000111000001110010', '011110011010111011011001110110111100100111100101', '010101011111110010001010010000101100111110011001', '011100101010110111010110110110110011010100011101', '011111001110110000000111111010110101001110101000', '011000111010010100111110010100000111101100101111', '111011001000010010110111111101100001100010111100', '111101111000101000111010110000010011101111111011', '111000001101101111101011111011011110011110000001', '101100011111001101000111101110100100011001001111', '001000010101111111010011110111101101001110000110', '011101010111000111110101100101000110011111101001', '100101111100010111010001111110101011101001000001', '010111110100001110110111111100101110011100111010', '101111111001000110001101001111010011111100001010', '110010110011110110001011000011100001011111110101']
    """
    tmp = ""
    if len(input) < len(PC1):
        input = input.zfill(len(PC1))
    for item in PC1:
        tmp += input[item - 1]

    key1 = tmp[:28]
    key2 = tmp[28:]
    result = []
    for num in range(16):
        curr1 = key1[left_shifts[num] :] + key1[: left_shifts[num]]
        curr2 = key2[left_shifts[num] :] + key2[: left_shifts[num]]
        key1 = curr1
        key2 = curr2

        c1c2 = curr1 + curr2
        tmp2 = ""
        if len(c1c2) < len(PC2):
            c1c2 = c1c2.zfill(len(PC2))
        for item in PC2:
            tmp2 += c1c2[item - 1]

        result.append(tmp2)
    return result


E = [
    32,
    1,
    2,
    3,
    4,
    5,
    4,
    5,
    6,
    7,
    8,
    9,
    8,
    9,
    10,
    11,
    12,
    13,
    12,
    13,
    14,
    15,
    16,
    17,
    16,
    17,
    18,
    19,
    20,
    21,
    20,
    21,
    22,
    23,
    24,
    25,
    24,
    25,
    26,
    27,
    28,
    29,
    28,
    29,
    30,
    31,
    32,
    1,
]

S = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ],
]

P = [
    16,
    7,
    20,
    21,
    29,
    12,
    28,
    17,
    1,
    15,
    23,
    26,
    5,
    18,
    31,
    10,
    2,
    8,
    24,
    14,
    32,
    27,
    3,
    9,
    19,
    13,
    30,
    6,
    22,
    11,
    4,
    25,
]


def f(input, k):
    """
    >>> f('11110000101010101111000010101010','000110110000001011101111111111000111000001110010')
    '00100011010010101010100110111011'
    """
    extd_data = ""
    for i in range(0, len(E)):
        extd_data += input[E[i] - 1]

    xor_extd_data = ""
    if len(extd_data) > len(k):
        k = k.rjust(len(extd_data), "0")
    if len(extd_data) < len(k):
        extd_data = extd_data.rjust(len(k), "0")
    for item in range(len(extd_data)):
        if extd_data[item] == k[item]:
            tmp = "0"
        else:
            tmp = "1"
        xor_extd_data += tmp
    if len(xor_extd_data) < len(extd_data):
        xor_extd_data = xor_extd_data.rjust(len(extd_data), "0")
    extd_data = xor_extd_data

    str_data = ""
    for i in range(0, len(extd_data), 6):
        B = extd_data[i : i + 6]
        tmp1 = int(B[0] + B[5], 2)
        tmp2 = int(B[1:5], 2)
        form_S = bin(S[i // 6][tmp1][tmp2])[2:]
        form_S = form_S.zfill(4)
        str_data += form_S

    result = ""
    for i in P:
        result += str_data[i - 1]
    return result


IP = [
    58,
    50,
    42,
    34,
    26,
    18,
    10,
    2,
    60,
    52,
    44,
    36,
    28,
    20,
    12,
    4,
    62,
    54,
    46,
    38,
    30,
    22,
    14,
    6,
    64,
    56,
    48,
    40,
    32,
    24,
    16,
    8,
    57,
    49,
    41,
    33,
    25,
    17,
    9,
    1,
    59,
    51,
    43,
    35,
    27,
    19,
    11,
    3,
    61,
    53,
    45,
    37,
    29,
    21,
    13,
    5,
    63,
    55,
    47,
    39,
    31,
    23,
    15,
    7,
]

IP_inverse = [
    40,
    8,
    48,
    16,
    56,
    24,
    64,
    32,
    39,
    7,
    47,
    15,
    55,
    23,
    63,
    31,
    38,
    6,
    46,
    14,
    54,
    22,
    62,
    30,
    37,
    5,
    45,
    13,
    53,
    21,
    61,
    29,
    36,
    4,
    44,
    12,
    52,
    20,
    60,
    28,
    35,
    3,
    43,
    11,
    51,
    19,
    59,
    27,
    34,
    2,
    42,
    10,
    50,
    18,
    58,
    26,
    33,
    1,
    41,
    9,
    49,
    17,
    57,
    25,
]


def bit_permutation(input, input_list):
    result = ""
    for i in input_list:
        result += input[i - 1]
    return result


def encrypt_DES(key, msg):
    """
    >>> encrypt_DES(b'\\x13\\x34\\x57\\x79\\x9b\\xbc\\xdf\\xf1',b'\\x01\\x23\\x45\\x67\\x89\\xab\\xcd\\xef')
    b'\\x85\\xe8\\x13T\\x0f\\n\\xb4\\x05'
    """
    binary_message = fillupbyte(bin(int.from_bytes(msg, byteorder="big"))[2:])
    binary_key = fillupbyte(bin(int.from_bytes(key, byteorder="big"))[2:])

    DES_subkeys = create_DES_subkeys(binary_key)

    binary_message = bit_permutation(binary_message, IP)

    right_part = binary_message[32:64]
    left_part = binary_message[0:32]

    for i in range(0, 16):
        inp_tmp = f(right_part, DES_subkeys[i])
        xor_tmp = ""
        if len(left_part) > len(inp_tmp):
            inp_tmp = inp_tmp.rjust(len(left_part), "0")
        if len(left_part) < len(inp_tmp):
            left_part = left_part.rjust(len(inp_tmp), "0")
        for item in range(len(left_part)):
            if left_part[item] == inp_tmp[item]:
                tmp = "0"
            else:
                tmp = "1"
            xor_tmp += tmp
        if len(xor_tmp) < len(left_part):
            xor_tmp = xor_tmp.rjust(len(left_part), "0")
        right_tmp = xor_tmp
        left_tmp = right_part

        left_part = left_tmp
        right_part = right_tmp

    inversed_rl = bit_permutation(right_part + left_part, IP_inverse)
    result = b""
    for item in range(0, len(inversed_rl), 8):
        tmp = inversed_rl[item : item + 8]
        result += int.to_bytes(int(tmp, 2), byteorder="big", length=1)

    return result


def are_random_tests_all_passes(input_number):
    """
    >>> are_random_tests_all_passes(100)
    True
    """
    for tries in range(input_number):
        random_data = os.urandom(8)
        random_key = os.urandom(8)
        tmp_des = DES.new(random_key, DES.MODE_ECB)
        true_val = encrypt_DES(random_key, random_data)
        test_val = tmp_des.encrypt(random_data)
        if true_val == test_val:
            return True
        else:
            return False

    return True


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
