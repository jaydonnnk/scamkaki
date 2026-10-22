"""Apply pending SQL migrations to DATABASE_URL (or the URL given as the first argument)."""

import sys

from scamkaki.lib.db import migrate
from scamkaki.lib.env import get_settings

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else get_settings().database_url
    applied = migrate(url)
    print("applied:", ", ".join(applied) if applied else "nothing pending")
