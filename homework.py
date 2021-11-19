from dataclasses import dataclass
from typing import ClassVar


@dataclass(
    init=True,
    repr=False,
    eq=False,
    order=False,
    unsafe_hash=False,
    frozen=False)
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str = None
    duration: float = None
    distance: float = None
    speed: float = None
    calories: float = None

    def get_message(self):
        """Возвращает сообщение с результатами тренеровки"""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


@dataclass(
    init=True,
    repr=False,
    eq=False,
    order=False,
    unsafe_hash=False,
    frozen=False)
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance_km = self.get_distance()
        return distance_km / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance_km = self.get_distance()
        mean_speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()
        return InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration,
            distance=distance_km,
            speed=mean_speed,
            calories=spent_calories
        )


@dataclass(
    init=True,
    repr=False,
    eq=False,
    order=False,
    unsafe_hash=False,
    frozen=False)
class Running(Training):
    """Тренировка: бег."""
    COEFF_1: ClassVar[int] = 18
    COEFF_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed = self.get_mean_speed()
        workout_time_min = self.duration * 60
        return (
            (self.COEFF_1 * mean_speed - self.COEFF_2)
            * self.weight / self.M_IN_KM * workout_time_min
        )


@dataclass(
    init=True,
    repr=False,
    eq=False,
    order=False,
    unsafe_hash=False,
    frozen=False)
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_1: ClassVar[float] = 0.035
    COEFF_2: ClassVar[float] = 0.029

    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed = self.get_mean_speed()
        workout_time_min = self.duration * 60
        return (
            (self.COEFF_1 * self.weight
             + (mean_speed**2 // self.height)
             * self.COEFF_2 * self.weight) * workout_time_min
        )


@dataclass(
    init=True,
    repr=False,
    eq=False,
    order=False,
    unsafe_hash=False,
    frozen=False)
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    COEFF_1: ClassVar[float] = 1.1
    COEFF_2: ClassVar[int] = 2

    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed = self.get_mean_speed()
        return (mean_speed + self.COEFF_1) * self.COEFF_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_trainings = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in dict_trainings:
        raise TypeError(f'Неизвестный тип датчика, "{workout_type}"')

    return dict_trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
