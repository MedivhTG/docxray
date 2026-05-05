from enum import IntFlag, StrEnum
from typing import Literal


class WD_STYLE_TYPE(StrEnum):
    CHARACTER = "character"
    LIST = "numbering"
    PARAGRAPH = "paragraph"
    TABLE = "table"


class WD_TBL_STYLE_OVERRIDE_TYPE(StrEnum):
    ENTIRE_TABLE = "wholeTable"
    HEADER_ROW = "firstRow"
    FOOTER_ROW = "lastRow"
    FIRST_COLUMN = "firstCol"
    LAST_COLUMN = "lastCol"
    VERTICAL_BAND_EVEN = "band1Vert"
    VERTICAL_BAND_ODD = "band2Vert"
    HORIZONTAL_BAND_EVEN = "band1Horz"
    HORIZONTAL_BAND_ODD = "band2Horz"
    TOP_RIGHT_CORNER_CELL = "neCell"
    TOP_LEFT_CORNER_CELL = "nwCell"
    BOTTOM_RIGHT_CORNER_CELL = "seCell"
    BOTTOM_LEFT_CORNER_CELL = "swCell"


class WD_CNF_FORMAT(IntFlag):
    # FirstRow
    FIRST_ROW = 1 << 0
    # LastRow
    LAST_ROW = 1 << 1
    # FirstColumn
    FIRST_COLUMN = 1 << 2
    # LastColumn
    LAST_COLUMN = 1 << 3
    # Band1Vertical
    ODD_VERTICAL_BAND = 1 << 4
    # Band2Vertical
    EVEN_VERTICAL_BAND = 1 << 5
    # Band1Horizontal
    ODD_HORIZONTAL_BAND = 1 << 6
    # Band2Horizontal
    EVEN_HORIZONTAL_BAND = 1 << 7
    # NE Cell (NE - NorthEast/TopRight)
    FIRST_ROW_LAST_COLUMN = 1 << 8
    # NW Cell (NW - NorthWest/TopLeft)
    FIRST_ROW_FIRST_COLUMN = 1 << 9
    # SE Cell (SE - SouthEast/BottomRight)
    LAST_ROW_LAST_COLUMN = 1 << 10
    # SW Cell (SW - SouthWest/BottomLeft)
    LAST_ROW_FIRST_COLUMN = 1 << 11

    @classmethod
    def ordered_flags(
        cls, order: Literal["lowest", "highest"] = "highest"
    ) -> list["WD_CNF_FORMAT"]:
        """Get flags in priority order.

        `highest` - first property that will override all others.

        `lowest` - standard inheritance (not recommended for fast resolve).
        """
        if order == "highest":
            return _PRIORITY_FLAGS
        return list(reversed(_PRIORITY_FLAGS))


# Order from reversed -> from highest to lowest:
_PRIORITY_FLAGS = [
    WD_CNF_FORMAT.LAST_ROW_LAST_COLUMN,
    WD_CNF_FORMAT.LAST_ROW_FIRST_COLUMN,
    WD_CNF_FORMAT.FIRST_ROW_LAST_COLUMN,
    WD_CNF_FORMAT.FIRST_ROW_FIRST_COLUMN,
    WD_CNF_FORMAT.LAST_ROW,
    WD_CNF_FORMAT.FIRST_ROW,
    WD_CNF_FORMAT.LAST_COLUMN,
    WD_CNF_FORMAT.FIRST_COLUMN,
    WD_CNF_FORMAT.EVEN_HORIZONTAL_BAND,
    WD_CNF_FORMAT.ODD_HORIZONTAL_BAND,
    WD_CNF_FORMAT.EVEN_VERTICAL_BAND,
    WD_CNF_FORMAT.ODD_VERTICAL_BAND,
]


class WD_MERGE(StrEnum):
    CONTINUE = "continue"
    RESTART = "restart"


class WD_VERTICAL_ALIGN_RUN(StrEnum):
    BASELINE = "baseline"
    SUPERSCRIPT = "superscript"
    SUBSCRIPT = "subscript"


class WD_UNDERLINE(StrEnum):
    SINGLE = "single"
    WORDS = "words"
    DOUBLE = "double"
    THICK = "thick"
    DOTTED = "dotted"
    DOTTED_HEAVY = "dottedHeavy"
    DASH = "dash"
    DASHED_HEAVY = "dashedHeavy"
    DASH_LONG = "dashLong"
    DASH_LONG_HEAVY = "dashLongHeavy"
    DOT_DASH = "dotDash"
    DASH_DOT_HEAVY = "dashDotHeavy"
    DOT_DOT_DASH = "dotDotDash"
    DASH_DOT_DOT_HEAVY = "dashDotDotHeavy"
    WAVE = "wave"
    WAVY_HEAVY = "wavyHeavy"
    WAVY_DOUBLE = "wavyDouble"
    NONE = "none"


class WD_MULTILEVEL_TYPE(StrEnum):
    SINGLE_LEVEL = "singleLevel"
    MULTILEVEL = "multilevel"
    HYBRID_MULTILEVEL = "hybridMultilevel"


class WD_TABLE_WIDTH(StrEnum):
    NONE = "nil"
    PERCENT = "pct"
    TWIPS = "dxa"
    AUTO = "auto"


class WD_BORDER(StrEnum):
    """Border styles for table cells and other elements."""

    NIL = "nil"
    NONE = "none"
    SINGLE = "single"
    THICK = "thick"
    DOUBLE = "double"
    DOTTED = "dotted"
    DASHED = "dashed"
    DOT_DASH = "dotDash"
    DOT_DOT_DASH = "dotDotDash"
    TRIPLE = "triple"
    THIN_THICK_SMALL_GAP = "thinThickSmallGap"
    THICK_THIN_SMALL_GAP = "thickThinSmallGap"
    THIN_THICK_THIN_SMALL_GAP = "thinThickThinSmallGap"
    THIN_THICK_MEDIUM_GAP = "thinThickMediumGap"
    THICK_THIN_MEDIUM_GAP = "thickThinMediumGap"
    THIN_THICK_THIN_MEDIUM_GAP = "thinThickThinMediumGap"
    THIN_THICK_LARGE_GAP = "thinThickLargeGap"
    THICK_THIN_LARGE_GAP = "thickThinLargeGap"
    THIN_THICK_THIN_LARGE_GAP = "thinThickThinLargeGap"
    WAVE = "wave"
    DOUBLE_WAVE = "doubleWave"
    DASH_SMALL_GAP = "dashSmallGap"
    DASH_DOT_STROKED = "dashDotStroked"
    THREE_D_EMBOSS = "threeDEmboss"
    THREE_D_ENGRAVE = "threeDEngrave"
    OUTSET = "outset"
    INSET = "inset"
    APPLES = "apples"
    ARCHED_SCALLOPS = "archedScallops"
    BABY_PACIFIER = "babyPacifier"
    BABY_RATTLE = "babyRattle"
    BALLOONS_3_COLORS = "balloons3Colors"
    BALLOONS_HOT_AIR = "balloonsHotAir"
    BASIC_BLACK_DASHES = "basicBlackDashes"
    BASIC_BLACK_DOTS = "basicBlackDots"
    BASIC_BLACK_SQUARES = "basicBlackSquares"
    BASIC_THIN_LINES = "basicThinLines"
    BASIC_WHITE_DASHES = "basicWhiteDashes"
    BASIC_WHITE_DOTS = "basicWhiteDots"
    BASIC_WHITE_SQUARES = "basicWhiteSquares"
    BASIC_WIDE_INLINE = "basicWideInline"
    BASIC_WIDE_MIDLINE = "basicWideMidline"
    BASIC_WIDE_OUTLINE = "basicWideOutline"
    BATS = "bats"
    BIRDS = "birds"
    BIRDS_FLIGHT = "birdsFlight"
    CABINS = "cabins"
    CAKE_SLICE = "cakeSlice"
    CANDY_CORN = "candyCorn"
    CELTIC_KNOTWORK = "celticKnotwork"
    CERTIFICATE_BANNER = "certificateBanner"
    CHAIN_LINK = "chainLink"
    CHAMPAGNE_BOTTLE = "champagneBottle"
    CHECKED_BAR_BLACK = "checkedBarBlack"
    CHECKED_BAR_COLOR = "checkedBarColor"
    CHECKERED = "checkered"
    CHRISTMAS_TREE = "christmasTree"
    CIRCLES_LINES = "circlesLines"
    CIRCLES_RECTANGLES = "circlesRectangles"
    CLASSICAL_WAVE = "classicalWave"
    CLOCKS = "clocks"
    COMPASS = "compass"
    CONFETTI = "confetti"
    CONFETTI_GRAYS = "confettiGrays"
    CONFETTI_OUTLINE = "confettiOutline"
    CONFETTI_STREAMERS = "confettiStreamers"
    CONFETTI_WHITE = "confettiWhite"
    CORNER_TRIANGLES = "cornerTriangles"
    COUPON_CUTOUT_DASHES = "couponCutoutDashes"
    COUPON_CUTOUT_DOTS = "couponCutoutDots"
    CRAZY_MAZE = "crazyMaze"
    CREATURES_BUTTERFLY = "creaturesButterfly"
    CREATURES_FISH = "creaturesFish"
    CREATURES_INSECTS = "creaturesInsects"
    CREATURES_LADY_BUG = "creaturesLadyBug"
    CROSS_STITCH = "crossStitch"
    CUP = "cup"
    DECO_ARCH = "decoArch"
    DECO_ARCH_COLOR = "decoArchColor"
    DECO_BLOCKS = "decoBlocks"
    DIAMONDS_GRAY = "diamondsGray"
    DOUBLE_D = "doubleD"
    DOUBLE_DIAMONDS = "doubleDiamonds"
    EARTH_1 = "earth1"
    EARTH_2 = "earth2"
    EARTH_3 = "earth3"
    ECLIPSING_SQUARES_1 = "eclipsingSquares1"
    ECLIPSING_SQUARES_2 = "eclipsingSquares2"
    EGGS_BLACK = "eggsBlack"
    FANS = "fans"
    FILM = "film"
    FIRECRACKERS = "firecrackers"
    FLOWERS_BLOCK_PRINT = "flowersBlockPrint"
    FLOWERS_DAISIES = "flowersDaisies"
    FLOWERS_MODERN_1 = "flowersModern1"
    FLOWERS_MODERN_2 = "flowersModern2"
    FLOWERS_PANSY = "flowersPansy"
    FLOWERS_RED_ROSE = "flowersRedRose"
    FLOWERS_ROSES = "flowersRoses"
    FLOWERS_TEACUP = "flowersTeacup"
    FLOWERS_TINY = "flowersTiny"
    GEMS = "gems"
    GINGERBREAD_MAN = "gingerbreadMan"
    GRADIENT = "gradient"
    HANDMADE_1 = "handmade1"
    HANDMADE_2 = "handmade2"
    HEART_BALLOON = "heartBalloon"
    HEART_GRAY = "heartGray"
    HEARTS = "hearts"
    HEEBIE_JEEBIES = "heebieJeebies"
    HOLLY = "holly"
    HOUSE_FUNKY = "houseFunky"
    HYPNOTIC = "hypnotic"
    ICE_CREAM_CONES = "iceCreamCones"
    LIGHT_BULB = "lightBulb"
    LIGHTNING_1 = "lightning1"
    LIGHTNING_2 = "lightning2"
    MAP_PINS = "mapPins"
    MAPLE_LEAF = "mapleLeaf"
    MAPLE_MUFFINS = "mapleMuffins"
    MARQUEE = "marquee"
    MARQUEE_TOOTHED = "marqueeToothed"
    MOONS = "moons"
    MOSAIC = "mosaic"
    MUSIC_NOTES = "musicNotes"
    NORTHWEST = "northwest"
    OVALS = "ovals"
    PACKAGES = "packages"
    PALMS_BLACK = "palmsBlack"
    PALMS_COLOR = "palmsColor"
    PAPER_CLIPS = "paperClips"
    PAPYRUS = "papyrus"
    PARTY_FAVOR = "partyFavor"
    PARTY_GLASS = "partyGlass"
    PENCILS = "pencils"
    PEOPLE = "people"
    PEOPLE_WAVING = "peopleWaving"
    PEOPLE_HATS = "peopleHats"
    POINSETTIAS = "poinsettias"
    POSTAGE_STAMP = "postageStamp"
    PUMPKIN_1 = "pumpkin1"
    PUSH_PIN_NOTE_2 = "pushPinNote2"
    PUSH_PIN_NOTE_1 = "pushPinNote1"
    PYRAMIDS = "pyramids"
    PYRAMIDS_ABOVE = "pyramidsAbove"
    QUADRANTS = "quadrants"
    RINGS = "rings"
    SAFARI = "safari"
    SAWTOOTH = "sawtooth"
    SAWTOOTH_GRAY = "sawtoothGray"
    SCARED_CAT = "scaredCat"
    SEATTLE = "seattle"
    SHADOWED_SQUARES = "shadowedSquares"
    SHARKS_TEETH = "sharksTeeth"
    SHOREBIRD_TRACKS = "shorebirdTracks"
    SKYROCKET = "skyrocket"
    SNOWFLAKE_FANCY = "snowflakeFancy"
    SNOWFLAKES = "snowflakes"
    SOMBRERO = "sombrero"
    SOUTHWEST = "southwest"
    STARS = "stars"
    STARS_TOP = "starsTop"
    STARS_3D = "stars3d"
    STARS_BLACK = "starsBlack"
    STARS_SHADOWED = "starsShadowed"
    SUN = "sun"
    SWIRLIGIG = "swirligig"
    TORN_PAPER = "tornPaper"
    TORN_PAPER_BLACK = "tornPaperBlack"
    TREES = "trees"
    TRIANGLE_PARTY = "triangleParty"
    TRIANGLES = "triangles"
    TRIANGLE_1 = "triangle1"
    TRIANGLE_2 = "triangle2"
    TRIANGLE_CIRCLE_1 = "triangleCircle1"
    TRIANGLE_CIRCLE_2 = "triangleCircle2"
    SHAPES_1 = "shapes1"
    SHAPES_2 = "shapes2"
    TWISTED_LINES_1 = "twistedLines1"
    TWISTED_LINES_2 = "twistedLines2"
    VINE = "vine"
    WAVELINE = "waveline"
    WEAVING_ANGLES = "weavingAngles"
    WEAVING_BRAID = "weavingBraid"
    WEAVING_RIBBON = "weavingRibbon"
    WEAVING_STRIPS = "weavingStrips"
    WHITE_FLOWERS = "whiteFlowers"
    WOODWORK = "woodwork"
    X_ILLUSIONS = "xIllusions"
    ZANY_TRIANGLES = "zanyTriangles"
    ZIG_ZAG = "zigZag"
    ZIG_ZAG_STITCH = "zigZagStitch"
    CUSTOM = "custom"
