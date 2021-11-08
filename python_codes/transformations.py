from numpy import array, cos, sin



def translation_along_x_axis(a):
    T = array([[1, 0, a],
                  [0, 1, 0],
                  [0, 0, 1]])

    return T

def rotation_around_zaxis(q):
    R = array([[cos(q), -sin(q), 0],
               [sin(q), cos(q), 0],
               [0, 0, 1]])
    return R