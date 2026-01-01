import abc

from pydantic import BaseModel


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def convert_to_dto(self, obj) -> BaseModel:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, obj_data: BaseModel) -> BaseModel:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, filters: BaseModel) -> list[BaseModel]:
        raise NotImplementedError
