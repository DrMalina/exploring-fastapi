from enum import Enum


class Environment(str, Enum):
    local = "local"
    testing = "testing"
    staging = "staging"
    production = "production"

    @property
    def is_debug(self) -> bool:
        return self in {self.local, self.staging, self.testing}

    @property
    def is_testing(self) -> bool:
        return self == self.testing

    @property
    def is_deployed(self) -> bool:
        return self in {self.staging, self.production}
