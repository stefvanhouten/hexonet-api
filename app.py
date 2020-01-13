from classes.hexonet import Hexonet, Customer
import pprint

pp = pprint.PrettyPrinter(indent=4)
customer = Customer('stef', 'van Houten', 'emmakade', 'leeuwarden', 'friesland', '8922', 'NL', '0612311154', 'stefvanhouten@gmail.com')

hexonet = Hexonet()
domain = 'stef1.co'
auth = 'Wb29L-dfGi4b'

# pp.pprint(hexonet.check_domain(domain))
# pp.pprint(hexonet.check_domains(['domain1.com', 'domain2.com', 'domain3.com', 'domain4.com']))
# pp.pprint(hexonet.status_domain(domain))
# pp.pprint(hexonet.add_domain('stef5.org', 1, customer, customer, customer, customer, ['nameserver1.com']))
# pp.pprint(hexonet.delete_domain('stef4.org'))


# pp.pprint(hexonet.transfer_domain(domain, auth=auth, action='usertransfer'))
# pp.pprint(hexonet.transfer_domain(domain, action='approve'))

pp.pprint(hexonet.list_transfers_incoming())
pp.pprint(hexonet.list_transfers_outgoing())
# pp.pprint(hexonet.list_owned_servers())
# pp.pprint(hexonet.unlock_domain_for_transfer('stef1.co', 0))