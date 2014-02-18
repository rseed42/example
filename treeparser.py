""" A general parser for tree structures defined by indentation in a single file
    of the following (example) type:
    ====
    element1:value
    ..child1:value
    ....subchild1:value
    ....subchild2:value
    ..child2
    elementN
    ====
    The indentation character, number of indentation character per tree level,
    and the key-value separator are configurable.
    ====
    Desription: The parser reads a properly formatted tree sequentially and
    builds up a tree representation. It throws an exception if it encounters
    malformed indentation. It has to be tested more thoroughly, as it currently
    is used only in one project.
    ====
    TODO: Add tests
"""
#-------------------------------------------------------------------------------
DEFAULT_INDENT = ' '
DEFAULT_INDENT_COUNT = 2
DEFAULT_SEP = ' '
#-------------------------------------------------------------------------------
class InvalidIndentedTree(Exception):
    def __init__(self, msg):
        super(InvalidIndentedTree, self).__init__(msg)
#-------------------------------------------------------------------------------
# Tree Element
#-------------------------------------------------------------------------------
class TreeElement(list):
    def __init__(self, parent, name, value):
        self.parent = parent
        self.name = name
        self.value = value

    def __str__(self):
        return '{0} : {1}'.format(self.name, self.value)
#-------------------------------------------------------------------------------
# Parser
#-------------------------------------------------------------------------------
class IndentedKVTreeParser(object):
    """ Recursive parser for indented tree files
    """
    def __init__(self, indent=DEFAULT_INDENT, indent_count=DEFAULT_INDENT_COUNT,
                 kv_sep=DEFAULT_SEP):
        self.cue = {}
        self.indent = indent
        self.indent_count = indent_count
        self.kv_sep = kv_sep

    def read(self, treefile, parent, indent=0):
        """ treefile - a properly formatted file that contains a tree defined
            by indentation where each line consists of a single key-value pair.
        """
        next_level = indent + self.indent_count
        while True:
            line = treefile.next().strip('\r\n')
            ln = line.lstrip(self.indent)
            # Easier than using a regex
            level = len(line) - len(ln)
            name, value = ln.split(self.kv_sep, 1)
            # We are finished on this level
            if level < indent:
                element = TreeElement(parent.parent, name, value)
                parent.parent.append(element)
                break
            # We need to dive into the next level
            if level == next_level:
                # If the parent has no children, then we have an error in the
                # cue file (maybe add a counter for the exception)
                try:
                    element = TreeElement(parent[-1], name, value)
                    parent[-1].append(element)
                except KeyError:
                    raise InvalidIndentedTree(line)
                self.read(treefile, parent[-1], indent=next_level)
                continue
            # Potential error (malformed cue file), raise exception
            if level > next_level:
                raise InvalidIndentedTree(line)
            element = TreeElement(parent, name, value)
            parent.append(element)

    def parse(self, filename):
        """ Construct a tree of TreeElement objects that represents
            the file.
        """
        with file(filename, 'r') as treefile:
            # Think about the exception: is this the right location?
            # What if a child element craps up?
            root = TreeElement(None, 'root', 'element')
            try:
                self.read(treefile, root, indent=0)
            except StopIteration: pass
            return root

#-------------------------------------------------------------------------------
# Helper function
#-------------------------------------------------------------------------------
def tree_walk(node, level=0):
    prefix = '-'*level
    print prefix+repr(node.name), '->', repr(node.value)
    for child in node:
        tree_walk(child, level=level+1)

#-------------------------------------------------------------------------------
# Test the parser
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    fn = 'tree.txt'
    parser = IndentedKVTreeParser(indent='.', indent_count=1, kv_sep=':')
    root = parser.parse(fn)
    tree_walk(root)
