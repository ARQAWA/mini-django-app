import loguru


class ShutdownContainer(dict[int, tuple[object, str]]):
    """Контейнер для хранения классов, которые должны быть зачищены при завершении приложения."""

    def __init__(self) -> None:
        super().__init__()

    def registry(self, resource: object, func_name: str) -> None:
        """Регистрация класса."""
        self[id(resource)] = (resource, func_name)

    async def shutdown(self) -> None:
        """Завершение работы."""
        for resource, func_name in self.values():
            shutdown_func = getattr(resource, func_name)
            if callable(shutdown_func):
                res = shutdown_func()
                if hasattr(res, "__await__"):
                    await res
                loguru.logger.info(f"Shutdown {resource.__class__.__name__} complete.")


shutdown_container = ShutdownContainer()
