import random



class Span:
    def __init__(self, name, trace_id=None, parent_id=None, timestamp=None, annotations=[], binary_annotations=[], span_id=None):
        self.name = name
        self.trace_id = trace_id or self._generate_id()
        self.span_id = span_id or self._generate_id()
        self.parent_id = parent_id
        self.timestamp = timestamp
        self.binary_annotations = binary_annotations
        self.annotations = annotations

    @staticmethod
    def _generate_id():
        return random.randrange(0, 2 ** 31 - 1)
    