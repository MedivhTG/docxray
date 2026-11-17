from enum import StrEnum


class WmfMimeType(StrEnum):
    WMF = "image/wmf"
    EMF = "image/emf"


# BigEndian to LittleEndian
WMF_PH_KEY = bytes.fromhex("D7 CD C6 9A")
WMF_RAW_TYPE_1 = bytes.fromhex("01 00")
WMF_RAW_TYPE_2 = bytes.fromhex("02 00")
WMF_RAW_HEADER_SIZE = bytes.fromhex("09 00")
WMF_RAW_VERSION_1 = bytes.fromhex("00 01")
WMF_RAW_VERSION_3 = bytes.fromhex("00 03")

EMR_HEADER_TYPE = bytes.fromhex("01 00 00 00")
EMR_ENHMETA_SIGNATURE = bytes.fromhex("20 45 4D 46")


def wmf_type(wmf_blob: bytes) -> WmfMimeType | None:
    """Determine mime type of hypothetical WMF blob.

    Analyzes the image with signature bytes or structure
    (shallow view) of WMF/EMF files.

    Args:
        wmf_blob (bytes): Image blob.
    """
    if is_wmf(wmf_blob):
        return WmfMimeType.WMF
    if is_emf(wmf_blob):
        return WmfMimeType.EMF
    return None


def is_wmf(blob: bytes) -> bool:
    if len(blob) < 18:
        return False

    return blob.startswith(WMF_PH_KEY) or (
        blob[:2] in (WMF_RAW_TYPE_1, WMF_RAW_TYPE_2)
        and blob[2:4] == WMF_RAW_HEADER_SIZE
        and blob[4:6] in (WMF_RAW_VERSION_1, WMF_RAW_VERSION_3)
    )


def is_emf(blob: bytes) -> bool:
    return (
        len(blob) >= 88
        and blob[:4] == EMR_HEADER_TYPE
        and blob[40:44] == EMR_ENHMETA_SIGNATURE
    )
