"""
Generated the AST
"""
from graphviz import Digraph

class AST:
    def __init__(self, ast):
        self.ast = ast
    def draw_ast(self, filename='ast'):
        dot = Digraph(comment='Abstract Syntax Tree')

        def add_nodes(node, parent_id=None):
            node_id = str(id(node))

            if isinstance(node, dict):
                dot.node(node_id, f"{node.get('type', 'node')}")

                if parent_id is not None:
                    dot.edge(parent_id, node_id)
                for key, value in node.items():
                    if isinstance(value, (dict, list)):
                        add_nodes(value, node_id)
                    else:
                        leaf_id = f"{node_id}_{key}"
                        dot.node(leaf_id, f"{key}: {value}")
                        dot.edge(node_id, leaf_id)

            elif isinstance(node, list):
                for index, item in enumerate(node):
                    item_id = f"{node_id}_{index}"
                    dot.node(item_id, f"Statement {index}")
                    if parent_id is not None:
                        dot.edge(parent_id, item_id)
                    add_nodes(item, item_id)
        add_nodes(self.ast)
        
        image_path = dot.render(filename, format='png', cleanup=True)

        return image_path
    