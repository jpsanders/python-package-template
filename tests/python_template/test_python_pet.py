from python_template.python_pet import PythonPet


class TestPythonPet:
    def test_starts_in_the_middle(self) -> None:
        pet = PythonPet("Baby Python")
        assert (pet.hunger, pet.happiness) == (5, 5)

    def test_feed_and_play(self) -> None:
        pet = PythonPet("Baby Python")
        pet.feed()
        pet.play()
        assert pet.get_status() == "Baby Python: hunger 4, happiness 6"

    def test_levels_stay_within_0_and_10(self) -> None:
        pet = PythonPet("Rex", hunger=0, happiness=10)
        pet.feed()
        pet.play()
        assert (pet.hunger, pet.happiness) == (0, 10)

    def test_as_dict(self) -> None:
        assert PythonPet("Rex").as_dict() == {"name": "Rex", "hunger": 5, "happiness": 5}
