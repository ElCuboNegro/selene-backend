"""Authenticate a user logging in with a email address and password

This type of login is considered "internal" because we are storing the email
address and password on our servers.  This is as opposed to "external"
authentication, which uses a 3rd party authentication, like Google.
"""

from binascii import a2b_base64
from http import HTTPStatus

from selene.data.account import Account, AccountRepository
from selene.api import SeleneEndpoint
from selene.util.auth import AuthenticationError


class AuthenticateInternalEndpoint(SeleneEndpoint):
    """Sign in a user with an email address and password."""
    def __init__(self):
        super(AuthenticateInternalEndpoint, self).__init__()
        self.account: Account = None

    def get(self):
        """Process HTTP GET request."""
        self._authenticate_credentials()
        self._generate_tokens()
        self._set_token_cookies()

        return '', HTTPStatus.NO_CONTENT

    def _authenticate_credentials(self):
        """Compare credentials in request to credentials in database.

        :raises AuthenticationError when no match found on database
        """
        basic_credentials = self.request.headers['authorization']
        binary_credentials = a2b_base64(basic_credentials[6:])
        email_address, password = binary_credentials.decode().split(':||:')
        acct_repository = AccountRepository(self.db)
        self.account = acct_repository.get_account_from_credentials(
                email_address,
                password
        )
        if self.account is None:
            raise AuthenticationError('provided credentials not found')
        self.access_token.account_id = self.account.id
        self.refresh_token.account_id = self.account.id
