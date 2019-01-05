import pytest


def test_basic():
    assert 1 == 1


# ============================================================================================


def test_exception():
    with pytest.raises(TypeError):
        raise TypeError


# ============================================================================================


@pytest.mark.fruits
def test_apple():
    assert 1 == 1


@pytest.mark.fruits
@pytest.mark.vegetable
def test_tomato():
    assert 1 == 1


# ============================================================================================


@pytest.mark.skip(reason="skip this")
def test_skip():
    assert False


import sys


@pytest.mark.skipif(sys.version_info < (4, 3), reason="requires python4.3")
def test_skipif():
    assert False


# ============================================================================================


@pytest.mark.xfail(reason="fail but still test")
def test_xfail():
    assert False


@pytest.mark.xfail(reason="fail but still test maybe pass")
def test_xpass():
    assert True


version = (1, 0, 0)


@pytest.mark.xfail(version < (0, 5, 0), reason="if version over 0.5.0, it should pass")
def test_condition_xfail():
    assert True


# ============================================================================================


@pytest.mark.parametrize("a,b,c", [(1, 2, 3), (4, 5, 6)])
def test_para(a, b, c):
    assert (a, b, c) == (1, 2, 3)


@pytest.mark.parametrize("a,b,c", [(1, 2, 3), (4, 5, 6)], ids=["tuple1", "tuple2"])
def test_para_ids(a, b, c):
    assert (a, b, c) == (1, 2, 3)


def ids_func(t):
    return "[{}]".format(t)


@pytest.mark.parametrize("a,b,c", [(1, 2, 3), (4, 5, 6)], ids=ids_func)
def test_para_ids_func(a, b, c):
    assert (a, b, c) == (1, 2, 3)


class Info:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


@pytest.mark.parametrize("i", [Info(1, 2, 3), Info(4, 5, 6)])
def test_para_class(i):
    assert i == Info(1, 2, 3)


def ids_class_func(t):
    return "Info({},{},{})".format(t.a, t.b, t.c)


@pytest.mark.parametrize("i", [Info(1, 2, 3), Info(4, 5, 6)], ids=ids_class_func)
def test_para_ids_class_func(i):
    assert i == Info(1, 2, 3)


@pytest.mark.parametrize(
    "i",
    [
        pytest.param(Info(1, 2, 3), id="basic"),
        pytest.param(Info(4, 5, 6), id="advance"),
    ],
)
def test_para_ids_setting(i):
    assert i == Info(1, 2, 3)


# ============================================================================================


@pytest.fixture
def fixture_fun1():
    return 1


@pytest.fixture
def fixture_fun2():
    print("\nsetup")
    yield 1
    print("\nteardown")


def test_fixture(fixture_fun1, fixture_fun2):
    assert fixture_fun1 == 1
    assert fixture_fun2 == 1


# ============================================================================================


@pytest.fixture(scope="function")
def func_scope():
    pass


@pytest.fixture(scope="module")
def mod_scope():
    pass


@pytest.fixture(scope="session")
def sess_scope():
    pass


@pytest.fixture(scope="class")
def class_scope():
    pass


def test_fixture_scope1(sess_scope, mod_scope, func_scope):
    pass


def test_fixture_scope2(sess_scope, mod_scope, func_scope):
    pass


@pytest.mark.usefixtures("class_scope")
class TestClassFixtures:
    def test_method1(self, mod_scope):
        pass

    def test_method2(self, func_scope):
        pass


# ============================================================================================


@pytest.fixture
def func_scope_with_sess_scope(sess_scope):
    pass


def test_fixture_with_fixture(func_scope_with_sess_scope):
    pass


# Error: ScopeMismatch
@pytest.fixture(scope="session")
def sess_scope_with_func_scope(func_scope):
    pass


def test_fixture_with_wrong_fixture(sess_scope_with_func_scope):
    pass


# ============================================================================================


@pytest.fixture(name="shortName")
def fixture_name_too_long():
    pass


def test_fixture_rename(shortName):
    pass


# ============================================================================================


@pytest.fixture(params=[(1, 2, 3), [4, 5, 6]])
def func_fixture_para(request):
    return request.param


def test_fixture_para(func_fixture_para):
    assert func_fixture_para == (1, 2, 3)


@pytest.fixture(params=[(1, 2, 3), [4, 5, 6]], ids=["tuple1", "tuple2"])
def func_fixture_para_ids(request):
    return request.param


def test_fixture_para_ids(func_fixture_para_ids):
    assert func_fixture_para_ids == (1, 2, 3)


def ids_func_fixture(t):
    return "{},{},{}".format(t[0], t[1], t[2])


@pytest.fixture(params=[(1, 2, 3), [4, 5, 6]], ids=ids_func_fixture)
def func_fixture_para_idsFunc(request):
    return request.param


def test_fixture_para_ids_func(func_fixture_para_idsFunc):
    assert func_fixture_para_idsFunc == (1, 2, 3)
