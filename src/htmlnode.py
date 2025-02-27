class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        new_string = ""
        if self.props == None:
            return new_string
        for item in self.props.items():
            new_string += f" {item[0]}='{item[1]}'"
        return new_string
    
    def __repr__(self):
        if self.children != None:
            return f"HTMLNode({self.tag},{self.value},{repr(self.children)},{self.props})"
        else:
            return f"HTMLNode({self.tag},{self.value},,{self.props})"
        
class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("No value provided")
        new_string = ""
        if self.tag == None:
            new_string = self.value
        else:
            prop_string = self.props_to_html()
            new_string = f"<{self.tag}{prop_string}>{self.value}</{self.tag}>"
        return new_string
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag provided")
        if self.children == None:
            raise ValueError("No children present")
        html_string = ""
        for child in self.children:
            html_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>"
