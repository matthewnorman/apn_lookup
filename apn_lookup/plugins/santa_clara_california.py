"""
The first plugin I'm writing, and sort of the
easiest.

This is for Santa Clara County, Home of San Jose,
Silicon Valley (the Enterprise half of it at least),
and Code for San Jose.
"""
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

    def lookup(self, ID):
        """
        For Santa Clara, the ID is handled as a single,
        eight digit number, with no dashes or other
        interruptions.
        """

        req = requests.get(URL, params={'parcelnumber': ID})



def factory():
    return SantaClaraPlugin()
