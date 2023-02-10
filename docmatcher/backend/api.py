from os import environ

import uvicorn

from api.app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(environ.get("PORT", "3001"))
    log_level = environ.get("LOG_LEVEL", "info")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level=log_level)
