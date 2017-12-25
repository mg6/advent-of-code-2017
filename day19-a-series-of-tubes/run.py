#!/usr/bin/env python3


from itertools import count


def get_diagram_size(diagram):
    if not diagram:
        return (0, 0)

    first_nl = diagram.find('\n')
    width = first_nl if first_nl >= 0 else len(diagram)
    height = diagram.count('\n') + 1

    return width, height


def follow_diagram(diagram):
    return ''.join(v for k, v in _follow_diagram(diagram) if k == 'char')


def get_path_length(diagram):
    return sum(1 for k, v in _follow_diagram(diagram) if k == 'step')


def _follow_diagram(diagram):
    diagram = diagram.strip('\n')
    width, height = get_diagram_size(diagram)
    pos = diagram.find('|')

    if pos >= width:
        raise ValueError('Diagram does not start in top line')

    direction = (0, -1)

    for n in count():
        if pos < 0:
            break

        try:
            cur = diagram[pos]
        except IndexError:
            break

        if cur in ' \n':
            break
        elif cur in '|-':
            pass
        elif cur in '+':
            if direction in ((0, 1), (0, -1)):
                try:
                    if diagram[pos + 1] not in ' \n':
                        direction = (1, 0)
                    else:
                        direction = (-1, 0)
                except IndexError:
                    direction = (-1, 0)
            elif direction in ((1, 0), (-1, 0)):
                try:
                    if diagram[pos - 1 - width] not in ' \n':
                        direction = (0, 1)
                    else:
                        direction = (0, -1)
                except IndexError:
                    direction = (0, -1)
            else:
                raise RuntimeError('Incorrect direction (%d, %d)' % direction)
        else:
            yield 'char', cur

        yield 'step', n

        if direction == (0, 1):
            pos -= width + 1
        elif direction == (1, 0):
            pos += 1
        elif direction == (0, -1):
            pos += width + 1
        elif direction == (-1, 0):
            pos -= 1
        else:
            raise RuntimeError('Incorrect direction (%d, %d)' % direction)


assert get_diagram_size('') == (0, 0)
assert get_diagram_size('.') == (1, 1)
assert get_diagram_size('..\n..') == (2, 2)

diagram = """
|
"""
assert follow_diagram(diagram) == ''
assert get_path_length(diagram) == 1

diagram = """
|
A
"""
assert follow_diagram(diagram) == 'A'
assert get_path_length(diagram) == 2

diagram = """
|
 
A
""" # noqa
assert follow_diagram(diagram) == ''
assert get_path_length(diagram) == 1

diagram = """
|
A
|
B
C
|
"""
assert follow_diagram(diagram) == 'ABC'
assert get_path_length(diagram) == 6

diagram = """
   |
   A
"""
assert follow_diagram(diagram) == 'A'
assert get_path_length(diagram) == 2

diagram = """
   |
  A+
"""
assert follow_diagram(diagram) == 'A'
assert get_path_length(diagram) == 3

diagram = """
   |
B A+
"""
assert follow_diagram(diagram) == 'A'
assert get_path_length(diagram) == 3

diagram = """
   | 
   +A
""" # noqa
assert follow_diagram(diagram) == 'A'
assert get_path_length(diagram) == 3

diagram = """
   |   
   +A B
""" # noqa
assert follow_diagram(diagram) == 'A'
assert get_path_length(diagram) == 3

diagram = """
|    
+AB-C
""" # noqa
assert follow_diagram(diagram) == 'ABC'
assert get_path_length(diagram) == 6

diagram = """
    |
AB-C+
"""
assert follow_diagram(diagram) == 'CBA'
assert get_path_length(diagram) == 6

diagram = """
|  
+-+
  A
""" # noqa
assert follow_diagram(diagram) == 'A'
assert get_path_length(diagram) == 5

diagram = """
  |
+-+
A  
""" # noqa
assert follow_diagram(diagram) == 'A'
assert get_path_length(diagram) == 5

diagram = """
| A
+-+
"""
assert follow_diagram(diagram) == 'A'
assert get_path_length(diagram) == 5

diagram = """
B |
+A+
"""
assert follow_diagram(diagram) == 'AB'
assert get_path_length(diagram) == 5

diagram = """
| 
++
 A
""" # noqa
assert follow_diagram(diagram) == 'A'
assert get_path_length(diagram) == 4

diagram = """
 |
++
A 
""" # noqa
assert follow_diagram(diagram) == 'A'
assert get_path_length(diagram) == 4

diagram = """
B|
|A
++
"""
assert follow_diagram(diagram) == 'AB'
assert get_path_length(diagram) == 6

diagram = """
| C-+
A   |
+-B-+
"""
assert follow_diagram(diagram) == 'ABC'
assert get_path_length(diagram) == 11

diagram = """
|   +-C
A   |  
+-B-+  
""" # noqa
assert follow_diagram(diagram) == 'ABC'
assert get_path_length(diagram) == 11

diagram = """
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
""" # noqa
assert follow_diagram(diagram) == 'ABCDEF'
assert get_path_length(diagram) == 38


if __name__ == '__main__':
    with open('input') as f:
        diagram = f.read().strip('\n')

    width, height = get_diagram_size(diagram)
    assert width == 201, width
    assert height == 201, height

    print('letters', follow_diagram(diagram))
    print('length', get_path_length(diagram))
