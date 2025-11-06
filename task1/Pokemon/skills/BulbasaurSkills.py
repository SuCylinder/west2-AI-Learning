from base.skills import Skill
from base.pokemon import Pokemon
from effects import effects
from time import sleep
import random

SLEEP_TIME = 1


class SeedBomb(Skill):
    name = "种子炸弹"

    def __init__(self, activation_chance: int = 15) -> None:
        super().__init__()
        self.activation_chance = activation_chance  # 确保激活几率被正确初始化

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> None:
        if opponent.dodged():
            return
        # 造成伤害
        damage = user.attack
        damage *= user.type_effectiveness(opponent)  # 属性克制倍率

        if random.randint(1, 100) <= self.activation_chance:
            opponent.add_status_effect(effects.PoisonEffect())
            print(f"{opponent.name} 被 {self.name} 下毒了!")
        sleep(SLEEP_TIME)
        opponent.receive_damage(damage, self.name)
        # 判断是否触发状态效果
        print()


class ParasiticSeeds(Skill):
    name = "寄生种子"

    def __init__(self, amount: int) -> None:
        super().__init__()
        self.amount = amount

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> None:
        if opponent.dodged():
            return
        # 给使用者添加治疗效果
        user.add_status_effect(effects.VampiricEffect(opponent, self.amount))
        print(f"{opponent.name} 被 {user.name} 寄生了!")
        sleep(SLEEP_TIME)
