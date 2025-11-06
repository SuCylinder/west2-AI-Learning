from base.effects import Effect
from base.pokemon import Pokemon
from skills import CharmanderSkills
from time import sleep

SLEEP_TIME = 1


class DamageReductionEffect(Effect):
    name = "伤害减免"

    def __init__(self, amount: float = 0.5, duration: int = 1) -> None:
        super().__init__(duration)
        self.amount = amount

    def apply(self, pokemon):
        if self.duration > 0:
            print(f"{pokemon.name} 现在拥有 {self.amount*100}% 的伤害减免")
            sleep(SLEEP_TIME)
            pokemon.damage_reduction = self.amount

    def effect_clear(self, pokemon):
        pokemon.damage_reduction = 0


class Flame(Effect):
    name = "蓄力中"

    def __init__(self, opponent: "Pokemon", duration: int = 2) -> None:
        super().__init__(duration)
        self.target = opponent

    def apply(self, pokemon):
        if self.duration > 1:
            print(f"{pokemon.name} 蓄力中,无法行动")
            sleep(SLEEP_TIME)
            pokemon.cant_move = True

    def effect_clear(self, pokemon):
        pokemon.cant_move = False
        print(f"{pokemon.name} 蓄力完成")
        sleep(SLEEP_TIME)
        pokemon.use_skill(CharmanderSkills.Flame_Charge_fire(), self.target)
