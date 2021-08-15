import sys
import numpy as np

class Node:
    def __init__(self,value,priority,blnDigit,blnTop=False):
        self.value = value
        self.priority = priority
        self.blnDigit = blnDigit
        self.blnTop = blnTop
        self.next = None
        self.left = None
        self.right = None
    def isDigit(self):
        return self.blnDigit
    def getRight(self):
        return self.right
    def getLeft(self):
        return self.left
    def setRight(self,node):
        self.right = node
    def setLeft(self,node):
        self.left = node
    def setNext(self,node):
        self.next = node
    def getNext(self):
        return self.next
    def getValue(self):
        return self.value
    def getPriority(self):
        return self.priority
    def isTop(self):
        return self.blnTop
    def getString(self,depth):
        ret = ""
        for itr in range(depth):
            ret = ret + "...."
        ret = ret + str( self.getValue() ) + "\n"
        if self.getLeft() != None:
            ret = ret + self.getLeft().getString(depth+1)
        if self.getRight() != None:
            ret = ret + self.getRight().getString(depth + 1)
        return ret

class Stack:
    def __init__(self):
        self.head = Node(None,-1,False,blnTop=True)
    def top(self):
        if self.head.getNext() != None:
            return self.head.getNext()
        return None
    def push(self,node):
        node.setNext(self.head.getNext())
        self.head.setNext(node)
    def pop(self):
        ret = self.head.getNext()
        if ret != None:
            self.head.setNext(ret.getNext())
        return ret
    def __str__(self):
        currentNode = self.head.getNext()
        ret = ""
        while currentNode != None:
            ret = str(currentNode.getValue()) + "," + ret
            currentNode = currentNode.getNext()
        return ret

class BinaryExpressionTree:

    priorities = {"+":1, "-":1, "*":2, "/":2, "^":3, "(":0}
    unaryPriority = 4

    def __init__(self,line):
        tokens = line.split(" ")
        self.stackOperator = Stack()
        self.stackOperand = Stack()
        self.root = self.buildTree(tokens)
        print("Tokens : "+str(tokens))
        print("Prefix : " + self.traversPreFix())
        print("Postfix : " + self.traversPostFix())

    def buildTree(self,tokens):
        prev=Node(None,0,False)
        for itr in range(len(tokens)):
            token = tokens[itr]
            node=Node(token,0,False)
            if token=='(':
                node.priority=0
                self.stackOperator.push(node)
            elif token==')':
                while self.stackOperator.top().value!='(':
                    self.mergeLastTwoOperand()
                self.stackOperator.pop()
                node.blnDigit=True
            elif self.isDigit(token):
                node.blnDigit=True
                self.stackOperand.push(node)
            elif prev.isDigit()==False:#unary operator
                node.priority=4
                self.stackOperator.push(node)
            else:
                node.priority=self.priorities[token]
                while self.stackOperator.top()!=None and self.stackOperator.top().getPriority()>=node.priority:
                    self.mergeLastTwoOperand()
                self.stackOperator.push(node)
            prev=node
            print("Step. " + str(itr + 1))
            print("Stack Operator : " + str(self.stackOperator))
            print("Stack Operand : " + str(self.stackOperand))
        while self.stackOperator.top() != None:
            self.mergeLastTwoOperand()
        return self.stackOperand.top()

    def evaluate(self, node = None):
        if node == None:
            node = self.root
        if node.getLeft() != None:
            valueLeft = self.evaluate(node.getLeft())
        if node.getRight() != None:
            valueRight = self.evaluate(node.getRight())
        if node.getLeft() != None and node.getRight() == None:#unary operator
            if node.getValue()=='-':
                return -valueLeft
            else:#ln
                return np.log(valueLeft)
            return node.getValue()
        elif node.getLeft() != None and node.getRight() != None:
            if node.getValue()=='+':
                return valueLeft+valueRight
            elif node.getValue()=='-':
                return valueLeft-valueRight
            elif node.getValue()=='*':
                return valueLeft*valueRight
            elif node.getValue()=='/':
                return valueLeft/valueRight
            else:
                return valueLeft**valueRight
        else:
            return float(node.getValue())

    def __str__(self):
        return self.root.getString(0)

    def traversPreFix(self,node=None):
        if node == None:
            node = self.root
        ret = ""
        ret+=node.getValue()
        if node.getLeft()!=None:
            ret+=self.traversPreFix(node.getLeft())
        if node.getRight()!=None:
            ret+=self.traversPreFix(node.getRight())
        return ret

    def traversPostFix(self,node=None):
        if node == None:
            node = self.root
        ret = ""
        if node.getLeft() != None:
            ret += self.traversPostFix(node.getLeft())
        if node.getRight() != None:
            ret += self.traversPostFix(node.getRight())
        ret += node.getValue()
        return ret

    def mergeLastTwoOperand(self):
        nodeOperator = self.stackOperator.pop()
        if nodeOperator.getPriority() == self.unaryPriority:
            nodeOperand=self.stackOperand.pop()
            nodeOperator.setLeft(nodeOperand)
        else:
            nodeOperand1=self.stackOperand.pop()
            nodeOperand2=self.stackOperand.pop()
            nodeOperator.setLeft(nodeOperand2)
            nodeOperator.setRight(nodeOperand1)
        self.stackOperand.push(nodeOperator)

    def isDigit(self,token):
        try:
            float(token)
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    line = input("Enter formula : ")
    # line = '3 + 5 - 2 * 7'
    # line = '3 + ( 5 - 2 ) * 7'
    # line = '- 3 + ( - ln 5 - 2 ) * 7'
    tree = BinaryExpressionTree(line)
    print ("Evaluate : "+str(tree.evaluate()))
    print ("Tree : \n"+str(tree))