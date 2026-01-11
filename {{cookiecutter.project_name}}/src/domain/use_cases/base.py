import abc
from typing import Union




class BaseUseCase(abc.ABC):
    @abc.abstractmethod
    def execute(self, request_object: BaseModel) -> BaseModel | None:
        raise NotImplementedError("Please implement this method")
