class Vector:
    """
    Simple 2 dimensional vector.
    
    Supports +, -, \*, ==
    """

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, item):
        return (self.x, self.y)[item]

    def to_rectangle(self, size):
        """
        Convert this vector into a rectangle
        
        :param size: (width, height) 
        :return: (x, y, width, height)
        """
        return list(self) + list(size)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __eq__(self, other):
        return list(self) == list(other)
