from inbox.util import get_all_subclasses


def test_get_all_subclasses():
    class Base:
        pass

    class A(Base):
        pass

    class B(Base):
        pass

    class C(A):
        pass

    subclasses = get_all_subclasses(Base)
    assert subclasses == {A, B, C}
