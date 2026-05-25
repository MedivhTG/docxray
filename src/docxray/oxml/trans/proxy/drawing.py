# from functools import cached_property

# docxray stuff
from docxray.oxml.trans.drawing import CT_Drawing

# from docxray.oxml.trans.image.image import Image
from docxray.oxml.trans.proxy.shared import ElementProxy


class Drawing(ElementProxy[CT_Drawing]):
    pass
