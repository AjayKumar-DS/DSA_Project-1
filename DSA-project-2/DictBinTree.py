class BinNode:
    def __init__(self,k):
        self.k=k
        self.left=None
        self.right=None
        self.parent=None
        
        

class DictBinTree:
    def __init__(self):
        self.root=None
    
    def search_node(self,node,k):
        if node is None or k==node.k:
            return node
        elif k < node.k:
            return self.search_node(node.left,k)
        else:
            return self.search_node(node.right,k)
    
    def search(self,k):
        if self.search_node(self.root,k) is not None:
            return True
        else:
            return False
        
        #return self._search(self.root, k) is not None # or we could just use this line instead of if condition
    
    def insert(self,k):
        x=self.root
        y=None
        z=BinNode(k)

        while x is not None:
            y=x
            if z.k < x.k:
                x=x.left
            else:
                x=x.right
        
        z.parent=y

        if y is None:
            self.root=z
        elif z.k < y.k:
            y.left=z
        else:
            y.right = z

    def inorder(self,node,result):
        if node is not None:
            self.inorder(node.left,result)
            result.append(node.k)
            self.inorder(node.right,result)
    
    def orderedTraversal(self):
        result=[]
        self.inorder(self.root,result)
        return result