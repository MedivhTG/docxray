"""XML namespace URIs for OOXML/Word documents, grouped by OPC part."""


class NAMESPACE_URI:
    """Namespace URIs for OOXML/Word package parts (class-level str constants)."""

    MEDIA_TYPES_STREAM = (
        "http://schemas.openxmlformats.org/package/2006/content-types"
    )
    CORE_PROPERTIES = "http://schemas.openxmlformats.org/package/2006/metadata/coreproperties"
    DIGITAL_SIGNATURES = (
        "http://schemas.openxmlformats.org/package/2006/digitalsignature"
    )
    RELATIONSHIPS = (
        "http://schemas.openxmlformats.org/package/2006/relationships"
    )


class MEDIA_TYPE:
    # Package-wide media types
    CORE_PROPERTIES_PART = (
        "application/vnd.openxmlformats-package.core-properties+xml"
    )
    DIGITAL_SIGNATURE_CERTIFICATE_PART = (
        "application/vnd.openxmlformats-package.digital-signature-certificate"
    )
    DIGITAL_SIGNATURE_ORIGIN_PART = (
        "application/vnd.openxmlformats-package.digital-signature-origin"
    )
    DIGITAL_SIGNATURE_XML_SIGNATURE_PART = "application/vnd.openxmlformats-package.digital-signature-xmlsignature+xml"
    RELATIONSHIPS_PART = (
        "application/vnd.openxmlformats-package.relationships+xml"
    )
    # Fundamentals
    MAIN_DOCUMENT_PART = "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
    EXTENDED_FILE_PROPERTIES_PART = (
        "application/vnd.openxmlformats-officedocument.extended-properties+xml"
    )


class RELATIONSHIP_TYPE:
    # Transitional
    MAIN_DOCUMENT_PART_TRANSITIONAL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
