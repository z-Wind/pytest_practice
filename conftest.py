# pytest_addoption 是特定名字
def pytest_addoption(parser):
    parser.addoption("--mybool", action="store_true", help="boolean option")
    parser.addoption("--name", action="store", default="abc", help="name: abc or ABC")


# =======================================================================

