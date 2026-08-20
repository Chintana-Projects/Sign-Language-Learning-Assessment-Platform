from abc import ABC, abstractmethod


class GestureRule(ABC):

    def __init__(self, gesture: str):

        self.gesture = gesture



    @abstractmethod
    def evaluate(
            self,
            landmarks: list,
            deviations: list,
            messages: list
    ) -> bool:

        pass