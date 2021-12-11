from enum import auto, Enum
from typing import List


class DeploymentType(Enum):
    DEPLOY = auto()
    DESTROY = auto()

    @staticmethod
    def to_list() -> List['DeploymentType']:
        items = []
        for item in DeploymentType:
            items.append(item)
        return items

    @staticmethod
    def to_string_list() -> List[str]:
        items = []
        for item in DeploymentType.to_list():
            items.append(item.name)
        return items
