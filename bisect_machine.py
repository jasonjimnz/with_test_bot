class StateBisect(object):
    left: int = 0
    right: int = None
    total_elements: int = None
    mapper: callable = None

    def __init__(
            self,
            left: int = None,
            right: int = None,
            total_elements: int = None,
            mapper: callable = None
    ):
        if left:
            self.left = left
        if total_elements:
            self.total_elements = total_elements
            self.right = total_elements - 1
        if right:
            self.right = right
        if mapper:
            self.mapper = mapper

    def bisect_interaction(self, tester: callable):
        """
        Performs a single bisect iteration, will update
        one of the edges based on the tester output and
        after the state update will return True if the
        bisection iteration can continue or False if the
        bisection finishes

        :param tester:
        :return:
        """
        mid = self.get_mid_value()

        val = self.mapper(mid) if self.mapper else self.default_mapper(mid)

        if tester(val):
            self.right = mid
        else:
            self.left = mid

        return self.left + 1 < self.right

    def get_mid_value(self):
        return int((self.left + self.right) / 2)

    @classmethod
    def default_mapper(cls, value: int) -> int:
        return value

    @staticmethod
    def get_bisection_from_state(state_dict: dict) -> object:
        return StateBisect(**state_dict)

    def serialize_bisect_state(self) -> dict:
        return {
            "left": self.left,
            "right": self.right,
            "total_elements": self.total_elements,
            "mapper": self.mapper
        }