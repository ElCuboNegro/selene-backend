# Mycroft Server - Backend
# Copyright (C) 2019 Mycroft AI Inc
# SPDX-License-Identifier: 	AGPL-3.0-or-later
#
# This file is part of the Mycroft Server.
#
# The Mycroft Server is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/
"""Account API endpoint to return a list of available wake words."""

from http import HTTPStatus

from selene.api import SeleneEndpoint
from selene.data.wake_word import WakeWordRepository


class WakeWordEndpoint(SeleneEndpoint):
    """Return a list of available wake words"""

    def get(self):
        """Handle a HTTP GET request."""
        self._authenticate()
        response_data = self._build_response_data()

        return response_data, HTTPStatus.OK

    def _build_response_data(self):
        """Build the response to the HTTP GET request."""
        response_data = []
        wake_word_repository = WakeWordRepository(self.db)
        wake_words = wake_word_repository.get_wake_words_for_web()
        for wake_word in wake_words:
            response_data.append(
                dict(id=wake_word.id, name=wake_word.name, user_defined=False,)
            )

        return response_data
