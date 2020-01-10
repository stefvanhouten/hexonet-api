
import requests

class Customer(object):
    def __init__(self, companyName,
                 firstName, lastName):
        self.COMPANY_NAME = companyName
        self.FIRST_NAME = firstName
        self.LAST_NAME = lastName


class Hexonet(object):
    LOGIN = "stefvanhouten"
    PW = "e@K!LfR7kcPa6a9"

    API = "https://api.ispapi.net/api/call.cgi"
    PARAMS = {
      's_entity': 1234,
      's_login': LOGIN,
      's_pw': PW,
    }

    @classmethod
    def add_domain(cls):
      """ """

    @classmethod
    def delete_domain(cls):
      """ """

    @classmethod
    def status_domain(cls):
      """ """

    @classmethod
    def convert_response_to_dict(cls, response):
      response_dict = {}
      start = 0
      text = response.text

      for i, char in enumerate(text):
        if char == "\n":
          line = text[start:i].split("=")
          if len(line) >= 2 and line[1] != "":
            key, value = line
            if key in response_dict.keys():
              key += "_1"
            response_dict[key] = value
          start = i + 1

      response_dict['status'] = response.status_code
      return response_dict

    @classmethod
    def check_domain(cls, domain):
      """ Checks availability of domain name"""
      # Create a copy of the original to prevent mutating it
      params = cls.PARAMS.copy()
      # Prepare query parameters
      params['command'] = "CheckDomain"
      params['domain'] = domain
      # Send request and convert request to dictionary
      response = requests.get(cls.API, params=params)
      response = cls.convert_response_to_dict(response)

      return response