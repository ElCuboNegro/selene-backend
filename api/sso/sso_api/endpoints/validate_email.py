from binascii import a2b_base64
from http import HTTPStatus

from selene.api import SeleneEndpoint
from selene.data.account import AccountRepository
from selene.util.auth import (
    get_facebook_account_email,
    get_github_account_email,
    get_google_account_email
)


class ValidateEmailEndpoint(SeleneEndpoint):
    def get(self):
        return_data = dict(accountExists=False, noFederatedEmail=False)
        if self.request.args['token']:
            email_address = self._get_email_address()
            account_repository = AccountRepository(self.db)
            account = account_repository.get_account_by_email(email_address)
            if account is None:
                if self.request.args['platform'] != 'Internal':
                    return_data.update(noFederatedEmail=True)
            else:
                return_data.update(accountExists=True)

        return return_data, HTTPStatus.OK

    def _get_email_address(self):
        if self.request.args['platform'] == 'Google':
            email_address = get_google_account_email(
                self.request.args['token']
            )
        elif self.request.args['platform'] == 'Facebook':
            email_address = get_facebook_account_email(
                self.request.args['token']
            )
        elif self.request.args['platform'] == 'GitHub':
            email_address = get_github_account_email(
                self.request.args['token']
            )
        else:
            coded_email = self.request.args['token']
            email_address = a2b_base64(coded_email).decode()

        return email_address
