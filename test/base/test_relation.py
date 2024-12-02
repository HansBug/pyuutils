import pytest

from pyuutils.base import Relation, sym_relation, sub2super, super2sub


@pytest.mark.unittest
class TestRelation:
    @pytest.mark.parametrize(['i', 'o'], [
        (Relation.DIFFERENT, 0),
        (Relation.SUPERSET, 1),
        (Relation.GREATER, 1),
        (Relation.SUBSET, 2),
        (Relation.LESS, 2),
        (Relation.EQUAL, 3),
    ])
    def test_relation_value(self, i, o):
        assert i.value == o

    @pytest.mark.parametrize(['i', 'o'], [
        (0, Relation.DIFFERENT),
        (1, Relation.SUPERSET),
        (1, Relation.GREATER),
        (2, Relation.SUBSET),
        (2, Relation.LESS),
        (3, Relation.EQUAL),
        (-1, ValueError),
        (4, ValueError),
    ])
    def test_relation_from_raw(self, i, o):
        if isinstance(o, type) and issubclass(o, Exception):
            with pytest.raises(o):
                _ = Relation.from_raw(i)
        else:
            assert Relation.from_raw(i) == o

    @pytest.mark.parametrize(['i', 'o'], [
        (Relation.DIFFERENT, Relation.DIFFERENT),
        (Relation.SUPERSET, Relation.SUBSET),
        (Relation.SUBSET, Relation.SUPERSET),
        (Relation.EQUAL, Relation.EQUAL),
    ])
    def test_sym_relation(self, i, o):
        assert sym_relation(i) == o

    @pytest.mark.parametrize(['i', 'o'], [
        (Relation.DIFFERENT, Relation.DIFFERENT),
        (Relation.SUPERSET, Relation.DIFFERENT),
        (Relation.SUBSET, Relation.SUPERSET),
        (Relation.EQUAL, Relation.SUPERSET),
    ])
    def test_sub2super(self, i, o):
        assert sub2super(i) == o

    @pytest.mark.parametrize(['i', 'o'], [
        (Relation.DIFFERENT, Relation.DIFFERENT),
        (Relation.SUPERSET, Relation.SUBSET),
        (Relation.SUBSET, Relation.DIFFERENT),
        (Relation.EQUAL, Relation.SUBSET),
    ])
    def test_super2sub(self, i, o):
        assert super2sub(i) == o
