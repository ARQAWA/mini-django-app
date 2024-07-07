import asyncio
import os
from asyncio import CancelledError

import django
import uvloop

from app.core.common.sentry import sentry_init
from app.core.envs import envs

sentry_init()
uvloop.install()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", envs.django_settings_module)
django.setup(set_prefix=False)

try:
    from app.tap_robotics.hamster_kombat.main import run_hamster

    while True:
        asyncio.run(run_hamster())
except (KeyboardInterrupt, SystemExit, CancelledError):
    ...
finally:
    ...
    # hamster_client.close()
