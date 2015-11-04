# -*- coding: utf-8 -*-
import logging

import pytest
from django.db import connections

from demo.models import DropTriggerConcurrentModel

from concurrency.triggers import factory

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_list_triggers():
    conn = connections['default']

    assert factory(conn).get_list() == [
        u'concurrency_demo_droptriggerconcurrentmodel_version',
        u'concurrency_demo_triggerconcurrentmodel_version']


@pytest.mark.django_db
def test_drop_triggers():
    conn = connections['default']
    f = [f for f in DropTriggerConcurrentModel._meta.fields if f.name == 'version'][0]
    ret = factory(conn).drop(f)
    assert ret == [u'concurrency_demo_droptriggerconcurrentmodel_version']
    assert factory(conn).get_list() == [u'concurrency_demo_triggerconcurrentmodel_version']