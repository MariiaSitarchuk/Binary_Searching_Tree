"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log, log2
from datetime import datetime
import random


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1

            left_kid = top.left
            right_kid = top.right
            cur_height = max(height1(left_kid), height1(right_kid)) + 1

            return cur_height

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < log(self._size - 1) + 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        tree_list = list(self.inorder())
        result_arr = []

        for elem in tree_list:
            if elem >= low and elem <= high:
                result_arr.append(elem)

        return result_arr

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def recurse(tree_lst):
            """
            Helper recursive function to rebalance tree.
            """
            if len(tree_lst) == 1:
                return BSTNode(tree_lst[0])
            if len(tree_lst) < 1:
                return None

            mid_index = len(tree_lst) // 2

            root = BSTNode(tree_lst[mid_index])

            root.left = recurse(tree_lst[:mid_index])
            root.right = recurse(tree_lst[mid_index + 1:])

            return root

        tree_lst = list(self.inorder())
        balanced_root = recurse(tree_lst)
        self._root = balanced_root

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def recurse(item, root, target=None):
            """
            Helper recursive finction to find the smallest item,
            which is larger than given item.
            """
            if root.data <= item and root.right != None:
                return recurse(item, root.right, target)
            elif root.data > item and root.left != None:
                target = root
                return recurse(item, root.left, target)
            elif root.data <= item and root.right == None:
                if target != None:
                    return target.data
                else:
                    return target
            elif root.data > item and root.left == None:
                return root.data

        return recurse(item, self._root)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def recurse(item, root, target=None):
            """
            Helper recursive finction to find the smallest item,
            which is larger than given item.
            """
            if root.data < item and root.right != None:
                target = root
                return recurse(item, root.right, target)
            elif root.data >= item and root.left != None:
                return recurse(item, root.left, target)
            elif root.data >= item and root.left == None:
                if target != None:
                    return target.data
                else:
                    return target
            elif root.data < item and root.right == None:
                return root.data

        return recurse(item, self._root)

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        ---------------------------------------------------------------------
        Arguments:
            self - an object of class LinkedBST.
            path (str) - the path to file with words.
        ---------------------------------------------------------------------
        Return:
            1) time of searching 10.000 random words in vocabulary
               sorted by alphabet, using LIST methods.

            2) time of searching 10.000 random words in vocabulary
               as a binary search tree.
               BST is formed by adding words in it from the vocabulary,
               which is sorted by alphabet.

            3) time of searching 10.000 random words in vocabulary
               as a binary search tree.
               BST is formed by adding words in it from the vocabulary,
               which is not sorted by alphabet (words are added randomly).

            4) time of searching 10.000 random words in vocabulary
               as a binary search tree after its rebalancing.
        """
        that_string = ''

        with open(path, 'r') as file:
            for line in file:
                that_string += line.lower()

        all_words_list = that_string.split('\n')

        random_list = []
        that_list_copy = all_words_list.copy()

        # now it's 10000 - for words.txt
        # you can change it for example:
        # to 200 - for max_recursion.txt
        # to 7 - for some_text.txt
        while len(random_list) < 10000:
            value = random.choice(that_list_copy)
            index_v = that_list_copy.index(value)
            that_list_copy.pop(index_v)
            random_list.append(value)

        print('-----------------------------------------------')
        start_time = datetime.now()
        found_1 = self.first_time(random_list, all_words_list)
        end_time = datetime.now()
        print('Time for first search: {}'.format(end_time - start_time))
        print(f'Found: {found_1}')
        print('-----------------------------------------------')

        alphabet_tree = LinkedBST()

        for elem in all_words_list:
            alphabet_tree.add(elem)
        # print(alphabet_tree)

        start_time = datetime.now()
        found_2 = self.second_time(random_list, alphabet_tree)
        end_time = datetime.now()
        print('Time for second search: {}'.format(end_time - start_time))
        print(f'Found: {found_2}')
        print('-----------------------------------------------')

        not_alphabet_tree = LinkedBST()

        not_alph_words = all_words_list.copy()
        random.shuffle(not_alph_words)

        for item in not_alph_words:
            not_alphabet_tree.add(item)
        # print(not_alphabet_tree)

        start_time = datetime.now()
        found_3 = self.third_time(random_list, not_alphabet_tree)
        end_time = datetime.now()
        print('Time for third search: {}'.format(end_time - start_time))
        print(f'Found: {found_3}')
        print('-----------------------------------------------')

        not_alphabet_tree.rebalance()
        # print(not_alphabet_tree)

        start_time = datetime.now()
        found_4 = self.forth_time(random_list, not_alphabet_tree)
        end_time = datetime.now()
        print('Time for forth search: {}'.format(end_time - start_time))
        print(f'Found: {found_4}')
        print('-----------------------------------------------')

    def first_time(self, ran_lst, all_words_lst):
        """
        First demonstration of efficiency binary search tree for the search tasks.
        Searching using List methods.
        -----------------------------------------------------------------------------
        Arguments:
            self - an object of class LinkedBST.
            ran_lst (list) - a list with random 10.000 words to find.
            all_words_lst (list) - a list of all words from file.
        ---------------------------------------------------------------------
        Return:
            1) time of searching 10.000 random words in vocabulary
               sorted by alphabet, using LIST methods.
        """
        found = 0

        for elem in ran_lst:
            if elem in all_words_lst:
                found += 1

        return found
        

    def second_time(self, ran_lst, alph_tree):
        """
        Second demonstration of efficiency binary search tree for the search tasks.
        Searching in a binary tree, where elements were added
        one by one in alphabet order.
        -----------------------------------------------------------------------------
        Arguments:
            self - an object of class LinkedBST.
            ran_lst (list) - a list with random 10.000 words to find.
            alph_tree (LinkedBST) - a tree sorted by alphabet.
        ---------------------------------------------------------------------
        Return:
            2) time of searching 10.000 random words in vocabulary
               as a binary search tree.
               BST is formed by adding words in it from the vocabulary,
               which is sorted by alphabet.
        """
        def recurse(root, ran_lst):
            """
            Helper function with recursion.
            """
            if root.data in ran_lst:
                if root.right == None:
                    return 1
                else:
                    return recurse(root.right, ran_lst) + 1
            else:
                if root.right == None:
                    return 0
                else:
                    return recurse(root.right, ran_lst)

        return recurse(alph_tree._root, ran_lst)

    def third_time(self, ran_lst, not_alph_tree):
        """
        Third demonstration of efficiency binary search tree for the search tasks.
        Searching in a binary tree, where elements were added
        one by one not in alphabet order.
        -----------------------------------------------------------------------------
        Arguments:
            self - an object of class LinkedBST.
            ran_lst (list) - a list with random 10.000 words to find.
            not_alph_tree (LinkedBST) - a tree not sorted by alphabet.
        ---------------------------------------------------------------------
        Return:
            3) time of searching 10.000 random words in vocabulary
               as a binary search tree.
               BST is formed by adding words in it from the vocabulary,
               which is not sorted by alphabet (words are added randomly).
        """
        def recurse(root, ran_lst):
            """
            Helper function with recursion.
            """
            if root.data in ran_lst:
                if root.right == None and root.left == None:
                    return 1
                elif root.left == None:
                    return recurse(root.right, ran_lst) + 1
                elif root.right == None:
                    return recurse(root.left, ran_lst) + 1
                else:
                    right_kid = recurse(root.right, ran_lst)
                    left_kid = recurse(root.left, ran_lst)
                    return right_kid + left_kid + 1
            else:
                if root.right == None and root.left == None:
                    return 0
                elif root.left == None:
                    return recurse(root.right, ran_lst)
                elif root.right == None:
                    return recurse(root.left, ran_lst)
                else:
                    right_kid = recurse(root.right, ran_lst)
                    left_kid = recurse(root.left, ran_lst)
                    return right_kid + left_kid

        return recurse(not_alph_tree._root, ran_lst)

    def forth_time(self, ran_lst, balance_tree):
        """
        Forth demonstration of efficiency binary search tree for the search tasks.
        Searching in a rebalanced binary tree.
        -----------------------------------------------------------------------------
        Arguments:
            self - an object of class LinkedBST.
            ran_lst (list) - a list with random 10.000 words to find.
            balance_tree (LinkedBST) - a rebalanced tree.
        ---------------------------------------------------------------------
        Return:
            4) time of searching 10.000 random words in vocabulary
               as a binary search tree after its rebalancing.
        """
        def recurse(root, ran_lst):
            """
            Helper function with recursion.
            """
            if root.data in ran_lst:
                if root.right == None and root.left == None:
                    return 1
                elif root.left == None:
                    return recurse(root.right, ran_lst) + 1
                elif root.right == None:
                    return recurse(root.left, ran_lst) + 1
                else:
                    right_kid = recurse(root.right, ran_lst)
                    left_kid = recurse(root.left, ran_lst)
                    return right_kid + left_kid + 1
            else:
                if root.right == None and root.left == None:
                    return 0
                elif root.left == None:
                    return recurse(root.right, ran_lst)
                elif root.right == None:
                    return recurse(root.left, ran_lst)
                else:
                    right_kid = recurse(root.right, ran_lst)
                    left_kid = recurse(root.left, ran_lst)
                    return right_kid + left_kid

        return recurse(balance_tree._root, ran_lst)
