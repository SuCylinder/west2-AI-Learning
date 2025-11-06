from typing import TYPE_CHECKING
from time import sleep
from . import skills

SLEEP_TIME = 1

if TYPE_CHECKING:
    from pokemon import Pokemon


class Effect:
    name: str

    def __init__(self, duration: int) -> None:
        # 初始化效果持续时间
        self.duration = duration

    def apply(self, pokemon: "Pokemon") -> None:
        # 应用效果的抽象方法，子类需要实现
        raise NotImplementedError

    def decrease_duration(self) -> None:
        # 减少效果持续时间
        self.duration -= 1
        if self.duration > 0:
            print(f"{self.name} 持续时间减少. 剩余: {self.duration} 回合")
        else:
            print(f"{self.name} 效果消失.")
        sleep(SLEEP_TIME)

    def effect_clear(self, pokemon: "Pokemon"):
        return
