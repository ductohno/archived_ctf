from sage.all import GF
import os
import random

random.seed(20252025)
p = 257
F = GF(p**16)
n = 110


def bytes_to_element(b: bytes):
    return F([c for c in b])


constant = [bytes_to_element(random.randbytes(16)) for _ in range(n)]


def memec(msg: bytes, key: bytes, mcst: int | None):
    assert len(msg) == 16

    msg = bytes_to_element(msg)
    k = bytes_to_element(key)
    if mcst is None:
        mcst = int(sum(msg))
        assert mcst != 0 and mcst != 1
        mcst |= 1

    result = msg
    for i in range(n):
        result = (result + k + constant[i]) ** mcst

    result += k
    return bytes(result)


def generate_challenge(key):
    while True:
        try:
            return memec(os.urandom(16), key, 7)
        except:
            continue


def game():
    key = os.urandom(16)

    name = input("Tell me your name: ")
    if not name.isprintable():
        print("Huh ?")
        exit()

    print(
        "Hello {}, your id is {}.".format(name, memec(name.encode(), key, None).hex())
    )

    cnt = 0
    for round in range(20):
        print("{}/20".format(round + 1))
        challenge = generate_challenge(key)
        print("Our challenge is {}".format(challenge.hex()))
        solution = bytes.fromhex(input("Your solution is: "))
        if challenge == memec(solution, key, 7):
            print("Correct!")
            cnt += 1
        else:
            print("Wrong!")
            exit()
    if cnt == 20:
        from secret import FLAG
        print(FLAG)


if __name__ == "__main__":
    game()
