__author__ = 'sms'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re
import codecs
import json
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB.

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to
update the street names before you save them to JSON.

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings.
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd": "Road",
            "Rd.": "Road",
            "Ave.": "Avenue",
            "Blvd": "Boulevard",
            "Blvd,": "Boulevard",
            "Blvd.": "Boulevard",
            "Ct": "Court",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Ln.": "Lane",
            "Pl": "Place"
            }

OSMFILE = "san-francisco_california.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    # iteratively parse the mapping xml
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        # node and way tags are of special interest
        if elem.tag == "node" or elem.tag == "way":
            # iterate the "tag" tags within a node or way
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if mapping.has_key(street_type):
            name = name.replace(street_type, mapping[street_type])
    return name

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def shape_element(element):
    node = {}
    created = {}
    if element.tag == "node" or element.tag == "way" :
        for attribval in CREATED:
            if element.attrib.has_key(attribval):
                created[attribval] = element.attrib[attribval]

        if element.attrib.has_key('id'):
            node['id'] = element.attrib['id']
        node['type'] = element.tag

        if element.attrib.has_key('visible'):
            node['visible'] = element.attrib['visible']

        if len(created)>0:
            node['created'] = created

        pos = []
        if element.attrib.has_key('lat'):
            pos.append(float(element.attrib['lat']))

        if element.attrib.has_key('lon'):
            pos.append(float(element.attrib['lon']))

        if len(pos) > 0:
            node['pos'] = pos

        nd_refs = []
        for tag in element.iter("nd"):
            nd_refs.append (tag.attrib['ref'])

        if element.tag == "way":
            if len(nd_refs) > 0:
                node["node_refs"] = nd_refs
        addr = {}
        for tag in element.iter("tag"):
            if tag.attrib.has_key('k'):
                if not problemchars.search(tag.attrib['k']):
                    if is_street_name(tag):
                        attrib_mod = tag.attrib['k'].replace('addr:','')
                        if not lower_colon.match(attrib_mod):
                           addr[attrib_mod] = update_name(tag.attrib['v'], mapping)
                    elif tag.attrib['k'].startswith('addr:'):
                       attrib_mod = tag.attrib['k'].replace('addr:','')
                       if not lower_colon.match(attrib_mod):
                           addr[attrib_mod] = tag.attrib['v']
                    else:
                        node[tag.attrib['k']] = tag.attrib['v']

        if len(addr) > 0:
            node['address'] = addr



        #print node

        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_map(OSMFILE, True)
    pprint.pprint(data)

    # correct_first_elem = {
    #     "id": "261114295",
    #     "visible": "true",
    #     "type": "node",
    #     "pos": [41.9730791, -87.6866303],
    #     "created": {
    #         "changeset": "11129782",
    #         "user": "bbmiller",
    #         "version": "7",
    #         "uid": "451048",
    #         "timestamp": "2012-03-28T18:31:23Z"
    #     }
    # }

    # assert data[0] == correct_first_elem
    # assert data[-1]["address"] == {
    #                                 "street": "West Lexington St.",
    #                                 "housenumber": "1412"
    #                                   }
    # assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369",
    #                                 "2199822370", "2199822284", "2199822281"]

if __name__ == "__main__":
    test()