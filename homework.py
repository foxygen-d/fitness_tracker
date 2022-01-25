from dataclasses import dataclass

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""    
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    my_str = ('Тип тренировки: {training_type}; '
              'Длительность: {duration:.3f} ч.; '
              'Дистанция: {distance:.3f} км; '
              'Ср. скорость: {speed:.3f} км/ч; '
              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Возвращает строку сообщения."""
        return self.my_str.format(training_type=self.training_type,
                                  duration=self.duration,
                                  distance=self.distance,
                                  speed=self.speed,
                                  calories=self.calories)


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    mins_in_hour: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration_h = duration
        self.weight = weight
        self.distance = self.get_distance()

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""        
        return self.distance / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=type(self).__name__,
                           duration=self.duration_h,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
        self.speed = self.get_mean_speed()
        self.duration_m = self.duration_h * self.mins_in_hour

    def get_spent_calories(self) -> float:
        """Возвращает число потраченных калорий при беге."""        
        return((18 * self.speed - 20) * self.weight
                / self.M_IN_KM * self.duration_m)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.speed = self.get_mean_speed()
        self.duration_m = self.duration_h * self.mins_in_hour

    def get_spent_calories(self) -> float:
        return((0.035 * self.weight + (self.speed ** 2 // self.height)
                * 0.029 * self.weight) * self.duration_m)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
        
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.speed = self.get_mean_speed()

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration_h)
    
    def get_spent_calories(self) -> float:
        return (self.speed + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    sport_dict = {'SWM': Swimming,
                  'RUN': Running,
                  'WLK': SportsWalking}
    return sport_dict[workout_type](*data)


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
