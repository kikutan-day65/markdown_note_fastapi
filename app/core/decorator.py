import functools


def transactional(func):
    @functools.wraps(func)
    def _wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            self.uow.commit()
            print(f"COMMIT: {func.__qualname__}")
            return result

        except Exception:
            self.uow.rollback()
            print(f"ROLLBACK: {func.__qualname__}")
            raise

    return _wrapper
