from .opc.pkg_reader import PkgReader

reader = PkgReader.from_file("tests/examples/content_check.docx")
wait = 1
