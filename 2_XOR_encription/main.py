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


def bin2dec(binary):
    binary1 = int(binary)
    decimal, i, n = 0, 0, 0

    while binary1 != 0:
        dec = binary1 % 10
        decimal = decimal + dec * pow(2, i)
        binary1 = binary1 // 10
        i += 1
    return decimal


def dec2hex(decimal):
    conversion_table = {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "A",
        11: "B",
        12: "C",
        13: "D",
        14: "E",
        15: "F",
    }

    if decimal <= 0:
        return ""

    remainder = decimal % 16
    return dec2hex(decimal // 16) + conversion_table[remainder]


def bin2hex(ch):
    decimal = bin2dec(ch)
    return dec2hex(decimal)


def hex2bin(ch):
    n = int(ch, 16)
    result = ""
    while n > 0:
        result = str(n % 2) + result
        n = n >> 1
    return result


def hex2string(ch):
    result = ""
    for i in range(0, len(ch), 2):
        result += chr(int(ch[i : i + 2], 16))
    return result


def string2hex(ch):
    result = ""
    for c in ch:
        result += hex(ord(c))[2:]
    return result


def hex_xor(ch1, ch2):
    """
    >>> hex_xor('0aabbf11','12345678')
    '189fe969'
    >>> hex_xor('12cc','12cc')
    '0000'
    >>> hex_xor('1234','2345')
    '3171'
    >>> hex_xor('111','248')
    '359'
    >>> hex_xor('8888888','1234567')
    '9abcdef'
    """
    maxlen = -1
    if len(ch1) > len(ch2):
        maxlen = len(ch1)
    else:
        maxlen = len(ch2)

    s1_bin = list(hex2bin(ch1))
    s2_bin = list(hex2bin(ch2))

    l1 = len(s1_bin)
    l2 = len(s2_bin)

    if l1 > l2:
        while l1 != l2:
            s2_bin.insert(0, "0")
            l2 = len(s2_bin)

    elif l1 < l2:
        while l1 != l2:
            s1_bin.insert(0, "0")
            l1 = len(s2_bin)

    s_xor = ""
    for i, j in zip(s1_bin, s2_bin):
        b1 = bool(int(i))
        b2 = bool(int(j))
        s_xor = s_xor + str(int((b1 ^ b2)))

    s_xor_pad = fillupbyte(s_xor)

    result = bin2hex(s_xor_pad)

    res_len = len(result)
    while res_len != maxlen:
        result = "0" + result
        res_len = res_len + 1

    return result.lower()


def encrypt_single_byte_xor(ch, key):
    """
    >>> encrypt_single_byte_xor('aaabbccc','00')
    'aaabbccc'
    >>> encrypt_single_byte_xor(string2hex('hello'),'aa')
    'c2cfc6c6c5'
    >>> hex2string(encrypt_single_byte_xor(encrypt_single_byte_xor(string2hex('hello'),'aa'),'aa'))
    'hello'
    >>> hex2string(encrypt_single_byte_xor(encrypt_single_byte_xor(string2hex('Encrypt and decrypt are the same'),'aa'),'aa'))
    'Encrypt and decrypt are the same'
    """
    key = (key * len(ch))[: len(ch)]

    return hex_xor(ch, key).lower()


def decrypt_single_byte_xor(ch):
    """
    >>> decrypt_single_byte_xor('e9c88081f8ced481c9c0d7c481c7ced4cfc581ccc480')
    'Hi! You have found me!'
    >>> decrypt_single_byte_xor('b29e9f96839085849d9085989e9f82d1889e84d199908794d197989f95d1859994d181908282869e8395d0')
    'Congratulations you have find the password!'
    """

    valid_chars = "abcdefghijklmnopqrstuvxyz'- \"ABCDEFGHIJKLMNOPQRSTUVXYZ"
    guess = 0
    count = 0

    for k in range(256):
        msg = hex2string(encrypt_single_byte_xor(ch, hex(k)[2:]))
        m = 0
        for c in msg:
            if c in valid_chars:
                m += 1
        if guess == 0 or count < m:
            guess = msg
            count = m

    return guess


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
