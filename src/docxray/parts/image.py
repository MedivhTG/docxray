"""The proxy class for an image part, and related objects."""

from __future__ import annotations

# docxray stuff
from docxray.opc.part import Part


class ImagePart(Part):
    """An image part.

    Corresponds to the target part of a relationship with type RELATIONSHIP_TYPE.IMAGE.
    """

    pass
