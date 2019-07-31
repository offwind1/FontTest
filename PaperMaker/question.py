class Question():
    QUESTION_MARGIN_NORMAL = (0, 0, 0, 0)

    def __init__(self, width):
        self.width = width
        self._margin = Question.QUESTION_MARGIN_NORMAL

    @property
    def top(self):
        return self._margin[0]

    @property
    def left(self):
        return self._margin[1]

    @property
    def down(self):
        return self._margin[2]

    @property
    def right(self):
        return self._margin[3]
