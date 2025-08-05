#!/usr/bin/env python3


def row_min_max_checksum(s):
    nums = [int(n) for n in s.split()]
    return max(nums) - min(nums) if len(nums) > 0 else 0


def row_evenly_divisible_checksum(s):
    nums = sorted([int(n) for n in s.split()])
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[j] % nums[i] == 0:
                return nums[j] // nums[i]
    return 0


def spreadsheet_checksum(spr, checksum):
    return sum(checksum(row) for row in spr)


assert row_min_max_checksum('5 1 9 5') == 8
assert row_min_max_checksum('7 5 3') == 4
assert row_min_max_checksum('2 4 6 8') == 6
assert row_min_max_checksum('2\t4\t6\t8') == 6
assert row_min_max_checksum('') == 0

assert row_evenly_divisible_checksum('5 9 2 8') == 4
assert row_evenly_divisible_checksum('9 4 7 3') == 3
assert row_evenly_divisible_checksum('3 8 6 5') == 2
assert row_evenly_divisible_checksum('') == 0

test_case = """
5 1 9 5
"""
expected = 8
assert spreadsheet_checksum(
    test_case.split('\n'), checksum=row_min_max_checksum) == expected

test_case = """
5 1 9 5
7 5 3
2 4 6 8
"""
expected = 18
assert spreadsheet_checksum(
    test_case.split('\n'), checksum=row_min_max_checksum) == expected

test_case = """
5 9 2 8
9 4 7 3
3 8 6 5
"""
expected = 9
assert spreadsheet_checksum(
    test_case.split('\n'), checksum=row_evenly_divisible_checksum) == expected


if __name__ == '__main__':
    with open('input') as f:
        s = f.readlines()
        print(spreadsheet_checksum(s, checksum=row_min_max_checksum))
        print(spreadsheet_checksum(s, checksum=row_evenly_divisible_checksum))
