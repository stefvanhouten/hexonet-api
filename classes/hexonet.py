
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

  def __call__(self, obj, 
               *args, **kwargs
               ):
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
    def build_params(cls, name, 
                     customer, params
                     ):
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
    def activate_domain_registration(cls, domain):
      """ 
      The ActivateDomainRegistration command is used to submit a domain registration request to the registry. 
      This step is only required, if the registrar needs to interact before the registration request is being submitted 
      to the regisitry ( e.g. for .NO domains a registration form is required upfront). 
      """
      params = cls.PARAMS.copy()
      params['command'] = 'ActivateDomainRegistration'
      params['domain'] = domain
      return requests.get(cls.API, params=params)
    
    @classmethod
    @convert_response_to_dict
    def activate_domain_trade(cls, domain):
      """ 
      The ActivateDomainTrade command is used to approve a domain trade, 
      which requires an activation through the registrar (e.g. for .AT domains upon receipt of required documentation). 
      """
      params = cls.PARAMS.copy()
      params['command'] = 'ActivateDomainTrade'
      params['domain'] = domain
      return requests.get(cls.API, params=params)
    
    @classmethod
    @convert_response_to_dict
    def activate_domain_transfer(cls, domain, action, 
                                 repository=None, trigger=None
                                 ):
      """
      action:
      - REQUEST
      - APPROVE
      - REJECT
      - DENY
       
      The ActivateDomainTransfer command is used to approve or reject a domain transfer which requires the active 
      participation of the registrar or repository owner (e.g. all gTLDs).
      
      As soon as a gLTD transfer is initiated, our system sends a FOA email to the registrant by default, 
      which contains a confirmation link. This link leads to a whitelabeled site where the transfer can be activated.
      If a reseller or a customer with its own domain repository does not want to use this FOA email function, 
      he needs to use ActivateDomainTransfer to confirm the transfer. The command can only be executed by registrars 
      or RegistrarOC customers. If you are no repository owner, you have to submit the respective repository and trigger code.
      """
      params = cls.PARAMS.copy()
      params['command'] = 'ActivateDomainTransfer'
      params['domain'] = domain
      
      if repository is not None:
        params['repository'] = repository
        
      if trigger is not None:
        params['trigger'] = trigger
        
      return requests.get(cls.API, params=params)
    
    @classmethod
    @convert_response_to_dict
    def add_domain(cls, domain, period, 
                   owner_contact, admin_contact, tech_contact, 
                   billing_contact, nameservers=None
                   ):
      """ 
      Used to register new domain names.
      period should be an integer 
      Use the customer object to add contacts to the request. 
      Nameservers should be a list of nameservers you want to add.
      """
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
    def add_domain_av_record(cls, domain, trigger=None, 
                             host=None, checktype=None
                             ):
      """ 
      The AddDomainAvRecord command is used to create a Authentication and Verification (A/V) Data record. 
      A/V records are only required for the .PRO registry at this point in time. 
      """
      params = cls.PARAMS.copy()
      params['command'] = 'AddDomainAvRecord'
      params['domain'] = domain
      
      if trigger is not None:
        params['trigger'] = trigger
        
      if host is not None:
        params['host'] = host
        
      if checktype is not None:
        params['checktype'] = checktype
      
      return request.get(cls.API, params=params)
    
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
    def check_domain_transfer(cls, domain, auth=None):
      """ 
      The CheckDomainTransfer command allows you to review the details which are necessary to perform a 
      successful transfer of a gTLD CNOBIN (i.e. eMail addresses, current registrar, domain status, ...).

      It is also possible to validate an AUTH code for the following gTLDs: 
      .aero, .asia, .biz, .ca, .cat, .com, .info, .mobi, .name, .net, .org, .tel. 
      The result of the validation is shown in the property AUTHISVALID.
      """
      params = cls.PARAMS.copy()
      params['command'] = 'CheckDomainTransfer'
      if auth is not None:
        params['auth'] = auth
        
      return requests.get(cls.API, params=params)
    
    @classmethod 
    @convert_response_to_dict
    def check_domain_av_record(cls, avid, repository):
      """ 
      The CheckDomainAvRecord command can be used used to check the availability of a 
      authentication and verification (A/V) data record. 
      A/V records are only required for the .PRO registry at this point in time.
      """
      params = cls.PARAMS.copy()
      params['command'] = 'CheckDomainAvRecord'
        
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
    @convert_response_to_dict
    def modify_domain(cls, domain):
      """ TODO find out what are the most important commands for modifying and workout this function """
      params = cls.PARAMS.copy()
      params['command'] = 'ModifyDomain'
      params['domain'] = domain
      return requests.get(cls.API, params=params)
    
    @classmethod
    @convert_response_to_dict
    def pay_domain_renewal(cls, domain, period=None):
      """
      The PayDomainRenewal command is used to pay the renewal of a single domain. 
      It sets the PAIDUNTILDATE of a domain according to the given renewal period.
      If a domain has been paid (as given by PAIDUNTILDATE) it will be renewed automatically when registry's EXPIREDATE is reached.
      """
      params = cls.PARAMS.copy()
      params['command'] = 'PayDomainRenewal'
      params['domain'] = domain
      if period is not None:
        params['period'] = period
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
    def transfer_domain(cls, domain, auth=None, 
                        action=None, transferlock=None
                        ):
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
      
      if auth is not None:
        params['auth'] = auth
      if action is not None:
        params['action'] = action
      if transferlock is not None:
        params['transferlock'] = transferlock
        
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
    
    @classmethod
    @convert_response_to_dict
    def unlock_domain_for_transfer(cls, domain, shouldLock):
      """ Takes integer 0 to unlock 1 to lock """
      params = cls.PARAMS.copy()
      params['domain'] = domain
      params['command'] = 'ModifyDomain'
      params['transferlock'] = shouldLock
      return requests.get(cls.API, params=params)