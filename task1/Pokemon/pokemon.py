from __future__ import annotations
from time import sleep
import skills
from skills import Skill
from effects import Effect
import random

SLEEP_TIME = 1


class Pokemon:
    name: str
    type: str
    effect_list = ["中毒", "寄生种子"]
    is_Paralysis = False

    def __init__(self, hp: int, attack: int, defense: int, dodge_chance: int) -> None:
        # 初始化 Pokemon 的属性
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.skills = self.initialize_skills()
        self.alive = True
        self.statuses = []
        self.dodge_chance = dodge_chance
        self.damage_reduction = 0

    def get_max_hp(self):
        return self.max_hp

    def initialize_skills(self):
        # 抽象方法，子类应实现具体技能初始化
        raise NotImplementedError

    def use_skill(self, skill: Skill, opponent: Pokemon):
        # 使用技能
        print(f"{self.name} 使用了 {skill.name}!")
        sleep(SLEEP_TIME)
        skill.execute(self, opponent)

    def heal_self(self, amount):
        # 为自身恢复生命值
        if not isinstance(amount, int):
            amount = int(amount)

        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"{self.name} 恢复了 {amount} HP! 现在的 HP: {self.hp}/{self.max_hp}")
        sleep(SLEEP_TIME)

    def receive_damage(self, damage, type: str):
        # 计算伤害并减去防御力，更新 HP
        if not isinstance(damage, int):
            damage = int(damage)

        if type not in self.effect_list:
            damage -= self.defense
            if damage <= 0:
                print(f"{self.name} 防御了这次攻击!")
                sleep(SLEEP_TIME)
                return

        self.hp -= damage
        print(f"{self.name} 受到了 {type} 的 {damage} 点伤害!", end=" ")
        print(f"当前 HP: {self.hp}/{self.max_hp}")
        sleep(SLEEP_TIME)
        if self.hp <= 0:
            self.alive = False
            print(f"{self.name} 倒下了!")
            sleep(SLEEP_TIME)

    def add_status_effect(self, effect: Effect):
        # 添加状态效果
        self.statuses.append(effect)

    def apply_status_effect(self):
        # 应用所有当前的状态效果，并移除持续时间结束的效果
        for status in self.statuses[:]:  # 使用切片防止列表在遍历时被修改
            status.apply(self)
            status.decrease_duration()
            if status.duration <= 0:
                sleep(SLEEP_TIME)
                status.effect_clear(self)
                self.statuses.remove(status)

    def type_effectiveness(self, opponent: Pokemon):
        # 计算属性克制的抽象方法，具体实现由子类提供
        raise NotImplementedError

    def dodged(self):
        if random.randint(1, 100) <= self.dodge_chance:
            print(f"{self.name} 闪避了这次攻击!")
            sleep(SLEEP_TIME)
            return True
        else:
            return False

    def begin(self):
        # 新回合开始时触发的方法
        pass

    def __str__(self) -> str:
        return f"{self.name} 属性: {self.type}"


# GlassPokemon 类
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


class ElectricPokemon(Pokemon):
    type = "电"
    is_dodged = False

    def type_effectiveness(self, opponent: Pokemon):
        effectiveness = 1.0
        opponent_type = opponent.type

        if opponent_type == "水":
            print("效果拔群!")
            sleep(SLEEP_TIME)
            effectiveness = 2.0
        elif opponent_type == "草":
            print("收效甚微")
            sleep(SLEEP_TIME)
            effectiveness = 0.5
        return effectiveness

    def dodged(self):
        self.is_dodged = super().dodged()
        return self.is_dodged

    def begin(self):
        self.apply_status_effect()


class WaterPokemon(Pokemon):
    type = "水"

    def type_effectiveness(self, opponent: Pokemon):
        effectiveness = 1.0
        opponent_type = opponent.type

        if opponent_type == "火":
            print("效果拔群!")
            sleep(SLEEP_TIME)
            effectiveness = 2.0
        elif opponent_type == "电":
            print("收效甚微")
            sleep(SLEEP_TIME)
            effectiveness = 0.5
        return effectiveness

    def begin(self):
        self.apply_status_effect()

    def receive_damage(self, damage, type, chance=50, damage_reduction=0.3):
        # 计算伤害并减去防御力，更新 HP
        if not isinstance(damage, int):
            damage = int(damage)

        if type not in self.effect_list:
            damage -= self.defense
            if damage <= 0:
                print(f"{self.name} 防御了这次攻击!")
                sleep(SLEEP_TIME)
                return
        if random.randint(1, 100) <= chance:
            print(f"{self.name}触发伤害减免!")
            sleep(SLEEP_TIME)
            damage *= 1 - damage_reduction - self.damage_reduction
        else:
            damage *= 1 - self.damage_reduction
        self.hp -= damage
        print(f"{self.name} 受到了 {type} 的 {damage} 点伤害!", end=" ")
        print(f"当前 HP: {self.hp}/{self.max_hp}")
        sleep(SLEEP_TIME)
        if self.hp <= 0:
            self.alive = False
            print(f"{self.name} 倒下了!")
            sleep(SLEEP_TIME)


# Bulbasaur 类，继承自 GlassPokemon
class Bulbasaur(GlassPokemon):
    name = "妙蛙种子"

    def __init__(self, hp=100, attack=35, defense=10, dodge_chance=15) -> None:
        # 初始化 Bulbasaur 的属性
        super().__init__(hp, attack, defense, dodge_chance)

    def initialize_skills(self):
        # 初始化技能，具体技能是 SeedBomb 和 ParasiticSeeds
        return [skills.SeedBomb(), skills.ParasiticSeeds(amount=0.1)]


class PikaChu(ElectricPokemon):
    name = "皮卡丘"

    def __init__(self, hp=80, attack=35, defense=5, dodge_chance=30) -> None:
        # 初始化 Bulbasaur 的属性
        super().__init__(hp, attack, defense, dodge_chance)

    def initialize_skills(self):
        return [skills.Thunderbolt(), skills.Quick_Attack()]


class Squirtle(WaterPokemon):
    name = "杰尼龟"

    def __init__(self, hp=80, attack=25, defense=20, dodge_chance=20) -> None:
        super().__init__(hp, attack, defense, dodge_chance)

    def initialize_skills(self):
        return [skills.Aqua_Jet(), skills.Shield()]
