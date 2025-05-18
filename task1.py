def strict(func):
    def wrapper(*args, **kwargs):
        # Получаем аннотации типов параметров функции
        annotations = func.__annotations__

        # Проверяем позиционные аргументы
        for arg_name, arg_value in zip(annotations.keys(), args):
            if arg_name in annotations:
                expected_type = annotations[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Argument '{arg_name}' must be of type "
                        f"{expected_type.__name__}, "
                        f"not {type(arg_value).__name__}"
                    )

        # Проверяем именованные аргументы
        for arg_name, arg_value in kwargs.items():
            if arg_name in annotations:
                expected_type = annotations[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(
                        f"Argument '{arg_name}' must be of type "
                        f"{expected_type.__name__}, "
                        f"not {type(arg_value).__name__}"
                    )

        # Вызываем исходную функцию
        return func(*args, **kwargs)

    return wrapper
