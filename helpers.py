import json
import time


def load_json(json_path=None):
    with open(json_path) as json_file:
        dic = json.load(json_file)
        return dic


def keep_trying(exceptions, n_attempts=3):
    """
    Retry decorator
    Retries the wrapped function/method attempts` times if the exceptions listed
    in ``exceptions`` are thrown
    :param exceptions: Lists of exceptions that trigger a keepTrying attempt
    :types Exceptions: Tuple of Exceptions
    :param n_attempts: The number of times to repeat the wrapped function/method
    :types times: Int
    """

    def decorator(func):
        def newfn(*args, **kwargs):
            attempts = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if type(e) in exceptions:
                        if attempts >=n_attempts:
                            print(f"Exception of type {type(e)} was raised in {str(func)}. Retrying...")
                            attempts +=1
                            time.sleep(1)
                        else:
                            print(f"Raising exception after {n_attempts} attempts")
                            raise(e)
                    else:
                        print(f"Exception of type {type(e)} not handled by {str(func)}")
                        raise (e)
            return func(*args, **kwargs)

        return newfn

    return decorator
