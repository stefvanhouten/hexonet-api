from classes.hexonet import Hexonet, Customer
import pprint

pp = pprint.PrettyPrinter(indent=4)
customer = Customer('stef', 'van Houten', 'emmakade', 'leeuwarden', 'friesland', '8922', 'NL', '0640811668', 'stefvanhouten@gmail.com')

hexonet = Hexonet()
pp.pprint(hexonet.check_domain('test.org'))
pp.pprint(hexonet.check_domains(['test.org', 'test1.org', 'test2.org', 'test3.org']))
pp.pprint(hexonet.status_domain('test.org'))
pp.pprint(hexonet.add_domain('stef5.org', 1, customer, customer, customer, customer, ['nameserver1.com']))