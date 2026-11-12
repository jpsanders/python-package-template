"""The example the template ships with: a pet whose state is two small numbers."""

from dataclasses import asdict, dataclass

LOWEST, HIGHEST = 0, 10


@dataclass
class PythonPet:
    """
    A pet with a hunger and a happiness level, each from 0 to 10.

    :param name: What the pet is called
    :param hunger: 0 is full, 10 is starving
    :param happiness: 0 is sad, 10 is happy
    """

    name: str
    hunger: int = 5
    happiness: int = 5

    def feed(self) -> None:
        """Lower the hunger level by one, never below 0."""
        self.hunger = max(LOWEST, self.hunger - 1)

    def play(self) -> None:
        """Raise the happiness level by one, never above 10."""
        self.happiness = min(HIGHEST, self.happiness + 1)

    def get_status(self) -> str:
        """
        Describe the pet in one line.

        :returns: The status line
        """
        return f"{self.name}: hunger {self.hunger}, happiness {self.happiness}"

    def as_dict(self) -> dict[str, str | int]:
        """
        Return the pet as plain data, for ``--json``.

        :returns: The pet's fields
        """
        return asdict(self)
