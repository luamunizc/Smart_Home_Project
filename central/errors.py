class HomeError(Exception):
    pass

class InvalidTransition(HomeError):
    ...

class DeviceNotFound(HomeError):
    ...

class DeviceTypeInvalid(HomeError):
    ...

class InvalidConfig(HomeError):
    ...