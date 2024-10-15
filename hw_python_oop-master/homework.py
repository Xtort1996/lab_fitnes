class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float, distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_MIN = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__, self.duration, self.get_distance(), self.get_mean_speed(), self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    SEC_IN_MIN = 60
    def get_spent_calories(self):
        CALORIES_MEAN_SPEED_MULTIPLIER = 18
        CALORIES_MEAN_SPEED_SHIFT = 1.79
        SEC_IN_MIN = 60
        return ((CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() + CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM * self.duration * SEC_IN_MIN)


class SportsWalking(Training):

    MULTI_WEIGHT = 0.035
    H_IN_MIN = 60
    MULTI_HEIGHT = 0.029
    KM_H_IN_M_S = 0.278
    M_IN_SM = 100
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int, duration: float, weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height



    def get_spent_calories(self):
        MULTI_WEIGHT = 0.035
        MULTI_HEIGHT = 0.029
        SEC_IN_MIN = 60
        KM_H_IN_M_S = 0.278
        M_IN_CM = 100
        height_in_meters = self.height / M_IN_CM
        mean_speed_in_ms = self.get_mean_speed() * KM_H_IN_M_S

        return ((MULTI_WEIGHT * self.weight
                + (mean_speed_in_ms ** 2 / height_in_meters) * MULTI_HEIGHT
                * self.weight) * self.duration * SEC_IN_MIN)


class Swimming(Training):
    LEN_STEP = 1.38
    MID_SPEED = 1.1
    MULTI_SPEED = 2


    """Тренировка: плавание."""
    def __init__(self, action: int, duration: float, weight: float, length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        return ((self.get_mean_speed() + 1.1) * 2 * self.duration
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return train_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


packages = [
    ('SWM', [720, 1, 80, 25, 40]),
    ('RUN', [15000, 1, 75]),
    ('WLK', [9000, 1, 75, 180]),
]

for workout_type, data in packages:
    training = read_package(workout_type, data)
    main(training)