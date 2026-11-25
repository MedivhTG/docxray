from enum import StrEnum


class SE_VECTOR_BASE_TYPE(StrEnum):
    VARIANT = "variant"
    I1 = "i1"
    I2 = "i2"
    I4 = "i4"
    I8 = "i8"
    UI1 = "ui1"
    UI2 = "ui2"
    UI4 = "ui4"
    UI8 = "ui8"
    R4 = "r4"
    R8 = "r8"
    LPSTR = "lpstr"
    LPWSTR = "lpwstr"
    BSTR = "bstr"
    DATE = "date"
    FILETIME = "filetime"
    BOOL = "bool"
    CY = "cy"
    ERROR = "error"
    CLSID = "clsid"


class SE_ARRAY_BASE_TYPE(StrEnum):
    VARIANT = "variant"
    I1 = "i1"
    I2 = "i2"
    I4 = "i4"
    INT = "int"
    UI1 = "ui1"
    UI2 = "ui2"
    UI4 = "ui4"
    UINT = "uint"
    R4 = "r4"
    R8 = "r8"
    DECIMAL = "decimal"
    BSTR = "bstr"
    DATE = "date"
    BOOL = "bool"
    CY = "cy"
    ERROR = "error"


class SE_SOURCE_TYPE(StrEnum):
    ARTICLE_IN_A_PERIODICAL = "ArticleInAPeriodical"
    BOOK = "Book"
    BOOK_SECTION = "BookSection"
    JOURNAL_ARTICLE = "JournalArticle"
    CONFERENCE_PROCEEDINGS = "ConferenceProceedings"
    REPORT = "Report"
    SOUND_RECORDING = "SoundRecording"
    PERFORMANCE = "Performance"
    ART = "Art"
    DOCUMENT_FROM_INTERNET_SITE = "DocumentFromInternetSite"
    INTERNET_SITE = "InternetSite"
    FILM = "Film"
    INTERVIEW = "Interview"
    PATENT = "Patent"
    ELECTRONIC_SOURCE = "ElectronicSource"
    CASE = "Case"
    MISC = "Misc"


class SE_ST_CALENDAR_TYPE(StrEnum):
    GREGORIAN = "gregorian"
    GREGORIAN_US = "gregorianUs"
    GREGORIAN_ME_FRENCH = "gregorianMeFrench"
    GREGORIAN_ARABIC = "gregorianArabic"
    HIJRI = "hijri"
    HEBREW = "hebrew"
    TAIWAN = "taiwan"
    JAPAN = "japan"
    THAI = "thai"
    KOREA = "korea"
    SAKA = "saka"
    GREGORIAN_XLIT_ENGLISH = "gregorianXlitEnglish"
    GREGORIAN_XLIT_FRENCH = "gregorianXlitFrench"
    NONE = "none"


class SE_ST_ALG_CLASS(StrEnum):
    HASH = "hash"
    CUSTOM = "custom"


class SE_ST_CRYPT_PROV(StrEnum):
    RSA_AES = "rsaAES"
    RSA_FULL = "rsaFull"
    CUSTOM = "custom"


class SE_ST_ALG_TYPE(StrEnum):
    TYPE_ANY = "typeAny"
    CUSTOM = "custom"


class SE_ST_ON_OFF1(StrEnum):
    ON = "on"
    OFF = "off"


class SE_ST_TRUE_FALSE(StrEnum):
    T = "t"
    F = "f"
    TRUE = "true"
    FALSE = "false"


class SE_ST_TRUE_FALSE_BLANK(StrEnum):
    T = "t"
    F = "f"
    TRUE = "true"
    FALSE = "false"
    BLANK = ""
    TRUE_CAP = "True"
    FALSE_CAP = "False"


class SE_ST_VERTICAL_ALIGN_RUN(StrEnum):
    BASELINE = "baseline"
    SUPERSCRIPT = "superscript"
    SUBSCRIPT = "subscript"


class SE_ST_X_ALIGN(StrEnum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    INSIDE = "inside"
    OUTSIDE = "outside"


class SE_ST_Y_ALIGN(StrEnum):
    INLINE = "inline"
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"
    INSIDE = "inside"
    OUTSIDE = "outside"


class SE_ST_CONFORMANCE_CLASS(StrEnum):
    STRICT = "strict"
    TRANSITIONAL = "transitional"
