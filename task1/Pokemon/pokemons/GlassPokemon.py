from base.pokemon import Pokemon
from skills import BulbasaurSkills
from time import sleep

SLEEP_TIME = 1


class GlassPokemon(Pokemon):
    type = "草"

    def type_effectiveness(self, opponent: Pokemon):
        # 针对敌方 Pokemon 的类型，调整效果倍率
        effectiveness = 1.0
        opponent_type = opponent.type

        if opponent_type == "水":
            print("效果拔群!")
            sleep(SLEEP_TIME)
            effectiveness = 2.0
        elif opponent_type == "火":
            print("收效甚微")
            sleep(SLEEP_TIME)
            effectiveness = 0.5
        return effectiveness

    def begin(self):
        # 每个回合开始时执行草属性特性
        self.glass_attribute()
        self.apply_status_effect()

    def glass_attribute(self):
        # 草属性特性：每回合恢复最大 HP 的 10%
        amount = self.max_hp * 0.1
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(
            f"{self.name} 在回合开始时治疗了 {amount} HP! 当前 HP: {self.hp}/{self.max_hp}"
        )
        sleep(SLEEP_TIME)


# Bulbasaur 类，继承自 GlassPokemon
class Bulbasaur(GlassPokemon):
    name = "妙蛙种子"

    def __init__(self, hp=100, attack=35, defense=10, dodge_chance=15) -> None:
        # 初始化 Bulbasaur 的属性
        super().__init__(hp, attack, defense, dodge_chance)

    def initialize_skills(self):
        # 初始化技能，具体技能是 SeedBomb 和 ParasiticSeeds
        return [BulbasaurSkills.SeedBomb(), BulbasaurSkills.ParasiticSeeds(amount=0.1)]
