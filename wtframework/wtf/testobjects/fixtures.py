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
from abc import abstractmethod
import abc


class AbstractFixture(object):
    """
    Interface for test fixture.  Test fixtures contain both an init, and 
    cleanup steps which are called by the TestFixtureManager at the end 
    of a test to clean up after the fixture.
    """
    # This class needs to subclassed.
    __metaclass__ = abc.ABCMeta
    
    
    @abstractmethod
    def initialize(self, *args, **kwargs):
        """
        Define your fixture.  Set your fixture member variable values.
        
        self.user = self.init('user', User)
        self.project_name = self.init('project_name', "TestProject")
        """
        pass

    @abstractmethod
    def get_value(self):
        """
        Returns the ID/value that represents this fixture.  For example, a 
        Project fixture will return a project ID.
        """
        pass
    
    @abstractmethod
    def tear_down(self):
        """
        Define your fixture clean up here.
        """
        pass
    

    def init(self, name_of_keyword_arg, default_value_or_fixture, *args, **kwargs):
        """
        Initialize a fixture value.
        @param name_of_keyword_arg: Name of keyword param to check.
        @param default_value_or_fixture: default value of fixture you wish to use if value is not provided.
        @param *args: Additional args to pass to the fixture if target keyword param is not specified.
        @param **kwargs: Additional keyword args to pass to the fixture if target keyword param is not specified.   
        """
        try:
            return self.__passed_in_kwargs__[name_of_keyword_arg]
        except:
            try:
                if issubclass(default_value_or_fixture, AbstractFixture):
                    #Handle fixture init.
                    return self.__fixture_manager__.create_fixture(default_value_or_fixture, *args, **kwargs).get_value()
            except TypeError:
                pass
            
            return default_value_or_fixture

    
    def __init__(self, fixture_manager, *args, **kwargs):
        "Init that's called by the fixture manager."
        self.__fixture_manager__ = fixture_manager
        self.__passed_in_args__ = args
        self.__passed_in_kwargs__ = kwargs
        
        self.initialize(*args, **kwargs)
    
    

class FixtureManager(object):
    """
    Manages fixtures for a test.  Use this class to instantiate fixtures, then when the test is 
    complete, use the 'tear_down()' method to call clean up on all registered fixtures.
    """
    
    def __init__(self):
        self.__registered_fixtures = [];
    
    def create_fixture(self, fixture_class, *args, **kwargs):
        """
        Instantiate a test fixture and return an instance of this test fixutre which is registered 
        to this FixtureManager for later cleanup.
        
        @param fixture_class: Fixture class that subclasses ITestFixture
        @return: ITestFixture 
        """
        fixture = fixture_class(self, *args, **kwargs)
        self._register_fixture(fixture)
        return fixture
    
    def _register_fixture(self, fixture):
        """
        Register a test fixture.
        
        Ideally fixtures should of already been registered upon creation.
        """
        self.__registered_fixtures.append(fixture)
    
    def tear_down(self):
        """
        Tear down all registered fixtures.
        """
        exceptions = []
        for fixture in self.__registered_fixtures:
            try:
                fixture.tear_down();
            except Exception as e:
                exceptions.append(e)
        
        # Empty out the fixture manager so it can be used by the next test.
        self.__registered_fixtures = []
        
        if len(exceptions) > 0:
            raise FixtureTearDownException(*tuple(exceptions))




class FixtureTearDownException(RuntimeError):
    "Thrown when 1 or more exceptions are thrown during tear down."
    
    def __init__(self, *args, **kwargs):
        super(FixtureTearDownException, self).__init__(*args, **kwargs)
        self.exception_list = args
    
    #Overriding __str__ to make the error message easier to read.
    def __str__(self, *args, **kwargs):
        exception_string = ""
        count = 0
        for exception_entry in self.exception_list:
            count += 1
            exception_string += "\nError {0}: ".format(count) + exception_entry.__str__()
        
        return RuntimeError.__str__(self, *args, **kwargs) + exception_string