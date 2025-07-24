import pytest
import grpc
from grpc import insecure_channel
from internal.grpc.interceptors.logging import LoggingInterceptor
from internal.grpc.interceptors.allure import AllureInterceptor
from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from settings.settings import Settings

INTERCEPTORS = [
    LoggingInterceptor(),
    AllureInterceptor()
]

@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()

def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--mock", action="store_true", default=False)

@pytest.fixture(scope="session")
def mock(request: pytest.FixtureRequest) -> bool:
    return request.config.getoption("--mock")

@pytest.fixture(scope="session")
def grpc_client(settings: Settings, mock: bool) -> NifflerCurrencyServiceClient:
    host = settings.currency_service_host
    if mock:
        host = settings.wiremock_host 
    channel = insecure_channel(host)
    intercepted_channel = grpc.intercept_channel(channel, *INTERCEPTORS)
    return NifflerCurrencyServiceClient(intercepted_channel)