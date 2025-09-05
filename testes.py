class A:
    pass
class B(A):
    pass
class C(B):
    pass
class D(C):
    pass
class E(D):
    pass

if __name__ == '__main__':
    a = A()
    b = B()
    c = C()
    d = D()
    e = E()
    print(a, type(a), isinstance(a,A), isinstance(a, A))
    print(b, type(b), isinstance(b,B), isinstance(b, A))
    print(c, type(c), isinstance(c,C), isinstance(c, A))
    print(d, type(d), isinstance(d,D), isinstance(d, A))
    print(e, type(e), isinstance(e,E), isinstance(e, A))