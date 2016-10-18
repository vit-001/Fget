__author__ = 'Nikitin'

class HistoryRecord():
    def __init__(self, data=None, context=None):
        self.data = data
        self.context = context

    def __repr__(self, *args, **kwargs):
        return self.data.__repr__()

    def __eq__(self, hr2):
        return hr2.data==self.data


class HistoryException(Exception):
    pass

class History():
    def __init__(self,on_history_changed=lambda:None):
        self.history = list()
        self.handler=on_history_changed

    def put(self, record=HistoryRecord()):
        self.history.append(record)
        self.handler()

    def pop(self):
        if len(self.history) == 0:
            raise HistoryException()
        self.handler()
        return self.history.pop()

    def get_last_data(self,items=10):
        result=list()
        for item in self.history[-items:]:
            result.append(item.data)

        return result



if __name__ == "__main__":
    h = History()
    h.put(HistoryRecord('1'))
    h.put(HistoryRecord('2'))
    h.put(HistoryRecord('3'))
    h.put(HistoryRecord('4'))

    print(h.get_last_data(3))

    print(h.pop())
    print(h.pop())
    print(h.pop())
    print(h.pop())