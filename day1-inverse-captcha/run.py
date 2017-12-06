#!/usr/bin/env python3

def solve_doubled_digit_captcha(s):
    def repeated_digits(s):
        for i in range(len(s) - 1):
            if s[i+1] == s[i]:
                yield int(s[i])

    s = s + s[0]
    return sum(repeated_digits(s))


def solve_halfway_captcha(s):
    def repeated_digits(s):
        digits = len(s) - 1
        for i in range(digits):
            if s[(i + digits // 2) % digits] == s[i]:
                yield int(s[i])

    s = s + s[0]
    return sum(repeated_digits(s))


assert solve_doubled_digit_captcha("1122") == 3
assert solve_doubled_digit_captcha("1111") == 4
assert solve_doubled_digit_captcha("1234") == 0
assert solve_doubled_digit_captcha("91212129") == 9

assert solve_halfway_captcha("1212") == 6
assert solve_halfway_captcha("1221") == 0
assert solve_halfway_captcha("123425") == 4
assert solve_halfway_captcha("123123") == 12
assert solve_halfway_captcha("12131415") == 4


if __name__ == '__main__':
    with open('input') as f:
        s = f.read().strip()
        print(solve_doubled_digit_captcha(s))
        print(solve_halfway_captcha(s))
