"""
UMass ECE 241 - Advanced Programming
Project #1   Fall 2021
project1.py - Sorting and Searching
"""
from pathlib import Path
#import matplotlib.pyplot as plt



"""
Stock class for stock objects
"""
class Stock:

    """
    Constructor to initialize the stock object
    """
    def __init__(self, sname, symbol, val, prices):
        self.sname = sname
        self.symbol = symbol
        self.val = val
        self.prices = prices
        pass

    """
    return the stock information as a string, including name, symbol, 
    market value, and the price on the last day (2021-02-01). 
    For example, the string of the first stock should be returned as: 
    “name: Exxon Mobil Corporation; symbol: XOM; val: 384845.80; price:44.84”. 
    """
    def __str__(self):
        return "name: " + self.sname + "; symbol: " + self.symbol + "; val: " + str(self.val) + "; price: " + str(self.prices[-1])
        pass

class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None,balanceFactor = 0):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.balanceFactor = balanceFactor

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1

    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if current.Node.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)
                self.updateBalance(currentNode.leftChild)
        else:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)
                self.updateBalance(currentNode.rightChild)

    def updateBalance(self, node):
        if node.balanceFactor > 1 or node.balanceFactor < -1:
            self.rebalance(node)
            return
        if node.parent != None:
            if node.isLeftChild():
                node.parent.balancefactor += 1
            elif node.isRightChild():
                node.parent.balanceFactor -= 1

            if node.parent.balanceFactor != 0:
                self.updateBalance(node.parent)

    def rotateLeft(self, rotRoot):
        newRoot = rotRoot.rightChild
        rotRoot.rightChild = newRoot.leftChild
        if newRoot.leftChild != None:
            newRoot.leftChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot
        newRoot.leftChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor + 1 - min(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor + 1 + max(rotRoot.balanceFactor, 0)

    def rotateRight(self, rotRoot):
        newRoot = rotRoot.leftChild
        rotRoot.leftChild = newRoot.rightChild
        if newRoot.rightChild != None:
            newRoot.rightChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isRightChild():
                rotRoot.parent.rightChild = newRoot
            else:
                rotRoot.parent.leftChild = newRoot
        newRoot.rightChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor + 1 - min(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.blanceFactor + 1 + max(rotRoot.balanceFactor, 0)

    def rebalance(self, node):
        if node.balanceFactor < 0:
            if node.rightChild.balanceFactor > 0:
                self.rotateRight(node.rightChild)
                self.rotateLeft(node)
            else:
                self.rotateLeft(node)
        elif node.balanceFactor > 0:
            if node.leftChild.balanceFactor < 0:
                self.rotateLeft(node.leftchilc)
                self.rotateRight(node)
            else:
                self.rotateRight(node)
"""
StockLibrary class to mange stock objects
"""
class StockLibrary:
    """
    Constructor to initialize the StockLibrary
    """
    def __init__(self, stockList=None, size=None, isSorted=False, bst=None,left = None, right=None):
        self.stockList = stockList
        self.size = size
        self.isSorted = isSorted
        self.bst = bst
        pass
    """
    The loadData method takes the file name of the input dataset,
    and stores the data of stocks into the library. 
    Make sure the order of the stocks is the same as the one in the input file. 
    """
    def loadData(self, filename: str):
        stockList = []
        file = open(Path(filename),'r')
        lines = file.readlines()[1:]
        for line in lines:  # for each stock break at line
            stockdetails = line.split('|') # split at every |
            sname = stockdetails[0]
            symbol = stockdetails[1]
            val = stockdetails[2]
            prices_raw = stockdetails[3:]
            prices = []
            for price in prices_raw:
                prices.append(price.strip("'"))

            new_stock = Stock(sname,symbol,val,prices)
            stockList.append(new_stock)
        self.stockList = stockList
        self.size = len(stockList)
        self.isSorted = False
        pass
    """
    The linearSearch method searches the stocks based on sname or symbol.
    It takes two arguments as the string for search and an attribute field 
    that we want to search (“name” or “symbol”). 
    It returns the details of the stock as described in __str__() function 
    or a “Stock not found” message when there is no match. 
    """
    def linearSearch(self, query: str, attribute: str):
        if query == testName:
            stock = 0
            found = False
            while stock != self.size-1 and not found:
                if self.stockList[stock].sname == attribute:
                    found = True
                else:
                    stock = stock+1
            if found == True:
                return self.stockList[stock]
            else:
                return "Stock not found"

        if query == testSymbol:
            stock = 0
            found = False
            while stock != self.size - 1 and not found:
                if self.stockList[stock].symbol == attribute:
                    found = True
                else:
                    stock = stock + 1
            if found == True:
                return self.stockList[stock]
            else:
                return "Stock not found\n"
        pass

    def quickSortHelper(self,first,last):
        if first<last:
            splitpoint = StockLibrary.partition(self,first,last)
            StockLibrary.quickSortHelper(self,first,splitpoint-1)
            StockLibrary.quickSortHelper(self,splitpoint+1,last)
        pass

    def partition(self,first,last):
        pivot = self.stockList[first].symbol

        leftmark = first +1
        rightmark = last

        sorted = False
        while not sorted:
            while leftmark <= rightmark and self.stockList[leftmark].symbol <= pivot:
                leftmark = leftmark + 1
            while rightmark >= leftmark and self.stockList[rightmark].symbol >= pivot:
                rightmark = rightmark - 1
            if rightmark < leftmark:
                sorted = True
            else:
                temp = self.stockList[leftmark]
                self.stockList[leftmark] = self.stockList[rightmark]
                self.stockList[rightmark] = temp
        temp = self.stockList[first]
        self.stockList[first] = self.stockList[rightmark]
        self.stockList[rightmark] = temp
        return rightmark
    """
    Sort the stockList using QuickSort algorithm based on the stock symbol.
    The sorted array should be stored in the same stockList.
    Remember to change the isSorted variable after sorted
    """
    def quickSort(self):
        StockLibrary.quickSortHelper(self,0, len(self.stockList) - 1)
        self.isSorted = True
    """
    
    build a balanced BST of the stocks based on the symbol. 
    Store the root of the BST as attribute bst, which is a TreeNode type.
    """

    def buildBST(self):
        BST = BinarySearchTree()
        for stock in range(0,len(self.stockList)):
            BST.put(self.stockList[stock].symbol,self.stockList[stock])
            self.bst = BST.root
        return "Built"

    def get(self, key):
        if self.bst:
            res = self._get(key, self.bst)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    """
    Search a stock based on the symbol attribute. 
    It returns the details of the stock as described in __str__() function 
    or a “Stock not found” message when there is no match. 
    """
    def searchBST(self, query, current='dnode'):
        if query == testSymbol and self.get(testSymbol) != None:
            return self.get(testSymbol)
        else:
            return "Stock not found"
        pass



# WRITE YOUR OWN TEST UNDER THIS IF YOU NEED


if __name__ == '__main__':

    stockLib = StockLibrary()

    testSymbol = 'GME'
    testName = 'General Electric Company'


    print("\n-------load dataset-------")
    stockLib.loadData("stock_database.csv")
    print(stockLib.size)


    print("\n-------linear search-------")
    print(stockLib.linearSearch(testSymbol, "GME"))
    print(stockLib.linearSearch(testName, "Black Hills Corporation"))


    print("\n-------quick sort-------")
    print(stockLib.isSorted)
    stockLib.quickSort()
    print(stockLib.isSorted)


    print("\n-------build BST-------")
    print(stockLib.buildBST())

    print("\n---------search BST---------")
    print(stockLib.searchBST(testSymbol))