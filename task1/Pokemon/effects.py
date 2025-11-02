from typing import TYPE_CHECKING
from time import sleep
import skills

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


class PoisonEffect(Effect):
    name = "中毒"

    def __init__(self, amount: float = 0.1, duration: int = 3) -> None:
        super().__init__(duration)
        self.amount = amount

    def apply(self, pokemon: "Pokemon") -> None:
        damage = pokemon.get_max_hp() * self.amount
        pokemon.receive_damage(damage, self.name)


class VampiricEffect(Effect):
    name = "寄生种子"

    def __init__(self, opponent: "Pokemon", amount: int, duration: int = 3) -> None:
        super().__init__(duration)
        self.amount = amount
        self.target = opponent

    def apply(self, pokemon: "Pokemon") -> None:
        damage = self.target.get_max_hp() * self.amount
        if self.target.alive:
            print(f"{pokemon.name} 偷取了{self.target.name} 的 {damage} 点 HP!")
            sleep(SLEEP_TIME)
            self.target.receive_damage(damage, self.name)
            pokemon.heal_self(damage)
        else:
            self.duration = -1


class DamageReductionEffect(Effect):
    name = "伤害减免"

    def __init__(self, amount: float = 0.5, duration: int = 1) -> None:
        super().__init__(duration)
        self.amount = amount

    def apply(self, pokemon):
        if self.duration > 0:
            print(f"{pokemon.name} 现在拥有 {self.amount*100}% 的伤害减免")
            pokemon.damage_reduction = self.amount

    def effect_clear(self, pokemon):
        pokemon.damage_reduction = 0


class BurnEffect(Effect):
    name = "烧伤"

    def __init__(self, amount: int = 10, duration: int = 2) -> None:
        super().__init__(duration)
        self.amount = amount

    def apply(self, pokemon):
        damage = self.amount
        pokemon.receive_damage(damage, self.name)


class ParalysisEffect(Effect):
    name = "麻痹"

    def __init__(self, duration: int = 2) -> None:
        super().__init__(duration)

    def apply(self, pokemon):
        if self.duration > 1:
            print(f"{pokemon.name}被麻痹了,无法行动")
            pokemon.cant_move = True

    def effect_clear(self, pokemon):
        pokemon.cant_move = False


class Flame(Effect):
    name = "蓄力中"

    def __init__(self, opponent: "Pokemon", duration: int = 2) -> None:
        super().__init__(duration)
        self.target = opponent

    def apply(self, pokemon):
        if self.duration > 1:
            print(f"{pokemon.name} 蓄力中,无法行动")
            pokemon.cant_move = True

    def effect_clear(self, pokemon):
        pokemon.cant_move = False
        print(f"{pokemon}蓄力完成")
        pokemon.use_skill(skills.Flame_Charge_fire.execute(pokemon, self.target))
