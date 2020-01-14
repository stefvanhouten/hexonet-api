
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
        line = text[start:i].split("=", 1)
        if len(line) >= 2 and line[1] != "":
          key, value = line
          if key in response_dict.keys():
            key += "_1"
          response_dict[key] = value
        start = i + 1

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
    LOGIN = "stefvanhouten1"
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
    def modify_domain(cls, domain, options):
      """ 
      TODO: find out what are the most important commands for modifying and workout this function
      All options keywords: 
      options = {
        'addnameserver0': 'value',
        'delnameserver0': 'value',
        'nameserver0': 'value',
        'addownercontact0': 'value',
        'delownercontact0': 'value',
        'ownercontact0': 'value',
        'addadmincontact0': 'value',
        'deladmincontact0': 'value',
        'admincontact0': 'value',
        'addtechcontact0': 'value',
        'deltechcontact0': 'value',
        'techcontact0': 'value',
        'addbillingcontact0': 'value',
        'delbillingcontact0': 'value',
        'billingcontact0': 'value',
        'addstatus0': 'value',
        'delstatus0': 'value',
        'status0': 'value',
      } 
      """
      params = cls.PARAMS.copy()
      params['command'] = 'ModifyDomain'
      params['domain'] = domain
      
      for value in options:
        params[value] = options[value]
      
      return requests.get(cls.API, params=params)
    
    @classmethod
    @convert_response_to_dict
    def pay_domain_renewal(cls, domain, period=None):
      """
      period as an integer
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
    def push_domain(cls, domain, target):
      """
      The PushDomain command is used to send .DE / .AT domains to transit / billwithdraw status 
      and change the tag or delete a .UK domain.
      """
      params = cls.PARAMS.copy()
      params['command'] = 'PushDomain'
      params['domain'] = domain
      params['target'] = target
      
      return requests.get(cls.API, params=params)

    @classmethod
    @convert_response_to_dict
    def renew_domain(cls, domain, period=None, expiration=None):
      """
      The PushDomain command is used to send .DE / .AT domains to transit / billwithdraw status 
      and change the tag or delete a .UK domain.
      """
      params = cls.PARAMS.copy()
      params['command'] = 'RenewDomain'
      params['domain'] = domain
      
      if period is not None:
        params['period'] = period
        
      if expiration is not None:
        params['expiration'] = expiration
      
      return requests.get(cls.API, params=params)
    
    @classmethod
    @convert_response_to_dict
    def restore_domain(cls, domain):
      """
      The RestoreDomain command automatically request a restore at the respective registry.
      The processing depends on the respective TLD/ccTLD / registry and varies from realtime up to 3 working days.
      """
      params = cls.PARAMS.copy()
      params['command'] = 'RestoreDomain'
      params['domain'] = domain
   
      return requests.get(cls.API, params=params)

    @classmethod
    @convert_response_to_dict
    def renew_domain(cls, domain, renewalmode, period):
      """
      renewalmode = AUTORENEW | AUTOEXPIRE | AUTODELETE
      period = 1Y | 1M

      SetDomainRenewalMode allows you to set the renewalmode on a per domain basis; the following modes are permitted:
      - AUTORENEW: the system pays the domain renewal internally if the domain has renewalmode 
                   AUTORENEW. Hence the PREPAIDPERIOD is increased.
      - AUTODELETE: the system will send a deletion command for the domain name on failure date
      - AUTOEXPIRE: the system let the domain expire on the so-called failure date, 
                    often this is equal to a deletion, but for some TLDs like .DE, another procedure apply (.de: "TRANSIT"; .at: "BILLWITHDRAW")

      With the optional parameter PERIOD you are able to set a .DE domain name to monthly renewal or back to yearly.
      """
      params = cls.PARAMS.copy()
      params['command'] = 'SetDomainRenewalMode'
      params['domain'] = domain
      params['renewalmode'] = renewalmode
      params['period'] = period
   
      return requests.get(cls.API, params=params)

    @classmethod
    @convert_response_to_dict
    def status_domain(cls, domain):
      """
      The StatusDomain command enables you to check the current status of a domain name. 
      It gives information about the created date, expiration, renewal mode, transfer-lock, etc. 
      """
      params = cls.PARAMS.copy()
      params['command'] = 'StatusDomain'
      params['domain'] = domain
      
      return requests.get(cls.API, params=params)
    
    @classmethod
    def get_domain_auth_key(cls, domain):
      """ Returns auth key used to transfer specific domain """
      result = cls.status_domain(domain)
      
      if 'PROPERTY[AUTH][0]' in result:
        return { "key": result['PROPERTY[AUTH][0]'] }
      else:
        return None
    
    @classmethod
    @convert_response_to_dict
    def status_domain_av_record(cls, domain):
      """
      The StatusDomainAvRecord command is used to check the current status of a Authentication and Verification (A/V) Data record.
      A/V records are only required for the .PRO registry at the moment. 
      """
      params = cls.PARAMS.copy()
      params['command'] = 'StatusDomainAvRecord'
      params['domain'] = domain
      
      return requests.get(cls.API, params=params)
    
    
    @classmethod
    @convert_response_to_dict
    def status_domain_transfer(cls, domain):
      """
      The StatusDomainTransfer command informs you about the current status of a transfer. 
      You can check if the transfer was successfully initiated or who received the eMail to confirm a transfer. 
      This command works currently only with COM / NET / ORG / INFO & BIZ domains.
      """
      params = cls.PARAMS.copy()
      params['command'] = 'StatusDomainTransfer'
      params['domain'] = domain
      
      return requests.get(cls.API, params=params)
    
    @classmethod
    @convert_response_to_dict
    def trade_domain(cls, domain, contact, action):
      """
      TODO Check if the ownercontact requires the Customer object
      action = request | cancel 
      It is not possible to change the owner name or company name of a: 
      .AT, .BE, .CH, .EU, .ES, .FR, .IT, .JP, .LI, .LU, .NL, .NU, .SE or .SG domain through the ModifyDomain command. 
      In such a case you have to request a so-called "trade" and state the new owner contact. 
      Please have a look at the  Domain API-Manual for a current list of allowed parameters.
      """
      params = cls.PARAMS.copy()
      params['command'] = 'TradeDomain'
      params['domain'] = domain
      
      return requests.get(cls.API, params=params)
    
    @classmethod
    @convert_response_to_dict
    def transfer_domain(cls, domain, auth=None, 
                        action=None, transferlock=None
                        ):
      """ 
      Transfer a domain. Action commands are one of the following:
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
    def query_domain_list(cls, admincontact=None, billingcontact=None,
                          domain=None, first=None, limit=None,
                          maxcreatedate=None, maxregistrationexpirationdate=None, maxupdateddate=None,
                          mincreateddate=None, minregistrationexpirationdate=None, minupdateddate=None,
                          nameserver=None, orderby=None, ownercontact=None,
                          status=None, techcontact=None, transferlock=None,
                          userdepth=None, x_trustee=None, zone=None
                          ):
      """ 
      The command QueryDomainList will return you a list of domain names managed by your HEXONET account. 
      With it's different parameters it enables you to filter the list of results depending on your needs
      
      admincontact = (CONTACT)
      billingcontact = (CONTACT)
      domain = (DOMAIN)
      first = (INT)
      limit = (INT)
      maxcreateddate = (DATE)
      maxregistrationexpirationdate = (DATE)
      maxupdateddate = (DATE)
      mincreateddate = (DATE)
      minregistrationexpirationdate = (DATE)
      minupdateddate = (DATE)
      nameserver = (NAMESERVER)
      nameserver# = (NAMESERVER)
      orderby = DOMAIN | DOMAINDESC | USER | USERDESC | CREATEDDATE | CREATEDDATEDESC | UPDATEDDATE | UPDATEDDATEDESC | 
      REGISTRATIONEXPIRATIONDATE | REGISTRATIONEXPIRATIONDATEDESC | REGISTRAR | REGISTRARDESC
      ownercontact = (CONTACT)
      status = (STATUS)
      techcontact = (CONTACT)
      transferlock = 0 | 1
      userdepth = SELF | SUBUSER | ALL
      x-trustee = 0 | 1
      zone = (ZONE)
      """
      params = cls.PARAMS.copy()
      params['command'] = 'QueryDomainList'
      params['admincontact'] = admincontact
      params['billingcontact'] = billingcontact
      params['domain'] = domain
      params['first'] = first
      params['maxcreatedate'] = maxcreatedate
      params['maxregistrationexpirationdate'] = maxregistrationexpirationdate
      params['maxupdateddate'] = maxupdateddate
      params['mincreateddate'] = mincreateddate
      params['minregistrationexpirationdate'] = minregistrationexpirationdate
      params['minupdateddate'] = minupdateddate
      params['nameserver'] = nameserver
      params['orderby'] = orderby
      params['ownercontact'] = ownercontact
      params['status'] = status
      params['techcontact'] = techcontact
      params['transferlock'] = transferlock
      params['userdepth'] = userdepth
      params['x-trustee'] = x_trustee
      params['zone'] = zone

      return requests.get(cls.API, params=params)
    
    @classmethod
    @convert_response_to_dict
    def query_domain_repository_info(cls, domain, repository, zone):
      """ The QueryDomainRepositoryInfo command is used to list all available information for a certain domain repository. """
      params = cls.PARAMS.copy()
      params['command'] = 'QueryDomainRepositoryInfo'
      params['domain'] = domain
      params['repository'] = repository
      params['zone'] = zone
      
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
      """ Returns dict with incoming domain transfers and their current status. """
      params = cls.PARAMS.copy()
      params['command'] = 'QueryForeignTransferList'
      
      return requests.get(cls.API, params=params)
    
    @classmethod
    @convert_response_to_dict
    def unlock_domain_for_transfer(cls, domain, shouldLock):
      """ Takes integer 0 to unlock and 1 to lock. """
      params = cls.PARAMS.copy()
      params['domain'] = domain
      params['command'] = 'ModifyDomain'
      params['transferlock'] = shouldLock
      
      return requests.get(cls.API, params=params)