class TaskResult:

    def __init__(self) -> None:
        # result
        self._result_bool = None
        self._result_msg = None
        self._result_args = None

    def insert_result(self, result_bool, result_msg, result_args):
        self._result_bool = result_bool
        self._result_msg = result_msg
        self._result_args = result_args

    def take_report(self):
        result_bool = self._result_bool
        result_msg = self._result_msg
        result_args = self._result_args

        return result_bool, result_msg, result_args