from client import Client
from endpoints import TenantEndpoint, TournamentEndpoint

class PlaytomicClient:
    def __init__(self, email, password):
        self.client = Client(email, password)
        self.Tenant = TenantEndpoint(self.client)
        self.Tournament = TournamentEndpoint(self.client)
