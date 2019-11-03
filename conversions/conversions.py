""" A module for conversion functions """


def _int32_to_bytes(i):
    """Convert an integer to four bytes in little-endian format."""
    return bytes((i & 0xff,
                  i >> 8 & 0xff,
                  i >> 16 & 0xff,
                  i >> 24 & 0xff))


def _bytes_to_int32(b):
    """Convert a bytes object containing four bytes into an integer."""
    return b[0] | (b[1] << 8) | (b[2] << 16) | (b[3] << 24)


def _int16_to_bytes(i):
    """Convert an integer to four bytes in little-endian format."""
    return bytes((i & 0xff,
                  i >> 8 & 0xff))


def _bytes_to_int16(b):
    """Convert a bytes object containing four bytes into an integer."""
    return b[0] | (b[1] << 8)