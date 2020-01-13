
import requests
from functools import update_wrapper, partial
import pprint

pp = pprint.PrettyPrinter(indent=4)

class MyDecorator(object):
  def __init__(self, func):
    update_wrapper(self, func)
    self.func = func

  def __get__(self, obj, objtype):
    """Support instance methods."""
    return functools.partial(self.__call__, obj)

  def __call__(self, obj, *args, **kwargs):
    response = self.func(obj, *args, **kwargs)
    text = response.text
    response_dict = {}
    start = 0
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

convert_response_to_dict = MyDecorator
   

class Customer(object):
    def __init__(self, firstName, lastName, 
                 street, city, state, 
                 zipcode, country, phone, 
                 email, fax=None, organization=None, 
                 middlename=None, title=None):
      
        self.firstname = firstName
        self.middlename = middlename
        self.lastname = lastName
        self.organization = organization
        self.street = street,
        self.city = city
        self.state = state,
        self.zip = zipcode
        self.country = country
        self.phone = phone
        self.email = email
        self.fax = fax
        self.title = title

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
    def build_params(cls, name, customer, params):
      if type(customer) == Customer:
        for key in customer.__dict__.keys():
          params['{}0{}'.format(name, key)] = customer.__dict__[key]
      else:
        #If its not a customer object its a list of nameservers
        for i, nameserver in enumerate(customer):
          params['{}{}'.format(name, i)] = nameserver
      return params
    
    @classmethod
    @convert_response_to_dict
    def add_domain(cls, domain, period, 
                   owner_contact, admin_contact, tech_contact, 
                   billing_contact, nameservers=None):
      """ Used to register new domain names """
      params = cls.PARAMS.copy()
      params['command'] = 'AddDomain'
      params['domain'] = domain
      params = cls.build_params('ownercontact', owner_contact, params)
      params = cls.build_params('admincontact', admin_contact, params)
      params = cls.build_params('techcontact', tech_contact, params)
      params = cls.build_params('billingcontact', billing_contact, params)
      
      if nameservers is not None:
        params = cls.build_params('nameserver', nameservers, params)
        
      return requests.get(cls.API, params=params)
    
    @classmethod
    @convert_response_to_dict
    def delete_domain(cls, domain):
      """ Deletes domain based on url """
      params = cls.PARAMS.copy()
      params['command'] = 'DeleteDomain'
      params['domain'] = domain
      return requests.get(cls.API, params=params)
    
    @classmethod
    def status_domain(cls):
      """ """

    @classmethod
    @convert_response_to_dict
    def check_domain(cls, domain):
      """ Checks availability of domain name. Takes single string as argument """
      # Create a copy of the original to prevent mutating it
      params = cls.PARAMS.copy()
      # Prepare query parameters
      params['command'] = 'CheckDomain'
      params['domain'] = domain
      # Send request and convert request to dictionary

      return requests.get(cls.API, params=params)
    
    @classmethod 
    @convert_response_to_dict
    def check_domains(cls, domains):
      """ Check availability of domain names. Takes list of strings as argument """
      # Create a copy of the original to prevent mutating it
      params = cls.PARAMS.copy()
      params['command'] = 'checkDomains'
      
      #Loop over given domains and add it to the params dict
      for i, domain in enumerate(domains):
        params['domain{}'.format(i)] = domain
        
      return requests.get(cls.API, params=params)

    @classmethod
    @convert_response_to_dict
    def status_domain(cls, domain):
      """ """
      params = cls.PARAMS.copy()
      params['command'] = 'StatusDomain'
      params['domain'] = domain
      return requests.get(cls.API, params=params)
    
    
    @classmethod
    @convert_response_to_dict
    def transfer_domain(cls, domain, auth, action):
      """ Transfer a domain. Action commands are one of the following:
          - REQUEST; request transfer
          - APPROVE; approve outgoing transfer
          - DENY; deny outgoing transfer
          - CANCEL; cancel incoming transfer request
          - USERTRANSFER; request local transfer within hexonet
      """
      params = cls.PARAMS.copy()
      params['command'] = 'TransferDomain'
      params['domain'] = domain
      params['auth'] = auth
      params['action'] = action
      return requests.get(cls.API, params=params)
    
    
    @classmethod
    @convert_response_to_dict
    def list_transfers_incoming(cls):
      """ Returns list of incoming domain transfers and their current status """
      params = cls.PARAMS.copy()
      params['command'] = 'QueryTransferList'
      return requests.get(cls.API, params=params)
    
    @classmethod
    @convert_response_to_dict
    def list_transfers_outgoing(cls):
      """ Returns dict with incoming domain transfers and their current status """
      params = cls.PARAMS.copy()
      params['command'] = 'QueryForeignTransferList'
      return requests.get(cls.API, params=params)
    
    @classmethod
    @convert_response_to_dict
    def list_owned_servers(cls):
      """ Returns dict with list of owned servers """
      params = cls.PARAMS.copy()
      params['command'] = 'QueryDomainList'
      return requests.get(cls.API, params=params)
    