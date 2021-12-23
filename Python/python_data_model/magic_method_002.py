# Magic method(=special method)

class Vector(object):
    def __init__(self, *args):
        '''
        Create a vector, example : v = Vector(5, 10)
        '''
        if len(args) == 0:
            self._x, self._y = 0, 0
        else:
            self._x, self._y = args

    def __repr__(self):
        '''
        Return the vector informations.
        '''
        return 'Vector(%r, %r)' % (self._x, self._y) # %s는 string r은 repr에서 사용

    def __add__(self, other):
        '''
        Add vector
        '''
        return Vector(self._x + other._x, self._y + other._y)

    def __mul__(self, y):
        return Vector(self._x * y, self._y * y)
    
    # (0, 0) 찾기
    def __bool__(self):
        return bool(max(self._x, self._y))


v1 = Vector(5, 7)
v2 = Vector(23, 35)
v3 = Vector()

print(Vector.__init__.__doc__)
print(Vector.__repr__.__doc__)
print(Vector.__add__.__doc__)

print(v1, v2, v3) # Vector(5, 7) Vector(23, 35) Vector(0, 0)

print(v1 + v2) # Vector(28, 42)

print(v1 * 3) # Vector(15, 21)

print(bool(v1), bool(v2)) # True True