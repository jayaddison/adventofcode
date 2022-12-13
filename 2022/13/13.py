def compare(left, right):
    match type(left).__name__, type(right).__name__:

        case 'int', 'int':
           return left < right

        case 'list', 'list':
           left = iter(left)
           right = iter(right)
           while True:
               left_item = next(left, None)
               right_item = next(right, None)
               if not right_item:
                   return True
               if not left_item:
                   return False
               if not compare(left_item, right_item):
                   return False

        case 'int', _:
            return compare([left], right)

        case _, 'int':
            return compare(left, [right])


assert compare(1, 2) == True  # left item is lower
assert compare(2, 1) == False
assert compare([1], [2]) == True  # lower integer first
assert compare([1, 2], [2]) == True  # left items exhausted; all lower than corresponding right items
assert compare([3, 2], [1]) == False
assert compare([1], [2, 3]) == False
