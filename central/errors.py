class SmartHomeError(Exception):
    # Base para exceções
    pass

class InvalidTransitionError(SmartHomeError):
    # falha de transição de estado
    pass

class DeviceNotFoundError(SmartHomeError):
    pass

class InvalidConfigError(SmartHomeError):
    pass