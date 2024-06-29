from asyncio.exceptions import CancelledError
from contextlib import suppress

import uvicorn

if __name__ == "__main__":
    with suppress(KeyboardInterrupt, SystemExit, CancelledError):
        uvicorn.run(
            "app.core.asgi:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="debug",
            loop="asyncio",
            http="httptools",
            lifespan="off",
            interface="asgi3",
        )
