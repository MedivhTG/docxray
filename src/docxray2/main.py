from .opc.package import OpcPackage
from .opc.part import PartFactory

package = OpcPackage.open("tests/examples/content_check.docx", PartFactory)
wait = 1
