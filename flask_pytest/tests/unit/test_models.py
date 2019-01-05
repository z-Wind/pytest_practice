from flaskr.models import User


def test_new_User(new_User):
    assert new_User.name == "Sun"


def test_init_db(init_db, new_User):
    init_db.session.add(new_User)
    init_db.session.commit()
    assert User.query.first().name == "Sun"
