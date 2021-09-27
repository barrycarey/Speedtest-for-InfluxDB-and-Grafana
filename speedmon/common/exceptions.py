class SpeedtestExceptionBase(Exception):
    pass


class SpeedtestRunError(SpeedtestExceptionBase):
    def __init__(self, message):
        super(SpeedtestRunError, self).__init__(message)


class StorageHandlerFailure(SpeedtestExceptionBase):
    def __init__(self, message):
        super(StorageHandlerFailure, self).__init__(message)

class UnsupportedOperatingSystem(SpeedtestExceptionBase):
    def __init__(self, message):
        super(UnsupportedOperatingSystem, self).__init__(message)

class SpeedtestInstallFailure(SpeedtestExceptionBase):
    def __init__(self, message):
        super(SpeedtestInstallFailure, self).__init__(message)
