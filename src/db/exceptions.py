class DbSessionManagerNotInitializedError(Exception):
    def __init__(self) -> None:
        super().__init__("DatabaseSessionManager is not initialized")
