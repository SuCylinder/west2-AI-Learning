import random
from typing import TYPE_CHECKING
import effects
from time import sleep

SLEEP_TIME = 1

if TYPE_CHECKING:
    from pokemon import Pokemon


class Skill:
    name: str

    def __init__(self) -> None:
        pass

    def execute(self, user: "Pokemon", opponent: "Pokemon"):
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.name}"


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
        else:
            print(f"{self.name} 没有对 {opponent.name} 造成中毒效果.")
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


class Aqua_Jet(Skill):
    name = "水枪"

    def __init__(self, amount: float = 1.4) -> None:
        super().__init__()
        self.amount = amount

    def execute(self, user, opponent):
        if opponent.dodged():
            return
        damage = self.amount * user.attack
        damage *= user.type_effectiveness(opponent)
        opponent.receive_damage(damage, self.name)


class Shield(Skill):
    name = "护盾"

    def __init__(self, amount: float = 0.5) -> None:
        super().__init__()
        self.amount = amount

    def execute(self, user, opponent):
        a = effects.DamageReductionEffect(self.amount)
        a.apply(user)
        user.add_status_effect(a)
        a.duration -= 1


class Ember(Skill):
    name = "火花"

    def __init__(self, amount: float = 1, chance: int = 10) -> None:
        super().__init__()
        self.amount = amount
        self.chance = chance

    def execute(self, user, opponent):
        if opponent.dodged():
            return False
        damage = user.attack * self.amount
        damage *= user.type_effectiveness(opponent)
        if random.randint(1, 100) <= self.chance:
            print(f"{user.name} 使 {opponent.name} 陷入烧伤")
            sleep(SLEEP_TIME)
            opponent.add_status_effect(effects.BurnEffect())
        opponent.receive_damage(damage, self.name)
        return True


class Flame_Charge(Skill):
    name = "蓄能爆炎-蓄力"

    def __init__(self, amount: float = 3, chance: int = 80) -> None:
        super().__init__()
        self.amount = amount
        self.chance = chance

    def execute(self, user, opponent):
        user.add_status_effect(effects.Flame(opponent))
        return False


class Flame_Charge_fire(Skill):
    name = "蓄能爆炎-发射"

    def __init__(self, amount: float = 3, chance: int = 80) -> None:
        super().__init__()
        self.amount = amount
        self.chance = chance

    def execute(self, user, opponent):
        if opponent.dodged():
            return False
        damage = user.attack * self.amount
        damage *= user.type_effectiveness(opponent)
        if random.randint(1, 100) <= 80:
            print(f"{user.name} 使 {opponent.name} 陷入烧伤")
            sleep(SLEEP_TIME)
            opponent.add_status_effect(effects.BurnEffect())
        opponent.receive_damage(damage, self.name)
        return True


class Crash(Skill):
    name = "撞击"

    def __init__(self, amount: int = 1):
        self.amount = amount

    def execute(self, user, opponent):
        damage = user.attack * self.amount
        opponent.receive_damage(damage, self.name)


class Imitate(Skill):
    name = "模仿"

    def __init__(self):
        pass

    def execute(self, user, opponent):
        skills = opponent.skills
        skill_to_use = random.choice(skills)
        print(f"{user.name} 模仿了 {opponent.name} 的 {skill_to_use.name}")
        user.use_skill(skill_to_use, opponent)
