class PriorityLinkedList:

    def __init__(self):
        self.head = PriorityNode(999999,None)
        self.tail = PriorityNode(-99999,None)
        self.head.setNext(self.tail)
        self.tail.setPrev(self.head)

    def getHead(self):
        return self.head

    def getTail(self):
        return self.tail

    def insertWithPriority(self,node):
        current = self.head
        while(True):
            if current.priority < node.priority:
                prev=current.getPrev()
                prev.setNext(node)
                node.setPrev(prev)
                node.setNext(current)
                current.setPrev(node)
                break
            current=current.getNext()

    def __str__(self):
        strReturn = ''
        current = self.getHead().getNext()
        while(current != self.getTail()):
            strReturn = strReturn + str(current.getValue())+"("+str(current.getPriority())+") -> "
            current = current.getNext()
        return strReturn

class PriorityNode:

    def __init__(self,priority,value):
        self.priority = priority
        self.value = value
        self.prev = None
        self.next = None

    def getPrev(self):
        return self.prev

    def getNext(self):
        return self.next

    def setNext(self,node):
        self.next = node

    def setPrev(self,node):
        self.prev = node

    def getValue(self):
        return self.value

    def setValue(self,value):
        self.value = value

    def getPriority(self):
        return self.priority

if __name__ == "__main__":

    list = PriorityLinkedList()
    list.insertWithPriority(PriorityNode(100, 'a'))
    list.insertWithPriority(PriorityNode(100, 'b'))
    list.insertWithPriority(PriorityNode(90, 'c'))
    list.insertWithPriority(PriorityNode(80, 'd'))
    list.insertWithPriority(PriorityNode(110, 'e'))

    print(list)
