import base64
import logging
from django.core.mail.backends.smtp import EmailBackend
from msal import ConfidentialClientApplication
from django.conf import settings

logger = logging.getLogger(__name__)

class OAuthEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize additional attributes
        self.authority = settings.OAUTH_AUTHORITY
        self.scopes = settings.OAUTH_SCOPES

    def _send(self, email_message):
        """
        Override the _send method to include OAuth2 token-based authentication.
        """
        access_token = self._get_access_token()
        # Use XOAUTH2 token for SMTP authentication
        #self.connection.login(
        #    user=self.username,
        #    password=self._generate_xoauth2_token(access_token)
        #)
        auth_string = self._generate_xoauth2_token(access_token)
        #auth_string = f"user={settings.EMAIL_HOST_USER}\x01auth=Bearer {access_token}\x01\x01"
        print(f"Auth string: {auth_string}")
        self.connection.docmd("AUTH", f"XOAUTH2 {auth_string}")
        super()._send(email_message)

    def _get_access_token(self):
        """
        Obtain an OAuth2 access token using MSAL.
        """
        try:
            app = ConfidentialClientApplication(
                client_id=settings.OAUTH_CLIENT_ID,
                client_credential=settings.OAUTH_CLIENT_SECRET,
                authority=self.authority,
            )
            result = app.acquire_token_for_client(scopes=self.scopes)
            if not result.get("access_token"):
                logger.error(f"Failed to obtain access token: {result.get('error_description', 'Unknown error')}")
                raise Exception("Failed to obtain OAuth2 access token")
            logger.info("Successfully obtained access token.")
            return result["access_token"]
        except Exception as e:
            logger.error(f"Error while obtaining access token: {str(e)}")
            raise

    def _generate_xoauth2_token(self, access_token):
        """
        Generate the XOAUTH2 string for SMTP authentication.
        """
        token = f"user={self.username}\x01auth=Bearer {access_token}\x01\x01"
        return base64.b64encode(token.encode()).decode()
