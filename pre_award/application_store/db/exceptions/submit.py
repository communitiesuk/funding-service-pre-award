class SubmitError(Exception):
    def __init__(self, application_id, *args):
        super().__init__(*args)
        self.application_id = application_id

    def __str__(self):
        return f"Unable to submit application [{self.application_id}]. Cause {self.__cause__}"
