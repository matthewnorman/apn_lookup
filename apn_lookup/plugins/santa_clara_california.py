"""
The first plugin I'm writing, and sort of the
easiest.

This is for Santa Clara County, Home of San Jose,
Silicon Valley (the Enterprise half of it at least),
and Code for San Jose.
"""
import lxml.html
import requests

from apn_lookup.plugins import base_plugin


URL = "https://payments.sccgov.org/propertytax/Secured/Parcel?"

class SantaClaraPlugin(base_plugin.PluginBase):
    """
    Class for holding any active communications
    and handling the calls.

    Fortunately, Santa Clara is somewhat easy,
    and so has no need for most of the mechanics.
    """

    def setup(self):
        """
        Do nothing.
        """
        pass

    def teardown(self):
        """
        Do nothing.
        """
        pass

    def open(self):
        """
        Do nothing.
        """
        pass

    def close(self):
        """
        Do nothing.
        """
        pass

    def lookup(self, ID):
        """
        For Santa Clara, the ID is handled as a single,
        eight digit number, with no dashes or other
        interruptions.
        """

        req = requests.get(URL, params={'parcelnumber': ID})
        html = lxml.html.fromstring(req.text)
        col_values_raw = html.xpath('//div[@class="col-sm-2 col-md-2"]/text()')
        col_values = [x.strip().replace('$', '').replace(',', '')
                      for x in col_values_raw if '$' in x]
        first_value = float(col_values[0])
        second_value = float(col_values[1])
        total_tax = first_value + second_value
        other_tax = sum([float(x) for x in col_values[2:]])
        return {'property_tax': total_tax,
                'other_tax': other_tax}



def factory():
    return SantaClaraPlugin()
