from base.effects import Effect
from base.pokemon import Pokemon
from time import sleep

SLEEP_TIME = 1


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
            print(f"{pokemon.name} 被麻痹了,无法行动")
            sleep(SLEEP_TIME)
            pokemon.cant_move = True

    def effect_clear(self, pokemon):
        pokemon.cant_move = False
