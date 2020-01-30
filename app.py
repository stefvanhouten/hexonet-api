import pprint

from classes.hexonet import Customer, Hexonet
from classes.sidn import Sidn

pp = pprint.PrettyPrinter(indent=4)
customer = Customer('stef', 'van Houten', 'emmakade', 'leeuwarden', 'friesland', '8922', 'NL', '0612311154', 'stefvanhouten@gmail.com')

domain = 'stef1.co'
auth = Hexonet.get_domain_auth_key(domain)['key']

print(Hexonet.get_tld_eu().get('.re'))

  
# pp.pprint(d)
# pp.pprint(Hexonet.check_domain(domain))
# pp.pprint(Hexonet.check_domains(['domain1.com', 'domain2.com', 'domain3.com', 'domain4.com']))
# pp.pprint(Hexonet.modify_domain(domain, {'delstatus1': 'value'}))

# pp.pprint(Hexonet.add_domain('stef5.org', 1, customer, customer, customer, customer, ['nameserver1.com']))
# pp.pprint(Hexonet.delete_domain('stef4.org'))


#TRANSFERS
# pp.pprint(Hexonet.transfer_domain(domain, auth=auth, action='usertransfer'))
# pp.pprint(Hexonet.transfer_domain(domain, action='approve'))

# pp.pprint(Hexonet.list_transfers_incoming())
# pp.pprint(Hexonet.list_transfers_outgoing())

# pp.pprint(Hexonet.query_domain_list())
# pp.pprint(Hexonet.unlock_domain_for_transfer('stef1.co', 0))
# pp.pprint(Hexonet.get_domain_auth_key(domain))


# Sidn.get_api_key()
# pp.pprint(Sidn.check_domain("quadratandtest"))
