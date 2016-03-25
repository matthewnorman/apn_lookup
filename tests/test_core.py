import pytest

from apn_lookup import taxfinder


@pytest.mark.integration
def test_integration_santa_clara():
    """
    DO NOT RUN THIS AUTOMATICALLY

    It's an integration test. You have been warned.
    """

    core = taxfinder.TaxfinderCore()
    core.get_property_info(ID=28423048, over_region='california',
                           tax_region='santa clara county')
                           
