from typing import List

def decode_repetition(bits, repetition=3) -> List[int]:
    """
    Decode a binary message with repetition encoding (with various levels
    of repetition). Takes the raw bits from the receiver (e.g.
    recording_to_bits) and recovers each message bit by majority vote
    over its repeats.

    Args:
        bits (List[int]): received bits.
        repetition (int, optional): number of times each bit was repeated. Defaults to 3.

    Returns:
        List[int]: decoded message bits.
    """
    decoded_bits = []
    num_bits = len(bits)//repetition

    for b in range(num_bits):
        # Extract groups of length repetition
        group = bits[b*repetition:(b+1)*repetition]
        # Majority vote
        decoded_bits.append(1 if sum(group) > repetition/2 else 0)

    print("Received bits:", list(bits))
    print("Decoded bits: ", decoded_bits)

    return decoded_bits

def decode_hamming(bits) -> List[int]:
    """
    Decode a binary message with Hamming(7,4) encoding. Each 7-bit block
    is laid out as [p1, p2, d1, p3, d2, d3, d4] (positions 1-7, parity
    bits at the powers of two). Corrects up to one flipped bit per block.

    Args:
        bits (List[int]): received bits.

    Returns:
        List[int]: the 4 data bits of each block.
    """
    decoded_bits = []
    num_blocks = len(bits)//7

    for b in range(num_blocks):
        # Extract blocks of length 7
        block = list(bits[b*7:(b+1)*7])

        # Each parity check covers the positions whose index has that bit set
        s1 = block[0] ^ block[2] ^ block[4] ^ block[6]  # positions 1,3,5,7
        s2 = block[1] ^ block[2] ^ block[5] ^ block[6]  # positions 2,3,6,7
        s3 = block[3] ^ block[4] ^ block[5] ^ block[6]  # positions 4,5,6,7

        # Syndrome gives the 1-indexed position of the error (0 = no error)
        syndrome = s1 + 2*s2 + 4*s3
        if syndrome != 0:
            block[syndrome - 1] ^= 1

        decoded_bits.extend([block[2], block[4], block[5], block[6]])

    print("Received bits:", list(bits))
    print("Decoded bits: ", decoded_bits)

    return decoded_bits