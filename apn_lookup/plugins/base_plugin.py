

class PluginBase:
    """
    Fairly simple base class for plugins.
    """

    def setup(self):
        """
        This method should be called only at initialization.
        """
        raise NotImplementedError('setup() must be implemented!')

    def open(self):
        """
        This method should be called before each query.
        """
        raise NotImplementedError('open() must be implemented!')

    def close(self):
        """
        This method should be called after each query.
        """
        raise NotImplementedError('close() must be implemented!')

    def teardown(self):
        """
        This should be called only in case of a shutdown.
        """
        raise NotImplementedError('teardown() must be implemented!')

    def lookup(self, ID):
        """
        Take an ID and turn it into a blob of property information.
        This is the heart of the code.
        """
        raise NotImplementedError('lookup() must be implemented')
