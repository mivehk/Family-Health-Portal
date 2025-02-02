from django.core.mail.backends.smtp import EmailBackend
from msal import ConfidentialClientApplication
from django.conf import settings

class OAuthEmailBackend(EmailBackend):
    def __init__(self, **kwargs): #constructor inheriting smtp emailBackend with OAuth properties
        super().__init__(**kwargs)
        self.client_id = kwargs.get("client_id", settings.OAUTH_CLIENT_ID)
        self.client_secret = kwargs.get("client_secret", settings.OAUTH_CLIENT_SECRET)
        self.tenant_id = kwargs.get("tenant_id", settings.OAUTH_TENANT_ID)
        self.token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        self.access_token = None


    def open(self):
        """
        Override to authenticate with OAuth and acquire an access token.
        """
        if self.connection:
            return False

        try:
            app = ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
            )
            result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

            if "access_token" not in result:
                raise Exception(f"Failed to acquire access token: {result.get('error_description')}")

            self.access_token = result["access_token"]

            self.connection = super().open()
            # Dynamically create auth_plain with username and accesstoken
            self.connection.auth_plain = lambda: f"user={self.username}\x01auth=Bearer {self.access_token}\x01\x01"

            return True
        except Exception as e:
            raise Exception(f"Error during OAuth authentication: {e}")
