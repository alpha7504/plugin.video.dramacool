"""
    Plugin for ResolveUrl
    Copyright (C) 2021 groggyegg

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import re
from resolveurl.resolver import ResolveUrl


class AsianLoadResolver(ResolveUrl):
    name = "asianload"
    domains = ['asianload.cc', 'asianload.io', 'asianload.net']
    pattern = r'(?://|\.)(asianload\.\w+)/\w+\.php\?(.+)'

    def get_media_url(self, host, media_id):
        html = self.net.http_GET(self.get_url(host, media_id)).content
        match = re.search(r'<div class="dowload">.+?href="([^"]+)"', html, re.DOTALL)

        if match:
            return match.group(1)

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/video.php?{media_id}')

    @classmethod
    def _is_enabled(cls):
        return True
