from internal.pb.niffler_currency_pb2 import CurrencyValues
from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from google.protobuf import empty_pb2

CURENCY_RATES = {
    CurrencyValues.EUR: 1.08,
    CurrencyValues.RUB: 0.015,
    CurrencyValues.USD: 1.0,
    CurrencyValues.KZT: 0.0021
}

def test_get_all_currencies(grpc_client: NifflerCurrencyServiceClient):
    response = grpc_client.get_all_currencies(empty_pb2.Empty())
    assert len(response.allCurrencies) == 4
    for currency_dict in response.allCurrencies:
        assert currency_dict.currency in [
            CurrencyValues.EUR, CurrencyValues.RUB, 
            CurrencyValues.USD, CurrencyValues.KZT
        ]
        assert currency_dict.currencyRate == CURENCY_RATES[currency_dict.currency]