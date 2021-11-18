class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str = None,
                 duration: float = None,
                 distance: float = None,
                 speed: float = None,
                 calories: float = None) -> None:
        self.speed = speed
        self.calories = calories
        self.duration = duration
        self.distance = distance
        self.training_type = training_type

    def get_message(self):
        """Возвращает сообщение с результатами тренеровки"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.weight = weight
        self.duration = duration
        self.workout_time_min = self.duration * 60

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
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=distance_km,
                           speed=mean_speed,
                           calories=spent_calories)


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1 = 18
        coeff_2 = 20
        w = self.weight
        m_k = self.M_IN_KM
        wtm = self.workout_time_min
        mean_s = self.get_mean_speed()
        return ((coeff_1 * mean_s - coeff_2) * w / m_k * wtm)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1 = 0.035
        coeff_2 = 0.029
        w = self.weight
        h = self.height
        wtm = self.workout_time_min
        mean_s = self.get_mean_speed()
        return ((coeff_1 * w + (mean_s**2 // h) * coeff_2 * w) * wtm)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        d = self.duration
        m_k = self.M_IN_KM
        c_p = self.count_pool
        l_p = self.length_pool
        return (l_p * c_p / m_k / d)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_cal_1 = 1.1
        coeff_cal_2 = 2
        mean_speed = self.get_mean_speed()
        return (mean_speed + coeff_cal_1) * coeff_cal_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_trainings = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}
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
