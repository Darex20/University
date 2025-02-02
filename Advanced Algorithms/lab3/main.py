from abc import ABC, abstractmethod
from typing import Optional
from enum import Enum


class Color(Enum):
    """
    Enumeration represeting the different possible colors of a node in a Red-Black.

    ...

    Values
    ------

    Color.Red: int
        Indicates a node of red color.
    Color.Black: int
        Indicates a node of red color.
    """

    Red = 0
    Black = 1


class RBNodeBase(ABC):
    """Base class for Red-Black tree nodes containing integer values.

    ...

    Attributes
    ----------

    value: int
        Value stored in the node.
    parent: RBNodeBase, optional
        Parent of the current node. Can be None.

    Properties
    ----------

    left: RBNodeBase, optional:
        Left child of the current node. Can be None or SENTINEL.
    right: RBNodeBase, optional:
        Right child of the current node. Can be None or SENTINEL.
    color: Color
        The color of the RB node. Can be Color.Black or Color.Red.
    """

    def __init__(self, value: int) -> None:
        self.value = value
        self.parent = None

    @property
    @abstractmethod
    def left(self) -> Optional["RBNodeBase"]:
        """The left child of the current node. Can be None."""
        pass

    @left.setter
    @abstractmethod
    def left(self, node: Optional["RBNodeBase"]) -> None:
        pass

    @property
    @abstractmethod
    def right(self) -> Optional["RBNodeBase"]:
        """The right child of the current node. Can be None."""
        pass

    @right.setter
    @abstractmethod
    def right(self, node: Optional["RBNodeBase"]) -> None:
        pass

    def set_left_child(self, node: Optional["RBNodeBase"]) -> None:
        """Set the left child of self to the given node.

        Sets the node's parent to self (if the node is not None).

        Args:
            node (RBNodeBase, optional): The node to set as the child.
        """
        self.left = node
        if node is not None:
            node.parent = self

    def set_right_child(self, node: Optional["RBNodeBase"]) -> None:
        """Set the right child of self to the given node.

        Sets the node's parent to self (if the node is not None).

        Args:
            node (RBNodeBase, optional): The node to set as the child.
        """
        self.right = node
        if node is not None:
            node.parent = self

    def replace_child(
        self, node: Optional["RBNodeBase"], replacement: "RBNodeBase"
    ) -> None:
        """Replace the specified node with the given replacement.

        Does nothing if the node is not a child of self.

        Args:
            node (RBNodeBase, optional): The node to be replaced.
            replacement (RBNodeBase, optional): The replacement node.
        """
        if self.left is node:
            self.set_left_child(replacement)
        elif self.right is node:
            self.set_right_child(replacement)

    @property
    @abstractmethod
    def color(self) -> Color:
        """The color of the node. Either Color.Black or Color.Red."""
        pass

    @color.setter
    @abstractmethod
    def color(self, color_value) -> None:
        pass


class SentinelChildError(Exception):
    """Exception which is raised when a child is set to a SENTINEL object.

    ...

    Attributes
    ----------
    node: RBNodeBase, optional:
        The node to be set as the child of a SENTINEL.
    """

    def __init__(self, sentinel, node):
        super().__init__(
            f"Pokusali ste postaviti dijete SENTINEL objektu, dijete: {node}, roditelj SENTINEL objekta: {sentinel.parent}"
        )
        self.node = node


class RBSentinel(RBNodeBase):
    """Class representing a NIL/NULL node in a Red-Black tree.

    All attributes inherited from RBNodeBase.

    ...

    Properties
    ----------
    color: Color
        Always returns Color.Black
    left: RBNodeBase, optional:
        Always returns None. Raises SentinelChildError if set.
    right: RBNodeBase, optional:
        Always returns None. Raises SentinelChildError if set.
    """

    def __init__(self) -> None:
        super().__init__(0)

    @property
    def color(self):
        return Color.Black

    @color.setter
    def color(self, color_value) -> None:
        pass

    @property
    def left(self) -> Optional[RBNodeBase]:
        return None

    @left.setter
    def left(self, node: Optional[RBNodeBase]) -> None:
        raise SentinelChildError(self, node)

    @property
    def right(self) -> Optional[RBNodeBase]:
        return None

    @right.setter
    def right(self, node: Optional[RBNodeBase]) -> None:
        raise SentinelChildError(self, node)

    def __bool__(self) -> bool:
        """Bool conversion operator for the NIL/NULL nodes.

        Always returns False.

        ...

        Usage
        -----

        'if not node:' -> Checks if the node is None or SENTINEL.
        """
        return False

    def __repr__(self) -> str:
        """String representation of sentinel (NIL/NULL) nodes."""
        return "SENTINEL"


SENTINEL = RBSentinel()


class RBNode(RBNodeBase):
    """Class representing a regular Red-Black tree node.

    Can have a left and right child unlike the SENTINEL node.

    ...

    Properties and attributes inherited from RBNodeBase.
    """

    def __init__(self, value: int, color: Color = Color.Red) -> None:
        super().__init__(value)
        self._color = color
        self._left = self._right = SENTINEL

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color_value: Color):
        self._color = color_value

    @property
    def left(self) -> Optional[RBNodeBase]:
        return self._left

    @left.setter
    def left(self, node: Optional[RBNodeBase]) -> None:
        self._left = node

    @property
    def right(self) -> Optional[RBNodeBase]:
        return self._right

    @right.setter
    def right(self, node: Optional[RBNodeBase]) -> None:
        self._right = node

    def __repr__(self) -> str:
        return f"RBNode({self.value}, {self.color})"


def _left_rotation_impl(rotatee: RBNode, rotator: RBNode) -> None:
    """
    Private static helper method for swapping the children of the rotatee and rotator.
    Specifically for left rotation.

    Args:
        rotatee (AVLNode, optional): The node around which we rotate (parent).

        rotator (AVLNode, optional): The node with which we rotate around the rotatee (child).
    """
    temp = rotator.left
    rotator.set_left_child(rotatee)
    rotatee.set_right_child(temp)


def _right_rotation_impl(rotatee: RBNode, rotator: RBNode) -> None:
    """
    Private static helper method for swapping the children of the rotatee and rotator.
    Specifically for right rotation.

    Args:
        rotatee (AVLNode, optional): The node around which we rotate (parent).
        rotator (AVLNode, optional): The node with which we rotate around the rotatee (child).
    """
    temp = rotator.right
    rotator.set_right_child(rotatee)
    rotatee.set_left_child(temp)


class RotationType(Enum):
    """
    Helper enum for types of rotation.
    The enum values are actually references to functions implementing rotations.
    """

    Left = _left_rotation_impl
    Right = _right_rotation_impl


class RBTree:
    """Class representing a Red-Black tree.

    ...

    Attributes
    ----------

    root: RBNodeBase, optional
        The root node of the Red-Black tree. Can be a SENTINEL.
    """

    def __init__(self, root: Optional[RBNodeBase] = SENTINEL) -> None:
        if root is None:
            root = SENTINEL
        self.root = root

    def set_root(self, root: Optional[RBNodeBase]) -> None:
        """Set the root node of this tree to the specified node and set its parent to None.

        Args:
            root (RBNodeBase, optional): The node to be set as the root.
        """
        if root is None:
            root = SENTINEL
        self.root = root
        self.root.parent = None

    @staticmethod
    def swap_colors(node_a: RBNodeBase, node_b: RBNodeBase) -> None:
        """Swap the colors of two nodes.

        Args:
            node_a (RBNodeBase): The first node.
            node_b (RBNodeBase): The second node.
        """
        if node_a is None or node_b is None:
            return
        temp = node_a.color
        node_a.color = node_b.color
        node_b.color = temp

    def rotate(
        self, rotatee: RBNodeBase, rotator: RBNodeBase, rotation: RotationType
    ) -> None:
        """Rotate the rotator around the rotatee using the specified rotation.

        Will not rotate if:
            - Any of the arguments is None
            - Any of the node arguments (rotatee, rotator) is a SENTINEL

        Args:
            rotatee (RBNodeBase, optional) : The node around which we rotate (parent).
            rotator (RBNodeBase, optional) : The node which we rotate around the rotatee (child).
            rotate (RotationType): The type of rotation to perform. Can be RotationType.Left or RotationType.Right.
        """
        if not (rotatee and rotator and rotation):
            return

        if rotator.parent is not rotatee:
            return

        parent = rotatee.parent
        if not parent:
            self.set_root(rotator)
        else:
            parent.replace_child(rotatee, rotator)
        rotation(rotatee, rotator)

    def insert_rebalance(self, node: Optional[RBNodeBase], node_is_left: bool) -> None:
        """Rebalance the Red-Black tree after inserting a new value.

        A recursive implementation of rebalancing nodes after inserting into the Red-Black tree.
        If the node has no parent (we are in the root) paints it to Color.Black and ignores the second argument.

        Does nothing on None or SENTINEL nodes.

        Args:
            node (RBNode): The node from which we start the rebalancing.
            node_is_left (bool): True if the node from which we start is on the left side of its parent. Otherwise False.
        """
        if not node:
            return

        if not node.parent:
            node.color = Color.Black
            return

        parent = node.parent
        grandparent = parent.parent
        if not grandparent or parent.color is not Color.Red:
            return

        parent_is_left = False
        uncle = grandparent.left
        if parent is grandparent.left:
            uncle = grandparent.right
            parent_is_left = True

        if uncle.color is Color.Red:
            red_uncle_case(self, node, parent, uncle, grandparent)
        else:
            if parent_is_left == node_is_left:
                straight_case(self, node, parent, uncle, grandparent)
            else:
                broken_case(self, node, parent, uncle, grandparent)

    def insert(self, value: int) -> bool:
        """Insert the given value into the Red-Black tree.

        Args:
            value (int): The value to insert.

        Returns:
            bool: True if the insert was successful. Otherwise False.
        """
        if not value:
            return False

        if not self.root:
            self.set_root(RBNode(value, Color.Black))
            return True

        node, parent = self.root, SENTINEL
        is_left = True
        while node:
            if value < node.value:
                parent = node
                node = node.left
                is_left = True
            elif value > node.value:
                parent = node
                node = node.right
                is_left = False
            else:
                return False
        new_node = RBNode(value, Color.Red)
        if is_left:
            parent.set_left_child(new_node)
        else:
            parent.set_right_child(new_node)

        self.insert_rebalance(new_node, is_left)
        return True


def red_uncle_case(
    tree: RBTree,
    node: RBNodeBase,
    parent: RBNodeBase,
    uncle: RBNodeBase,
    grandparent: RBNodeBase
) -> None:
    """Implements the insert rebalancing case when the uncle of the node is red.

    Args:
        tree (RBTree): The tree we are rebalancing.
        node (RBNodeBase): The node on which we are currently rebalancing.
        parent (RBNodeBase): The parent of the node we are currently rebalancing, i.e. node.parent.
        uncle (RBNodeBase): The uncle of the node we are currently rebalancing.
        grandparent (RBNodeBase, optional): The grandparent node of the node we are currently rebalancing, i.e. node.parent.parent. Can be None.
    """
    # TODO: Implementirati slučaj kada je ujak čvora crven i po potrebi pozvati ponovno 'insert_rebalance' metodu iz RBTree klase.
    grandparent.color = Color.Red
    parent.color = Color.Black
    uncle.color = Color.Black
    if grandparent and grandparent.parent and grandparent.parent.left == grandparent:
        tree.insert_rebalance(grandparent, True)
    else:
        tree.insert_rebalance(grandparent, False)
    

def straight_case(
    tree: RBTree,
    node: RBNodeBase,
    parent: RBNodeBase,
    uncle: RBNodeBase,
    grandparent: RBNodeBase
) -> None:
    """Implements the insert rebalancing case when the uncle of the node is black and we have a straight case (the node and parent are 'in a line', i.e. both on the left or right of their parents).

    Args:
        tree (RBTree): The tree we are rebalancing.
        node (RBNodeBase): The node on which we are currently rebalancing.
        parent (RBNodeBase): The parent of the node we are currently rebalancing, i.e. node.parent.
        uncle (RBNodeBase): The uncle of the node we are currently rebalancing.
        grandparent (RBNodeBase, optional): The grandparent node of the node we are currently rebalancing, i.e. node.parent.parent. Can be None.
    """
    # TODO: Implementirati ulančani slučaj sa crnim ujakom i po potrebi pozvati ponovno 'insert_rebalance' metodu iz RBTree klase.
    if grandparent and parent:
        if parent and parent.parent and parent.parent.left == parent:
            tree.rotate(grandparent, parent, RotationType.Right)
        else:
            tree.rotate(grandparent, parent, RotationType.Left)
        tree.swap_colors(parent, grandparent)
    if node and node.parent and node.parent.left:
        tree.insert_rebalance(node, True)
    else:
        tree.insert_rebalance(node, False)

    
def broken_case(
    tree: RBTree,
    node: RBNodeBase,
    parent: RBNodeBase,
    uncle: RBNodeBase,
    grandparent: RBNodeBase
) -> None:
    """Implements the insert rebalancing case when the uncle of the node is black and we have a broken case (the node and parent are NOT 'in a line', i.e. the parent is on the left of the grandparent and the node is on the right of the parent).

    Args:
        tree (RBTree): The tree we are rebalancing.
        node (RBNodeBase): The node on which we are currently rebalancing.
        parent (RBNodeBase): The parent of the node we are currently rebalancing, i.e. node.parent.
        uncle (RBNodeBase): The uncle of the node we are currently rebalancing.
        grandparent (RBNodeBase, optional): The grandparent node of the node we are currently rebalancing, i.e. node.parent.parent. Can be None.
    """
    # TODO: Implementirati razlomljeni slučaj sa crnim ujakom i po potrebi pozvati ponovno 'insert_rebalance' metodu iz RBTree klase.
    if grandparent:
        if parent and parent.left == node:
            tree.rotate(parent, node, RotationType.Right)
        else:
            tree.rotate(parent, node, RotationType.Left)
    if parent.parent and parent.parent.left == parent:
        tree.insert_rebalance(parent, True)
    else:
        tree.insert_rebalance(parent, False)


def _validate_node_ancestry(node: RBNodeBase) -> None:
    """Raises a RecursionError if the specified node is its own parent or child.

    Args:
        node (RBNodeBase): The node which we are validating.

    Raises:
        RecursionError: If node.parent, node.left or node.right is node.
    """
    if node.left is node or node.right is node:
        raise RecursionError(f"A node is its own child: {node} - Infinite recursion!")

    if node.parent is node:
        raise RecursionError(f"A node is its own parent: {node} - Infinite recursion!")

def black_height(node: Optional[RBNodeBase]) -> int:
    """Calculate the black height of the subtree rooted at the specified node.

    Args:
        node (RBNodeBase, optional): The root of the subtree for which we calculate the black height.
    
    Returns:
        int: 0 if the node is None or SENTINEL. Otherwise the height of the subtree.

    Raises:
        RecursionError: If the node is its own parent or child.
    """
    if not node:
        return 0
    _validate_node_ancestry(node)
    
    return max(black_height(node.left), black_height(node.right)) + int(
        node.color is Color.Black
    )


def is_valid_rb_subtree(node: Optional[RBNodeBase]) -> bool:
    """Check if the subtree rooted at the specified node is a valid Red-black subtree.

    Args:
        node (RBNodeBase, optional): The root of the Red-Black subtree.
    
    Returns:
        bool: True if the node is None, SENTINEL or adheres to the rules of Red-Black trees. Otherwise False. 

    Raises:
        RecursionError: If the node is its own parent or child.
    """
    if not node:
        return True
    _validate_node_ancestry(node)

    if node.color is Color.Red and (
        node.left.color,
        node.right.color,
        node.parent.color,
    ) != (Color.Black, Color.Black, Color.Black):
        return False

    if node.left is not SENTINEL and node.value < node.left.value:
        return False

    if node.right is not SENTINEL and node.value > node.right.value:
        return False

    return is_valid_rb_subtree(node.left) and is_valid_rb_subtree(node.right)


###############################

def _validate_node_ancestry(node: RBNodeBase) -> None:
    """Raises a RecursionError if the specified node is its own parent or child.

    Args:
        node (RBNodeBase): The node which we are validating.

    Raises:
        RecursionError: If node.parent, node.left or node.right is node.
    """
    if node.left is node or node.right is node:
        raise RecursionError(f"A node is its own child: {node} - Infinite recursion!")

    if node.parent is node:
        raise RecursionError(f"A node is its own parent: {node} - Infinite recursion!")

def black_height(node: Optional[RBNodeBase]) -> int:
    """Calculate the black height of the subtree rooted at the specified node.

    Args:
        node (RBNodeBase, optional): The root of the subtree for which we calculate the black height.
    
    Returns:
        int: 0 if the node is None or SENTINEL. Otherwise the height of the subtree.

    Raises:
        RecursionError: If the node is its own parent or child.
    """
    if not node:
        return 0
    _validate_node_ancestry(node)
    
    return max(black_height(node.left), black_height(node.right)) + int(
        node.color is Color.Black
    )


def is_valid_rb_subtree(node: Optional[RBNodeBase]) -> bool:
    """Check if the subtree rooted at the specified node is a valid Red-black subtree.

    Args:
        node (RBNodeBase, optional): The root of the Red-Black subtree.
    
    Returns:
        bool: True if the node is None, SENTINEL or adheres to the rules of Red-Black trees. Otherwise False. 

    Raises:
        RecursionError: If the node is its own parent or child.
    """
    if not node:
        return True
    _validate_node_ancestry(node)

    if node.color is Color.Red and (
        node.left.color,
        node.right.color,
        node.parent.color,
    ) != (Color.Black, Color.Black, Color.Black):
        return False

    if node.left is not SENTINEL and node.value < node.left.value:
        return False

    if node.right is not SENTINEL and node.value > node.right.value:
        return False

    return is_valid_rb_subtree(node.left) and is_valid_rb_subtree(node.right)


def is_valid_rb_tree(tree: Optional[RBTree]) -> bool:
    """Check if the specified Red-Black tree is valid.
    
    Args:
        tree: (RBTree, optional): The Red-Black tree object to check.
    
    Returns:
        bool: True if the tree is a valid Red-Black tree (adheres to the rules of Red-Black trees). Otherwise False.

    Raises:
        RecursionError: If any of the nodes are their own parents or children.
    """
    if tree is None:
        return False
    if tree.root.color is not Color.Black:
        return False
    return is_valid_rb_subtree(tree.root) and black_height(
        tree.root.left
    ) == black_height(tree.root.right)

def test_random_values():
    import random
    tree = RBTree()
    values = random.sample(range(1, 100), k=12)
    print(f'Testiram za vrijednosti: {values}')
    for value in values:
        print(f'\tUnosim {value}')
        tree.insert(value)
        assert is_valid_rb_tree(tree)
        
test_random_values()