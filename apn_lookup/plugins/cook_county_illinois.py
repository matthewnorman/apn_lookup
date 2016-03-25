"""
Chicago! Chicago!

"""
import lxml.html
import requests

from apn_lookup.plugins import base_plugin

URL = 'http://www.cookcountypropertyinfo.com/Pages/Pin-Results.aspx'


class CookCountyIllinoisPlugin(base_plugin.PluginBase):
    """
    Go take a look at the heart of Chicago.

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
        For Chicago, the ID is handled as a single,
        fourteen digit number, with no dashes or other
        interruptions.
        """

        req = requests.get(URL, params={'pin': ID})
        html = lxml.html.fromstring(req.text)
        tax_value = html.xpath('//span[@id="ctl00_PlaceHolderMain_ctl00'
                               '_taxCalculator_lblEstimatedTaxValue"]'
                               '/text()')
        tax_value = float(tax_value[0].replace(',', ''))
        return {'property_tax': tax_value}

def factory():
    return CookCountyIllinoisPlugin()
