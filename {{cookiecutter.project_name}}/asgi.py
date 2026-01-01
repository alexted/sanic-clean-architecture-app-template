from granian import Granian
from granian.log import LogLevels
from granian.constants import Interfaces

if __name__ == "__main__":
    Granian(
        "src.infrastructure.core.application:create_app",
        factory=True,
        reload=True,
        port=5000,
        interface=Interfaces.ASGI,
        log_level=LogLevels.debug,
    ).serve()
