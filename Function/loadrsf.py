import m8r

def loadrsf(file_name):
    mat = m8r.Input('%s.rsf' % file_name)
    n1 = mat.int("n1")
    n2 = mat.int("n2")
    D = mat.read(shape=(n2,n1))
    shot = int(file_name[9:])
    return D, shot
