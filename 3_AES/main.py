from Crypto.Cipher import AES


def decrypt_aes_ecb(input, key):
    """
    >>> key = bytes([57, 226, 240, 61, 125, 240, 75, 68, 22, 35, 124, 205, 144, 27, 118, 220])
    >>> decrypt_aes_ecb(bytes([215, 221, 59, 138, 96, 94, 155, 69, 52, 90, 212, 108, 49, 65, 138, 179]),key)
    b'lovecryptography'
    >>> decrypt_aes_ecb(bytes([147, 140, 44, 177, 97, 209, 42, 239, 152, 124, 241, 175, 202, 164, 183, 18]),key)
    b'!!really  love!!'
    """
    aes2 = AES.new(key, AES.MODE_ECB)
    result = aes2.decrypt(input)
    return result


def xor_byte_arrays(input_array1, input_array2):
    """
    >>> xor_byte_arrays(bytes([1,2,3,4]),bytes([2,3,4,5]))
    b'\\x03\\x01\\x07\\x01'
    >>> xor_byte_arrays(bytes([1,2,3,4]),bytes([]))
    b'\\x01\\x02\\x03\\x04'
    >>> xor_byte_arrays(bytes([1,2,3,4]),bytes([1,2]))
    b'\\x01\\x02\\x02\\x06'
    >>> xor_byte_arrays(bytes([1,2,4,8,16,32,64,128]),bytes([1,1,1,1,1,1,1,1]))
    b'\\x00\\x03\\x05\\t\\x11!A\\x81'
    """
    if len(input_array1) > len(input_array2):
        input_array2 = input_array2.rjust(len(input_array1), bytes([0]))
    else:
        input_array1 = input_array1.rjust(len(input_array2), bytes([0]))

    result = bytearray(b"")

    for i in range(len(input_array1)):
        result.append(input_array1[i] ^ input_array2[i])

    return bytes(result)


def decrypt_aes_cbc_with_ecb(input, key, IV):
    """
    >>> key = bytes([57, 226, 240, 61, 125, 240, 75, 68, 22, 35, 124, 205, 144, 27, 118, 220])
    >>> iv = bytes([241, 147, 66, 129, 194, 34, 37, 51, 236, 69, 188, 205, 64, 140, 244, 204])
    >>> decrypt_aes_cbc_with_ecb(bytes([255, 18, 67, 115, 172, 117, 242, 233, 246, 69, 81, 156, 52, 154, 123, 171]),key,iv)
    b'hello world 1234'
    >>> decrypt_aes_cbc_with_ecb(bytes([171, 218, 160, 96, 193, 134, 73, 81, 221, 149, 19, 180, 31, 247, 106, 64]),key,iv)
    b'lovecryptography'
    >>> decrypt_aes_cbc_with_ecb(bytes([171, 218, 160, 96, 193, 134, 73, 81, 221, 149, 19, 180, 31, 247, 106, 64] * 2),key,iv)
    b'lovecryptography6&\\x94\\x84`\\xd6\\x15\\x12E\\xbf\\xc8\\x0b>\\x0b\\xf6\\xf5'
    """
    result = bytearray(b"")
    temp = xor_byte_arrays(decrypt_aes_ecb(input[:16], key), IV)

    for item in temp:
        result.append(item)

    for i in range(16, len(input), 16):
        temp2 = xor_byte_arrays(
            decrypt_aes_ecb(input[i : i + 16], key),
            input[i - 16 : i],
        )
        for item in temp2:
            result.append(item)
    return bytes(result)


def encrypt_aes_cbc_with_ecb(input, key, IV):
    """
    >>> key = bytes([57, 226, 240, 61, 125, 240, 75, 68, 22, 35, 124, 205, 144, 27, 118, 220])
    >>> iv = bytes([241, 147, 66, 129, 194, 34, 37, 51, 236, 69, 188, 205, 64, 140, 244, 204])
    >>> encrypt_aes_cbc_with_ecb(b'hello world 1234',key,iv)
    b'\\xff\\x12Cs\\xacu\\xf2\\xe9\\xf6EQ\\x9c4\\x9a{\\xab'
    >>> encrypt_aes_cbc_with_ecb(bytes(b'lovecryptography'),key,iv)
    b'\\xab\\xda\\xa0`\\xc1\\x86IQ\\xdd\\x95\\x13\\xb4\\x1f\\xf7j@'
    >>> encrypt_aes_cbc_with_ecb(b'hello world 1234hello world 1234hello world 1234',key,iv)
    b'\\xff\\x12Cs\\xacu\\xf2\\xe9\\xf6EQ\\x9c4\\x9a{\\xab>\\xe3\\xc3\\xf5g\\xc7kYZpk>\\x88\\xf3\\x0f\\x16\\x13\\x85\\xb5\\x1d\\r+\\xdc\\xae\\xa1\\x1d\\x80\\xfa_F\\xb1\\xc0'
    >>> encrypt_aes_cbc_with_ecb(bytes(b'lovecryptography123456789abcdefhellooooooooooooo'),key,iv)
    b'\\xab\\xda\\xa0`\\xc1\\x86IQ\\xdd\\x95\\x13\\xb4\\x1f\\xf7j@\\xd7\\xf2\\xd1T\\xfe[\\xd1\\xb4d5\\x90\\xdc\\x1fj?\\x12\\xfd\\x15\\xcb\\x8b\\xa3\\x1c*\\xd4B\\x8fJs\\x03\\xf9\\x7f3'
    """
    ret = bytearray(b"")
    aes2 = AES.new(key, AES.MODE_ECB)
    first = aes2.encrypt(xor_byte_arrays(input[:16], IV))
    for item in first:
        ret.append(item)
    prev = first
    for i in range(16, len(input), 16):
        aes2 = AES.new(key, AES.MODE_ECB)
        original = aes2.encrypt(xor_byte_arrays(input[i : i + 16], prev))
        for item in original:
            ret.append(item)
        prev = original
    return bytes(ret)


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
