from service_adapters.dadata_adapter import AddressData


def get_address_data() -> AddressData:
    return AddressData(address="Address",
                       lat=1.1,
                       lon=0.0,
                       qc_geo=1)


def get_imprecise_addr_data():
    return AddressData(address="None",
                       lat=0.,
                       lon=0.,
                       qc_geo=2)


def get_atm_groups():
    return ['gr1', 'gr2']
