import Queue


class DataSource:

    def __init__(self):
        pass

    def save(self, processor):
        pass


class Processor:

    def __init__(self):
        self.next_processor = None

    def process(self, item):
        pass

    def process_next(self, item):
        if self.next_processor is not None:
            self.next_processor.process(item)


class Chain(Processor):

    def __init__(self):
        Processor.__init__(self)
        self.processes = []
        pass

    def add(self, processor):
        if len(self.processes) > 0:
            self.processes[-1].next_processor = processor
        self.processes.append(processor)
        return self

    def process(self, item):
        self.processes[0].process(item)


class Flow:

    def __init__(self):
        pass

    def run(self):
        pass

