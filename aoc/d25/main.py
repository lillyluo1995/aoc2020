from typing import IO

def handshake(subject, public_key):
    '''the handshake thing to return # loops'''
    divisor = 20201227
    current = 1
    num_loops = 0
    while current != public_key:
        num_loops += 1
        current = current * subject % divisor
    return num_loops

def decrypt(subject, num_loops):
    '''decrypt with num loops'''
    divisor = 20201227
    current = 1
    for _ in range(num_loops):
        current = current * subject % divisor
    return current

def p_1(input_file: IO, debug=False): # pylint: disable=unused-argument
    '''encrypt/decrypt the card and door'''
    card_public = 9789649
    door_public = 3647239
    subject = 7

    num_loops_card = handshake(subject, card_public)
    num_loops_door = handshake(subject, door_public)

    encrypt_card = decrypt(door_public,num_loops_card)
    encrypt_door = decrypt(card_public, num_loops_door)
    assert encrypt_card == encrypt_door
    return encrypt_card


def p_2(input_file: IO, debug=False): # pylint: disable=unused-argument
    '''unknown part 2....'''
    return 'Success'
