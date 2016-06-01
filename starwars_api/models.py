from starwars_api.client import SWAPIClient
from starwars_api.exceptions import SWAPIClientError

api_client = SWAPIClient()


class BaseModel(object):

    def __init__(self, json_data):
        """
        Dynamically assign all attributes in `json_data` as instance
        attributes of the Model.
        """
        for key, value in json_data.iteritems():
            setattr(self, key, value)

    @classmethod
    def get(cls, resource_id):
        """
        Returns an object of current Model requesting data to SWAPI using
        the api_client.
        """
        res_name = cls.RESOURCE_NAME
        method_name = 'get_{}'.format(res_name)
        #print('method name is now: {}').format(method_name)
        result = getattr(api_client, method_name)
        return cls(result(resource_id))

    @classmethod
    def all(cls):
        """
        Returns an iterable QuerySet of current Model. The QuerySet will be
        later in charge of performing requests to SWAPI for each of the
        pages while looping.
        """
        
        # QSN should be set to something like PeopleQuerySet
        # based on the RESOURCE_NAME 'people'
        res_name = cls.RESOURCE_NAME # res name is 'people'
        res_name = res_name.capitalize() # now res name is 'People'
        QuerySetName = '{}QuerySet'.format(res_name) # now 'PeopleQuerySet'
        print('qsn is now: {}').format(QuerySetName)
        # I thnk this line is reutnring 'cls.QuerySetName and not cls.[interpolated name]'
        # this SHOULD return cls.PeopleQuerySet
        return cls.QuerySetName()  # Real function
        # return cls.PeopleQuerySet()  # Test function

'''
class PeopleIterator(object):
    def __init__(self):
        self.index = 0
        self.page = None
        self.count = None
        self.next_page_number = 1
        
    def make_request(self):
        json_page_file_name = "page{page_num}.json".format(
            page_num=self.next_page_number)
        with open(json_page_file_name, 'r') as fp:
            self.page = json.load(fp)
        self.next_page_number += 1
    
    def __next__(self):
        if self.page is None:
            self.make_request()

        if self.index == 10:
            self.index = 0
            self.make_request()

        if self.index >= self.count:
            raise StopIteration

        elem = self.page['results'][self.index]
        self.index += 1
        return elem
    
    next = __next__
    
    def __iter__(self):
        return self
'''

class People(BaseModel):
    """Representing a single person"""
    RESOURCE_NAME = 'people'

    def __init__(self, json_data):
        super(People, self).__init__(json_data)

    def __repr__(self):
        return 'Person: {0}'.format(self.name)

    '''    
    @classmethod
    def get(cls, person_id):
        # should return the dictionary for the person id.
        # api_client object for querying already exists.
        result = api_client.get_people(people_id = person_id)
        #print(result['name'])
        for key in result.keys():
            #print('Key is {}').format(key)
            self.key = result.get(key)
            # self.name = 'Luke Skywalker'
            #print('Setting attribute to key: {} with value {}').format(key, result[key])


    @classmethod
    def all(cls):
        return PeopleIterator()
    '''

class Films(BaseModel):
    RESOURCE_NAME = 'films'

    def __init__(self, json_data):
        super(Films, self).__init__(json_data)

    def __repr__(self):
        return 'Film: {0}'.format(self.title)


class BaseQuerySet(object):

    def __init__(self):
        self.index = 0
        self.page = None
        self.count = None
        self.next_page_number = 1

    def __iter__(self):
        return self

    def make_request(self):
        json_page_file_name = "page{page_num}.json".format(
            page_num=self.next_page_number)
        with open(json_page_file_name, 'r') as fp:
            self.page = json.load(fp)
        self.next_page_number += 1
        
    def __next__(self):
        """
        Must handle requests to next pages in SWAPI when objects in the current
        page were all consumed.
        """
        if self.page is None:
            self.make_request()

        if self.index == 10:
            self.index = 0
            self.make_request()

        if self.index >= self.count:
            raise StopIteration

        elem = self.page['results'][self.index]
        self.index += 1
        return elem        

    next = __next__

    def count(self):
        """
        Returns the total count of objects of current model.
        If the counter is not persisted as a QuerySet instance attr,
        a new request is performed to the API in order to get it.
        """

        res_name = cls.RESOURCE_NAME
        method_name = 'get_{}'.format(res_name)
        return getattr(api_client, method_name)['count']


class PeopleQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'people'

    def __init__(self):
        super(PeopleQuerySet, self).__init__()

    def __repr__(self):
        return 'PeopleQuerySet: {0} objects'.format(str(len(self.objects)))


class FilmsQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'films'

    def __init__(self):
        super(FilmsQuerySet, self).__init__()

    def __repr__(self):
        return 'FilmsQuerySet: {0} objects'.format(str(len(self.objects)))
