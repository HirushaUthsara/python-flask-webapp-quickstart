class NotFoundError(Exception):
    """Custom exception for not found resources."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)