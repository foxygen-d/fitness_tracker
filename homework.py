from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    result_str = ('Тип тренировки: {training_type}; '
                  'Длительность: {duration:.3f} ч.; '
                  'Дистанция: {distance:.3f} км; '
                  'Ср. скорость: {speed:.3f} км/ч; '
                  'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Возвращает строку сообщения."""
        return self.result_str.format(training_type=self.training_type,
                                      duration=self.duration,
                                      distance=self.distance,
                                      speed=self.speed,
                                      calories=self.calories)


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MINS_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration_h = duration
        self.weight = weight
        self.duration_m = self.duration_h * self.MINS_IN_HOUR

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return 22 * 9.247 + 3.098 * self.LEN_STEP

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=type(self).__name__,
                           duration=self.duration_h,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    K_1: int = 18
    K_2: int = 20

    def get_spent_calories(self) -> float:
        """Возвращает число потраченных калорий при беге."""
        return((self.K_1 * self.get_mean_speed() - self.K_2)
               * self.weight / self.M_IN_KM * self.duration_m)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    K_1: float = 0.035
    K_2: float = 0.029
    DEGREE: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return((self.K_1 * self.weight + (self.get_mean_speed() ** self.DEGREE
               // self.height) * self.K_2 * self.weight) * self.duration_m)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    K_1: float = 1.1
    K_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration_h)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.K_1) * self.K_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_sports: dict = {'SWM': Swimming,
                             'RUN': Running,
                             'WLK': SportsWalking}

    if workout_type in types_of_sports:
        return types_of_sports[workout_type](*data)
    else:
        raise Exception('Ошибка! Такого вида спорта в нашем фитнес-трекере нет!')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('BOX', [1, 1])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        if type(training) is str:
            print(training)
        else:
            main(training)
