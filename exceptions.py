"""Public errors, exceptions, & warnings.

Classes:
EquityTypeMismatchError -- equity_value does not match Equity subclass.

"""

class EquityTypeMismatchError(ValueError):
    """Exception raised when equity_type attribute does not match type
    implied by specific Equity subclass.

    """

    def __init__(self, message=None, class_instance=None):
        self._message = message
        self._class_instance = class_instance

    def __str__(self) -> str:
        if self._message is not None:
            return self._message
        else:
            if self._class_instance is None:
                self._message = 'Inappropriate equity_type value for' \
                                'this subclass.'
            else:
                _class_name = type(self._class_instance).__name__
                self._message = f"For Equity subclass of type" \
                                f"{_class_name}, equity_value must be" \
                                f"'{_class_name.lower()}'"

