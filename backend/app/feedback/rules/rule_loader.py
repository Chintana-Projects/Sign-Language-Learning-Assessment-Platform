from .rule_A import RuleA
from .rule_B import RuleB
from .rule_C import RuleC
from .rule_D import RuleD
from .rule_E import RuleE
from .rule_F import RuleF
from .rule_G import RuleG
from .rule_H import RuleH
from .rule_I import RuleI
from .rule_J import RuleJ
from .rule_K import RuleK
from .rule_L import RuleL
from .rule_M import RuleM
from .rule_N import RuleN
from .rule_O import RuleO
from .rule_P import RuleP
from .rule_Q import RuleQ
from .rule_R import RuleR
from .rule_S import RuleS
from .rule_T import RuleT
from .rule_U import RuleU
from .rule_V import RuleV
from .rule_W import RuleW
from .rule_X import RuleX
from .rule_Y import RuleY
from .rule_Z import RuleZ

from .default_rule import DefaultRule


class RuleLoader:
    """
    Loads the appropriate rule for each ASL alphabet.
    Falls back to DefaultRule if a rule is unavailable.
    """

    def __init__(self):

        self.rules = {
            "A": RuleA(),
            "B": RuleB(),
            "C": RuleC(),
            "D": RuleD(),
            "E": RuleE(),
            "F": RuleF(),
            "G": RuleG(),
            "H": RuleH(),
            "I": RuleI(),
            "J": RuleJ(),
            "K": RuleK(),
            "L": RuleL(),
            "M": RuleM(),
            "N": RuleN(),
            "O": RuleO(),
            "P": RuleP(),
            "Q": RuleQ(),
            "R": RuleR(),
            "S": RuleS(),
            "T": RuleT(),
            "U": RuleU(),
            "V": RuleV(),
            "W": RuleW(),
            "X": RuleX(),
            "Y": RuleY(),
            "Z": RuleZ(),
        }

    def get_rule(self, letter):

        if not letter:
            return DefaultRule("?")

        letter = str(letter).upper()

        return self.rules.get(
            letter,
            DefaultRule(letter)
        )