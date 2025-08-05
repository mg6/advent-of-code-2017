#!/usr/bin/env python3


def validate_no_repeated(passphrase):
    words = passphrase.strip().split()
    return len(set(words)) == len(words)


def validate_no_anagrams(passphrase):
    words = [''.join(sorted(word)) for word in passphrase.strip().split()]
    return len(set(words)) == len(words)


assert validate_no_repeated("aa bb cc dd ee")
assert validate_no_repeated("aa bb cc dd aaa")
assert not validate_no_repeated("aa bb cc dd aa")

assert validate_no_anagrams("aa bb cc dd ee")
assert validate_no_anagrams("aa bb cc dd aaa")
assert validate_no_anagrams("abcde fghij")
assert validate_no_anagrams("a ab abc abd abf abj")
assert validate_no_anagrams("iiii oiii ooii oooi oooo")
assert not validate_no_anagrams("aa bb cc dd aa")
assert not validate_no_anagrams("abcde xyz ecdab")
assert not validate_no_anagrams("oiii ioii iioi iiio")


if __name__ == '__main__':
    with open('input') as f:
        lines = f.readlines()
        print(sum(validate_no_repeated(passphrase) for passphrase in lines))
        print(sum(validate_no_anagrams(passphrase) for passphrase in lines))
