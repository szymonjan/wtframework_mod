##########################################################################
#This file is part of WTFramework. 
#
#    WTFramework is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WTFramework is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WTFramework.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################
import unittest
from wtframework.wtf.testobjects.fixtures import AbstractFixture, FixtureManager


class TestFixtureManager(unittest.TestCase):


    def test_fixture_is_created_and_initialized(self):
        "Test initializing a fixture with no params."
        fixture_mgr = FixtureManager()
        my_fixture = fixture_mgr.create_fixture(MyTestFixture1)
        self.assertIsNotNone(my_fixture)
        self.assertIsInstance(my_fixture, MyTestFixture1)
        self.assertTrue(my_fixture.initialized_was_called)

    def test_fixture_is_created_with_params(self):
        "Test we can pass in keyword params to initialize value."
        fixture_mgr = FixtureManager()
        my_fixture = fixture_mgr.create_fixture(MyTestFixture1, pass_value="hello")
        self.assertEqual(my_fixture.pass_value, "hello")

    def test_fixture_is_created_with_defaults(self):
        "Test defaults could be provided."
        fixture_mgr = FixtureManager()
        my_fixture = fixture_mgr.create_fixture(MyTestFixture1)
        self.assertEqual(my_fixture.pass_hello, "world")

    def test_fixture_cleanup_is_called(self):
        "Test cleanup is called."
        fixture_mgr = FixtureManager()
        my_fixture = fixture_mgr.create_fixture(MyTestFixture1)
        my_fixture2 = fixture_mgr.create_fixture(MyTestFixture1)
        fixture_mgr.tear_down()
        self.assertTrue(my_fixture.clean_up_was_called)
        self.assertTrue(my_fixture2.clean_up_was_called)

    def test_fixture_can_use_other_fixtures(self):
        "Test that the 2nd fixture is created and the value is returned to the first fixture."
        fixture_mgr = FixtureManager()
        my_fixture = fixture_mgr.create_fixture(MyTestFixture2)
        self.assertEqual(my_fixture.a_fixture, 999)

    def test_fixture_uses_default_value_if_provided_instead_of_a_default_fixture(self):
        "Test that the 2nd fixture is created and the value is returned to the first fixture."
        fixture_mgr = FixtureManager()
        my_fixture = fixture_mgr.create_fixture(MyTestFixture2, a_fixture = 555)
        self.assertEqual(my_fixture.a_fixture, 555)

    def test_subfixtures_get_cleaned_up(self):
        "Test that the 2nd fixture is created and the value is returned to the first fixture."
        fixture_mgr = FixtureManager()
        _ = fixture_mgr.create_fixture(MyTestFixture2)
        fixture_mgr.tear_down()
        self.assertTrue(MyTestFixture1.is_cleaned_up)
        self.assertTrue(MyTestFixture2.is_cleaned_up)


class MyTestFixture1(AbstractFixture):
    def initialize(self, *args, **kwargs):
        self.initialized_was_called = True
        self.pass_value = self.init('pass_value', None)
        self.pass_hello = self.init('pass_hello', "world")
        MyTestFixture1.is_cleaned_up = False

    def get_value(self):
        return 999;

    def tear_down(self):
        self.clean_up_was_called = True
        MyTestFixture1.is_cleaned_up = True

class MyTestFixture2(AbstractFixture):
    def initialize(self, *args, **kwargs):
        self.a_fixture = self.init('a_fixture', MyTestFixture1)
        MyTestFixture2.is_cleaned_up = False

    def get_value(self):
        return 8080;

    def tear_down(self):
        self.clean_up_was_called = True
        MyTestFixture2.is_cleaned_up = True


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()