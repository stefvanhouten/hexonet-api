
import pprint

import requests


class Sidn(object):
  API = 'https://api.sidn.nl/rest/is?'
  api_token = { "api_token": "eyJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoiQVBJIiwiaWF0IjoxNTc4OTI3MTk5LCJleHAiOjE1Nzg5Mjg5OTl9.l8Z1GyGZ5UkCH_i6FpOLr3XUpPTGYBK3WB-3K2H-y8gDwnIWvBbhFGxuL8bkrDFodcZUxJyCDzIbXsBwckSp9Q"}
  
  @classmethod
  def get_api_key(cls):
    session = requests.Session()
    response = session.get("https://api.sidn.nl/rest/is?domain=test")
    return session.cookies.get_dict()['api_token']
    
  @classmethod
  def check_domain(cls, domain):
    response = requests.get(cls.API, params={'domain': domain}, cookies=cls.api_token)
    return response.json()
  
  @classmethod
  def test(cls):
    xml = """ 
          <?xml version="1.0" encoding="UTF-8" standalone="no"?>
          <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
            <hello />
          </epp>
          """
    print(requests.post("drs.domain-registry.nl:700", data=xml))
