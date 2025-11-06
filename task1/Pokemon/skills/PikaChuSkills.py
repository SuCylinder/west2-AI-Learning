from base.skills import Skill
from base.pokemon import Pokemon
from effects import effects
from time import sleep
import random

SLEEP_TIME = 1


class Thunderbolt(Skill):
    name = "十万伏特"

    def __init__(self, amount: float = 1.4, activation_chance: int = 10) -> None:
        super().__init__()
        self.amount = amount
        self.activation_chance = activation_chance

    def execute(self, user: "Pokemon", opponent: "Pokemon"):
        if opponent.dodged():
            return
        damage = self.amount * user.attack
        damage *= user.type_effectiveness(opponent)
        if random.randint(1, 100) <= self.activation_chance:
            print(f"{opponent.name} 被麻痹了")
            sleep(SLEEP_TIME)
            opponent.add_status_effect(effects.ParalysisEffect())
        opponent.receive_damage(damage, self.name)


class Quick_Attack(Skill):
    name = "电光一闪"

    def __init__(self, amount: int = 1.0, activation_chance: int = 10) -> None:
        super().__init__()
        self.amount = amount
        self.activation_chance = activation_chance

    def execute(self, user: "Pokemon", opponent: "Pokemon"):
        damage = self.amount * user.attack
        damage *= user.type_effectiveness(opponent)
        if not opponent.dodged():
            opponent.receive_damage(damage, self.name)
        if random.randint(1, 100) <= self.activation_chance:
            print(f"{user.name}的 {self.name} 触发二次攻击!")
            sleep(SLEEP_TIME)
            opponent.receive_damage(damage, self.name)
