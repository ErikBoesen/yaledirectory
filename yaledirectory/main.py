import requests
import re
from lxml import html


class Person(dict):
    def __init__(self, raw):
        self.update(raw)
        self.update(self.__dict__)

        self.directory_title = raw.get('DirectoryTitle')
        self.first_name = raw.get('FirstName')
        self.known_as = raw.get('KnownAs')
        self.last_name = raw.get('LastName')
        self.display_name = raw.get('DisplayName', (self.known_as or self.first_name) + ' ' + self.last_name)
        self.matched = raw.get('Matched')
        self.netid = raw.get('NetId')
        self.phone_number = raw.get('PhoneNumber')
        self.primary_organization_name = raw.get('PrimaryOrganizationName')
        self.primary_school_code = raw.get('PrimarySchoolCode')
        self.primary_school_name = raw.get('PrimarySchoolName')
        self.residential_college_name = raw.get('ResidentialCollegeName')
        self.student_curriculum = raw.get('StudentCurriculum')
        self.student_expected_graduation_year = raw.get('StudentExpectedGraduationYear')
        self.upi = raw.get('UPI')
        self.internal_location = raw.get('InternalLocation')


class YaleDirectory:
    API_ROOT = 'https://directory.yale.edu/'
    LOGIN_URL = 'https://secure.its.yale.edu/cas/login'

    def __init__(self, people_search_session_cookie, csrf_token):
        self.session = requests.Session()
        headers = {
            'X-CSRF-Token': 'mcz/aFs98WvNml9m3wlhmQTGKkX5Pa9fclcLnuxWFHfzpLBAWD4rRYZFQglzq8sSssDB0PibeS5Yh6iaSBTEYQ==',
            'Content-Type': 'application/json',
        }
        self.session.headers.update(headers)

    def get(self, endpoint: str, params: dict = {}):
        """
        Make a GET request to the API.

        :param params: dictionary of custom params to add to request.
        """
        request = self.session.get(self.API_ROOT + endpoint, params=params)
        if request.ok:
            return request.json()
        else:
            # TODO: Can we be more helpful?
            raise Exception('API request failed. Data returned: ' + request.text)

    def post(self, endpoint: str, data: dict = {}):
        """
        Make a POST request to the API.

        :param params: dictionary of custom data to add to request.
        """
        request = self.session.post(self.API_ROOT + endpoint, json=data)
        if request.ok:
            return request.json()
        else:
            # TODO: Can we be more helpful?
            raise Exception('API request failed. Data returned: ' + request.text)

    def search(self, name: str):
        # TODO: use actual urlencode?
        result = self.get('suggest', {'q': name.replace(' ', '%2C')})['Records']
        num_results = int(result['@TotalRecords'])
        if num_results == 0:
            return []
        record = result['Record']
        if num_results == 1:
            record = [record]
        print(record)
        return [Person(raw) for raw in record]

    # TODO: unacceptable name
    def request(self, name: str):
        return self.post('api', {'peoplesearch': [{'netid': '', 'queryType': 'term', 'query': [{'pattern': 'Erik'}]}]})
