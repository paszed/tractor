class TractorError(Exception):
    pass


class FetchError(TractorError):
    pass


class ConfigError(TractorError):
    pass


class SelectorError(TractorError):
    pass
