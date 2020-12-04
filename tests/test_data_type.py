#!/usr/bin/env python
# --coding:utf-8--

# Copyright (c) 2020 vesoft inc. All rights reserved.
#
# This source code is licensed under Apache 2.0 License,
# attached with Common Clause Condition 1.0, found in the LICENSES directory.

import sys
import os
from datetime import date


current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, '..')
sys.path.insert(0, root_dir)

from nebula2.Exception import InvalidKeyException
from nebula2.common.ttypes import Value, NullType, Time, DateTime, Set, Date, List, Map
from nebula2.common import ttypes
from nebula2.graph import ttypes as graphTtype
from unittest import TestCase
from nebula2.data.ResultSet import ResultSet
from nebula2.data.DataObject import (
    ValueWrapper,
    Node,
    Relationship,
    PathWrapper,
    TimeWrapper, DateTimeWrapper, DateWrapper, Null)


class TestBaseCase(TestCase):
    @classmethod
    def get_vertex_value(self, vid):
        vertex = ttypes.Vertex()
        vertex.vid = vid
        vertex.tags = list()
        for i in range(0, 3):
            tag = ttypes.Tag()
            tag.name = ('tag{}'.format(i)).encode('utf-8')
            tag.props = dict()
            for j in range(0, 5):
                value = ttypes.Value()
                value.set_iVal(j)
                tag.props[('prop{}'.format(j)).encode('utf-8')] = value
            vertex.tags.append(tag)
        return vertex

    @classmethod
    def get_edge_value(self, src_id, dst_id):
        edge = ttypes.Edge()
        edge.src = src_id
        edge.dst = dst_id
        edge.type = 1
        edge.name = b'classmate'
        edge.ranking = 100
        edge.props = dict()
        for i in range(0, 5):
            value = ttypes.Value()
            value.set_iVal(i)
            edge.props[('prop{}'.format(i)).encode('utf-8')] = value
        return edge

    @classmethod
    def get_path_value(self, start_id, steps=5):
        path = ttypes.Path()
        path.src = self.get_vertex_value(start_id)
        path.steps = list()
        for i in range(0, steps):
            step = ttypes.Step()
            step.dst = self.get_vertex_value(('vertex{}'.format(i)).encode('utf-8'))
            step.type = 1 if i % 2 == 0 else -1
            step.name = b'classmate'
            step.ranking = 100
            step.props = dict()
            for i in range(0, 5):
                value = ttypes.Value()
                value.set_iVal(i)
                step.props[('prop{}'.format(i)).encode('utf-8')] = value
            path.steps.append(step)
        return path

    @classmethod
    def get_result_set(self):
        resp = graphTtype.ExecutionResponse()
        resp.error_code = graphTtype.ErrorCode.E_BAD_PERMISSION
        resp.error_msg = b"Permission"
        resp.comment = b"Permission"
        resp.space_name = b"test"
        resp.latency_in_us = 100
        data_set = ttypes.DataSet()
        data_set.column_names = [b"col1_empty",
                                 b"col2_null",
                                 b"col3_bool",
                                 b"col4_int",
                                 b"col5_double",
                                 b"col6_string",
                                 b"col7_list",
                                 b"col8_set",
                                 b"col9_map",
                                 b"col10_time",
                                 b"col11_date",
                                 b"col12_datetime",
                                 b"col13_vertex",
                                 b"col14_edge",
                                 b"col15_path"]
        row = ttypes.Row()
        row.values = []
        value1 = ttypes.Value()
        row.values.append(value1)
        value2 = ttypes.Value()
        value2.set_nVal(NullType.BAD_DATA)
        row.values.append(value2)
        value3 = ttypes.Value()
        value3.set_bVal(False)
        row.values.append(value3)
        value4 = ttypes.Value()
        value4.set_iVal(100)
        row.values.append(value4)
        value5 = ttypes.Value()
        value5.set_fVal(10.01)
        row.values.append(value5)
        value6 = ttypes.Value()
        value6.set_sVal(b"hello world")
        row.values.append(value6)
        value7 = ttypes.Value()
        str_val1 = ttypes.Value()
        str_val1.set_sVal(b"word")
        str_val2 = ttypes.Value()
        str_val2.set_sVal(b"car")
        list_val = List()
        list_val.values = [str_val1, str_val2]
        value7.set_lVal(list_val)
        row.values.append(value7)
        value8 = ttypes.Value()
        set_val = Set()
        set_val.values = set()
        set_val.values.add(str_val1)
        set_val.values.add(str_val2)
        value8.set_uVal(set_val)
        row.values.append(value8)
        value9 = ttypes.Value()
        map = Map()
        map.kvs = {b"a": str_val1, b"b": str_val2}
        value9.set_mVal(map)
        row.values.append(value9)
        value10 = ttypes.Value()
        value10.set_tVal(Time(10, 10, 10, 10000))
        row.values.append(value10)
        value11 = ttypes.Value()
        value11.set_dVal(date(2020, 10, 1))
        row.values.append(value11)
        value12 = ttypes.Value()
        value12.set_dtVal(DateTime(2020, 10, 1, 10, 10, 10, 10000))
        row.values.append(value12)
        value13 = ttypes.Value()
        value13.set_vVal(self.get_vertex_value(b"Tom"))
        row.values.append(value13)
        value14 = ttypes.Value()
        value14.set_eVal(self.get_edge_value(b"Tom", b"Lily"))
        row.values.append(value14)
        value15 = ttypes.Value()
        value15.set_pVal(self.get_path_value(b"Tom", 3))
        row.values.append(value15)
        data_set.rows = []
        data_set.rows.append(row)
        resp.data = data_set
        return ResultSet(resp)


class TesValueWrapper(TestBaseCase):
    def test_as_bool(self):
        value = ttypes.Value()
        value.set_bVal(False)
        value_wrapper = ValueWrapper(value)
        assert value_wrapper.is_bool()

        node = value_wrapper.as_bool()
        assert isinstance(node, bool)

    def test_as_int(self):
        value = ttypes.Value()
        value.set_iVal(100)
        value_wrapper = ValueWrapper(value)
        assert value_wrapper.is_int()

        node = value_wrapper.as_int()
        assert isinstance(node, int)

    def test_as_double(self):
        value = ttypes.Value()
        value.set_fVal(10.10)
        value_wrapper = ValueWrapper(value)
        assert value_wrapper.is_double()

        node = value_wrapper.as_double()
        assert isinstance(node, float)

    def test_as_string(self):
        value = ttypes.Value()
        value.set_sVal(b'Tom')
        value_wrapper = ValueWrapper(value)
        assert value_wrapper.is_string()

        str_val = value_wrapper.as_string()
        assert isinstance(str_val, str)

    def test_as_list(self):
        value = ttypes.Value()
        str_val1 = ttypes.Value()
        str_val1.set_sVal(b"word")
        str_val2 = ttypes.Value()
        str_val2.set_sVal(b"car")
        val_list = List()
        val_list.values = [str_val1, str_val2]
        value.set_lVal(val_list)
        value_wrapper = ValueWrapper(value)
        assert value_wrapper.is_list()

        list_val = value_wrapper.as_list()
        assert isinstance(list_val, list)
        expect_result = [ValueWrapper(ttypes.Value(sVal=b"word")),
                         ValueWrapper(ttypes.Value(sVal=b"car"))]
        assert list_val == expect_result

    def test_as_set(self):
        value = ttypes.Value()
        str_val1 = ttypes.Value()
        str_val1.set_sVal(b"word")
        str_val2 = ttypes.Value()
        str_val2.set_sVal(b"car")
        set_val = Set()
        set_val.values = set()
        set_val.values.add(str_val1)
        set_val.values.add(str_val2)
        value.set_uVal(set_val)
        value_wrapper = ValueWrapper(value)
        assert value_wrapper.is_set()

        set_val = value_wrapper.as_set()
        assert isinstance(set_val, set)
        expect_result = set()
        expect_result.add(ValueWrapper(ttypes.Value(sVal=b"word")))
        expect_result.add(ValueWrapper(ttypes.Value(sVal=b"car")))
        assert set_val == expect_result

    def test_as_map(self):
        value = ttypes.Value()
        str_val1 = ttypes.Value()
        str_val1.set_sVal(b"word")
        str_val2 = ttypes.Value()
        str_val2.set_sVal(b"car")
        map_val = Map()
        map_val.kvs = {b"a": str_val1, b"b": str_val2}
        value.set_mVal(map_val)
        value_wrapper = ValueWrapper(value)
        assert value_wrapper.is_map()

        map_val = value_wrapper.as_map()
        assert isinstance(map_val, dict)
        expect_result = dict()
        expect_result["a"] = ValueWrapper(ttypes.Value(sVal=b"word"))
        expect_result["b"] = ValueWrapper(ttypes.Value(sVal=b"car"))
        assert map_val == expect_result

    def test_as_time(self):
        time = Time()
        time.hour = 10
        time.minute = 20
        time.sec = 10
        time.microsec = 100
        value = ttypes.Value(tVal = time)
        value_wrapper = ValueWrapper(value)
        assert value_wrapper.is_time()

        time_val = value_wrapper.as_time()
        assert isinstance(time_val, TimeWrapper)
        assert time_val.get_hour() == 10
        assert time_val.get_minute() == 20
        assert time_val.get_sec() == 10
        assert time_val.get_microsec() == 100
        assert '10:20:10.000100' == str(time_val)

    def test_as_date(self):
        date = Date()
        date.year = 220
        date.month = 2
        date.day = 10
        value = ttypes.Value(dVal=date)
        value_wrapper = ValueWrapper(value)
        assert value_wrapper.is_date()

        date_val = value_wrapper.as_date()
        assert isinstance(date_val, DateWrapper)
        assert date_val.get_year() == 220
        assert date_val.get_month() == 2
        assert date_val.get_day() == 10
        assert '220-02-10' == str(date_val)

    def test_as_datetime(self):
        datetime = DateTime()
        datetime.year = 123
        datetime.month = 2
        datetime.day = 1
        datetime.hour = 10
        datetime.minute = 20
        datetime.sec = 10
        datetime.microsec = 100
        value = ttypes.Value(dtVal=datetime)
        value_wrapper = ValueWrapper(value)
        assert value_wrapper.is_datetime()

        datetime_val = value_wrapper.as_datetime()
        assert isinstance(datetime_val, DateTimeWrapper)
        assert datetime_val.get_hour() == 10
        assert datetime_val.get_minute() == 20
        assert datetime_val.get_sec() == 10
        assert datetime_val.get_microsec() == 100
        assert '123-02-01T10:20:10.000100' == str(datetime_val)

    def test_as_node(self):
        value = ttypes.Value()
        value.set_vVal(self.get_vertex_value(b'Tom'))
        value_wrapper = ValueWrapper(value)
        assert value_wrapper.is_vertex()

        node = value_wrapper.as_node()
        assert isinstance(node, Node)

    def test_as_relationship(self):
        value = ttypes.Value()
        value.set_eVal(self.get_edge_value(b'Tom', b'Lily'))
        value_wrapper = ValueWrapper(value)
        assert value_wrapper.is_edge()

        relationship = value_wrapper.as_relationship()
        assert isinstance(relationship, Relationship)

    def test_as_path(self):
        value = ttypes.Value()
        value.set_pVal(self.get_path_value(b'Tom'))
        vaue_wrapper = ValueWrapper(value)
        assert vaue_wrapper.is_path()

        node = vaue_wrapper.as_path()
        assert isinstance(node, PathWrapper)


class TestNode(TestBaseCase):
    def test_node_api(self):
        test_set = set()
        test_set.add(Value())
        node = Node(self.get_vertex_value(b'Tom'))
        assert 'Tom' == node.get_id()

        assert node.has_tag('tag2')

        assert ['prop0', 'prop1', 'prop2', 'prop3', 'prop4'] == node.prop_names('tag2')

        assert [0, 1, 2, 3, 4] == [(value.as_int()) for value in node.prop_values('tag2')]

        assert ['tag0', 'tag1', 'tag2'] == node.tags()

        expect_propertys = {}
        for key in node.propertys('tag2').keys():
            expect_propertys[key] = node.propertys('tag2')[key].as_int()
        assert {'prop0': 0, 'prop1': 1, 'prop2': 2, 'prop3': 3, 'prop4': 4} == expect_propertys


class TestRelationship(TestBaseCase):
    def test_relationship_api(self):
        relationship = Relationship(self.get_edge_value(b'Tom', b'Lily'))

        assert 'Tom' == relationship.start_vertex_id()

        assert 'Lily' == relationship.end_vertex_id()

        assert 100 == relationship.ranking()

        assert 100 == relationship.ranking()

        assert 'classmate' == relationship.edge_name()

        assert ['prop0', 'prop1', 'prop2', 'prop3', 'prop4'] == relationship.keys()

        expect_propertys = {}
        for key in relationship.propertys().keys():
            expect_propertys[key] = relationship.propertys()[key].as_int()
        assert {'prop0': 0, 'prop1': 1, 'prop2': 2, 'prop3': 3, 'prop4': 4} == expect_propertys


class TestPath(TestBaseCase):
    def test_path_api(self):
        path = PathWrapper(self.get_path_value(b'Tom'))
        assert Node(self.get_vertex_value(b'Tom')) == path.start_node()

        assert 5 == path.length()

        assert path.contain_node(Node(self.get_vertex_value(b'vertex3')))

        assert path.contain_relationship(Relationship(self.get_edge_value(b'vertex3', b'vertex2')))

        nodes = list()
        nodes.append(path.start_node())
        for i in range(0, 5):
            nodes.append(Node(self.get_vertex_value(('vertex'.format(i)).encode('utf-8'))))

        relationships = list()
        relationships.append(Relationship(self.get_edge_value(b'Tom', b'vertex0')))
        for i in range(0, 4):
            if i % 2 == 0:
                relationships.append(Relationship(
                    self.get_edge_value(('vertex{}'.format(i + 1)).encode('utf-8'),
                                        ('vertex{}'.format(i)).encode('utf-8'))))
            else:
                relationships.append(Relationship(
                    self.get_edge_value(('vertex{}'.format(i)).encode('utf-8'),
                                        ('vertex{}'.format(i + 1)).encode('utf-8'))))

        assert relationships == path.relationships()


class TestResultset(TestBaseCase):
    def test_all_interface(self):
        result = self.get_result_set()
        assert result.space_name() == "test"
        assert result.comment() == "Permission"
        assert result.error_msg() == "Permission"
        assert result.error_code() == graphTtype.ErrorCode.E_BAD_PERMISSION
        assert result.plan_desc() is None
        assert result.latency() == 100
        assert not result.is_empty()
        assert not result.is_succeeded()
        expect_keys = ["col1_empty",
                       "col2_null",
                       "col3_bool",
                       "col4_int",
                       "col5_double",
                       "col6_string",
                       "col7_list",
                       "col8_set",
                       "col9_map",
                       "col10_time",
                       "col11_date",
                       "col12_datetime",
                       "col13_vertex",
                       "col14_edge",
                       "col15_path"]
        assert result.keys() == expect_keys
        assert result.col_size() == 15
        assert result.row_size() == 1

        # test column_values
        assert len(result.column_values("col6_string")) == 1
        assert result.column_values("col6_string")[0].is_string()
        assert result.column_values("col6_string")[0].as_string() == "hello world"
        # test row_values
        assert len(result.row_values(0)) == 15
        assert result.row_values(0)[5].is_string()
        assert result.row_values(0)[5].as_string() == "hello world"

        # test rows
        assert len(result.rows()) == 1
        assert len(result.rows()[0].values) == 15
        assert isinstance(result.rows()[0].values[0], Value)
        assert isinstance(result.get_row_types(), list)

        # test get_row_types
        assert result.get_row_types() == [ttypes.Value.__EMPTY__,
                                          ttypes.Value.NVAL,
                                          ttypes.Value.BVAL,
                                          ttypes.Value.IVAL,
                                          ttypes.Value.FVAL,
                                          ttypes.Value.SVAL,
                                          ttypes.Value.LVAL,
                                          ttypes.Value.UVAL,
                                          ttypes.Value.MVAL,
                                          ttypes.Value.TVAL,
                                          ttypes.Value.DVAL,
                                          ttypes.Value.DTVAL,
                                          ttypes.Value.VVAL,
                                          ttypes.Value.EVAL,
                                          ttypes.Value.PVAL]

        # test record
        in_use = False
        for record in result:
            in_use = True
            record.size() == 15

            # test keys()
            assert record.keys() == expect_keys
            # test values()
            values = record.values()
            assert len(record.values()) == 15
            assert record.values()[0].is_empty()
            assert record.values()[5].is_string()
            assert record.values()[5].is_string()
            assert record.values()[5].as_string() == "hello world"

            # test get_value()
            assert record.get_value(0).is_empty()
            assert values[0].is_empty()
            assert record.get_value(1).is_null()
            assert record.get_value(1).as_null() == Null(Null.BAD_DATA)
            assert str(record.get_value(1).as_null()) == 'BAD_DATA'

            # test get_value_by_key()
            assert record.get_value_by_key('col2_null').is_null()
            assert record.get_value_by_key('col3_bool').is_bool()
            assert not record.get_value_by_key('col3_bool').as_bool()

            # get_value_by_key with not exited key
            try:
                record.get_value_by_key('not existed')
                assert False, 'Not expect here'
            except InvalidKeyException as e:
                assert True
                assert e.message == "KeyError: `not existed'"
            assert values[1].is_null()
            assert record.get_value(2).is_bool()
            assert not record.get_value(2).as_bool()
            assert record.get_value(2).is_bool()
            assert record.get_value(3).is_int()
            assert record.get_value(3).as_int() == 100
            assert record.get_value(4).is_double()
            assert record.get_value(4).as_double() == 10.01
            assert record.get_value(5).is_string()
            assert record.get_value(5).as_string() == "hello world"
            assert record.get_value(6).is_list()
            assert record.get_value(7).is_set()
            assert record.get_value(8).is_map()
            assert record.get_value(9).is_time()
            assert record.get_value(10).is_date()
            assert record.get_value(11).is_datetime()
            assert record.get_value(12).is_vertex()
            assert record.get_value(13).is_edge()
            assert record.get_value(14).is_path()
        assert in_use

        # test use iterator again
        in_use = False
        for record in result:
            in_use = True
            record.size() == 15
        assert in_use

