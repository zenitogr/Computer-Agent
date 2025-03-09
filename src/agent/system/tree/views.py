from dataclasses import dataclass,field
from uiautomation import Control

@dataclass
class TreeState:
    nodes:list['TreeElementNode']=field(default_factory=[])
    selector_map:dict[int,'TreeElementNode']=field(default_factory={})

    def elements_to_string(self)->str:
        return '\n'.join([f'Label: {index} - ControlType: {node.control_type} Name: {node.name}' for index,node in enumerate(self.nodes)])

@dataclass
class BoundingBox:
    left:int
    top:int
    right:int
    bottom:int

@dataclass
class CenterCord:
    x:int
    y:int

@dataclass
class TreeElementNode:
    name:str
    control_type:str
    shortcut:str
    bounding_box:BoundingBox
    center:CenterCord
    handle:Control

    def __repr__(self):
        return f'TreeElementNode(name={self.name},control_type={self.control_type},shortcut={self.shortcut},bounding_box={self.bounding_box},center={self.center})'
