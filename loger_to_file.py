from datetime import datetime

def loger_to_file(path='log.txt'):
    def decorator(func):
        def func_wraper(*args, **kwargs):
            resutl = func(*args, **kwargs)
            with open(path, mode='a', encoding='utf-8') as file:
                file.write(f'{datetime.now()}- name: {func.__name__}, args: {args}, kwargs: {kwargs}, result: {resutl}\n')
            return resutl
        return func_wraper
    return decorator
