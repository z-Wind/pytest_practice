def test_tmpdir(tmpdir):
    tmdir_same_part(tmpdir)


def test_tmpdir_factory(tmpdir_factory):
    dir_ = tmpdir_factory.mktemp("mydir")

    # 印出暫存位置
    base_temp = tmpdir_factory.getbasetemp()
    print("base:", base_temp)

    tmdir_same_part(dir_)


def tmdir_same_part(dir_):
    file1 = dir_.join("fileName1.txt")
    sub_dir = dir_.mkdir("dirName")
    file2 = sub_dir.join("fileName2.txt")

    file1.write("一二三")
    file2.write("四五六")

    assert file1.read() == "一二三"
    assert file2.read() == "四五六"


# =====================================================================================

import pytest


# pytestconfig fixtures
def test_pytestconfig_option(pytestconfig):
    print('"name" :', pytestconfig.getoption("name"), pytestconfig.option.name)
    print('"mybool" :', pytestconfig.getoption("mybool"), pytestconfig.option.mybool)


# pytestconfig fixtures
def test_pytestconfig(pytestconfig):
    print("args            :", pytestconfig.args)
    print("inifile         :", pytestconfig.inifile)
    print("invocation_dir  :", pytestconfig.invocation_dir)
    print("rootdir         :", pytestconfig.rootdir)
    print("-k EXPRESSION   :", pytestconfig.getoption("keyword"))
    print("-v, --verbose   :", pytestconfig.getoption("verbose"))
    print("-q, --quiet     :", pytestconfig.getoption("--quiet"))
    print("-l, --showlocals:", pytestconfig.getoption("showlocals"))
    print("--tb=style      :", pytestconfig.getoption("tbstyle"))


# request fixtures
def test_pytestconfig_legacy(request):
    print('\n"name" :', request.config.getoption("name"))
    print('"myopt" :', request.config.getoption("mybool"))
    print('"keyword" :', request.config.getoption("keyword"))


# =============================================================================

import pytest
import datetime
import random
import time
from collections import namedtuple

Duration = namedtuple("Duration", ["current", "last"])


@pytest.fixture(scope="session")
def duration_cache(request):
    # 存放的資料夾與檔名
    key = "folder/fileName"
    d = Duration({}, request.config.cache.get(key, {}))
    yield d
    request.config.cache.set(key, d.current)


@pytest.fixture()
def check_duration(request, duration_cache):
    d = duration_cache
    nodeid = request.node.nodeid
    start_time = datetime.datetime.now()
    yield
    duration = (datetime.datetime.now() - start_time).total_seconds()
    d.current[nodeid] = duration
    if d.last.get(nodeid, None) is not None:
        errorstring = "測試時間是上次的兩倍"
        assert duration <= (d.last[nodeid] * 2), errorstring


@pytest.mark.parametrize("i", range(5))
def test_cache(i, check_duration):
    time.sleep(random.random())


# ================================================================================

import sys
import pytest


def capsys_Hi(name):
    print("Hi, {}".format(name))
    print("有錯誤", file=sys.stderr)


def test_capsys_Hi(capsys):
    capsys_Hi("一")
    out, err = capsys.readouterr()
    assert out == "Hi, 一\n"
    assert "錯誤" in err

    capsys_Hi("二")
    capsys_Hi("三")
    out, err = capsys.readouterr()
    assert out == "Hi, 二\nHi, 三\n"
    assert err == ""


def test_capsys_disabled(capsys):
    with capsys.disabled():
        print("\n總是顯示")
    print("有 -s 才顯示")


# =======================================================================

import math


def test_monkeypatch(monkeypatch):
    d = {"a": 1}
    assert d.get("a") == 1
    monkeypatch.setitem(d, "a", 100)
    assert d.get("a") == 100

    with monkeypatch.context() as m:
        m.setattr(math, "cos", (lambda x: x))
        assert math.cos("a") == "a"
    assert math.cos(math.pi) == -1
