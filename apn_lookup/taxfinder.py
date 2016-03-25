"""
This is the core library which calls all the other
libraries.
"""

import importlib
import collections


class InvalidRegionError(ValueError):
    """
    Dummy class - raise this if someone asks
    for a region that doesn't exist in the config.
    """

class TaxfinderCore():
    """
    Core class. Should take requests with state, county, and
    APN/AIN/property identification number, and return
    a dictionary with all the possible data.
    """

    def __init__(self):
        """
        Init the caching objects.
        """

        self._plugin_cache = collections.defaultdict(dict)
        self._plugin_config = self._load_config()

    def _load_config(self):
        """
        Until I write a real config, put things here.
        """
        return {
            'california': {
                'santa clara': 'santa_clara_california'
            }
        }

    def _sanitize_names(self, tax_region, over_region):
        """
        Sanitize the names so that they are formatted
        in a consistent way.
        """
        big_region = over_region.strip().lower()
        small_region = tax_region.replace('county', '').strip().lower()
        return small_region, big_region

    def get_property_info(self, ID, tax_region, over_region):
        """
        So in theory property lookup requires three values.

        :param: ID - the ID used to identify property parcels for
                     tax purposes.
        :param: tax_region - The region in which taxes are assigned.
                     This is county/parish in the US.
        :param: over_region - Next step up in the geographic
                     organization of the country. The largest geographic
                     division in which the tax_region is unique.
        """

        # Do we have to load the plugin?
        tax_region, over_region = self._sanitize_names(tax_region,
                                                       over_region)
        plugin = self._plugin_cache[over_region].get(tax_region)

        if plugin is None:
            # We failed to find it in the cache.
            # Time to load.
            try:
                plugin_name = self._plugin_config[over_region][tax_region]
            except KeyError:
                msg = 'Could not find region {}:{}'.format(tax_region,
                                                           over_region)
                raise InvalidRegionError(msg)

            plugin_path = '.plugins.{}'.format(plugin_name)
            imported = importlib.import_module(name=plugin_path,
                                               package='apn_lookup')
            plugin = imported.factory()
            plugin.setup()
            self._plugin_cache[over_region][tax_region] = plugin

        # By now we should have the plugin
        plugin.open()
        data = plugin.lookup(ID=ID)
        plugin.close()

        return data

        
