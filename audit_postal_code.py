__author__ = 'sms'
"""
- Audit postal codes
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "san-francisco_california.osm"
postal_type_re = re.compile(r'.*(\d{5}(\-\d{4})?)$')



def audit_postal_code(bad_postal_codes, postal_code):
    m = postal_type_re.search(postal_code)
    if m:
        postal_code_type = m.group()
    else:
        bad_postal_codes.append(postal_code)
        print postal_code

def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    bad_postal_codes = []
    # iteratively parse the mapping xml
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        # node and way tags are of special interest
        if elem.tag == "node" or elem.tag == "way":
            # iterate the "tag" tags within a node or way
            for tag in elem.iter("tag"):
                if is_postal_code(tag):
                    audit_postal_code(bad_postal_codes, tag.attrib['v'])

    return bad_postal_codes



def test():
    bad_postal_codes = audit(OSMFILE)
    #assert len(st_types) == 3
    pprint.pprint(bad_postal_codes)

if __name__ == '__main__':
    test()