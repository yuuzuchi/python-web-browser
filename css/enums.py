from enum import Enum


# ==================================== parsing ==================================== #


class Property(Enum):
    CUSTOM = "custom"
    FONT = "font"
    FONT_VARIANT = "font-variant"
    LIST_STYLE = "list-style"
    TEXT_WRAP = "text-wrap"
    ALL = "all"
    ANIMATION = "animation"
    BACKGROUND = "background"
    BACKGROUND_POSITION = "background-position"
    BORDER = "border"
    BORDER_BLOCK = "border-block"
    BORDER_BLOCK_COLOR = "border-block-color"
    BORDER_BLOCK_END = "border-block-end"
    BORDER_BLOCK_START = "border-block-start"
    BORDER_BLOCK_STYLE = "border-block-style"
    BORDER_BLOCK_WIDTH = "border-block-width"
    BORDER_BOTTOM = "border-bottom"
    BORDER_COLOR = "border-color"
    BORDER_IMAGE = "border-image"
    BORDER_INLINE = "border-inline"
    BORDER_INLINE_COLOR = "border-inline-color"
    BORDER_INLINE_END = "border-inline-end"
    BORDER_INLINE_START = "border-inline-start"
    BORDER_INLINE_STYLE = "border-inline-style"
    BORDER_INLINE_WIDTH = "border-inline-width"
    BORDER_LEFT = "border-left"
    BORDER_RADIUS = "border-radius"
    BORDER_RIGHT = "border-right"
    BORDER_STYLE = "border-style"
    BORDER_TOP = "border-top"
    BORDER_WIDTH = "border-width"
    COLUMNS = "columns"
    CORNER_BLOCK_END_SHAPE = "corner-block-end-shape"
    CORNER_BLOCK_START_SHAPE = "corner-block-start-shape"
    CORNER_BOTTOM_SHAPE = "corner-bottom-shape"
    CORNER_INLINE_END_SHAPE = "corner-inline-end-shape"
    CORNER_INLINE_START_SHAPE = "corner-inline-start-shape"
    CORNER_LEFT_SHAPE = "corner-left-shape"
    CORNER_RIGHT_SHAPE = "corner-right-shape"
    CORNER_SHAPE = "corner-shape"
    CORNER_TOP_SHAPE = "corner-top-shape"
    FLEX = "flex"
    FLEX_FLOW = "flex-flow"
    GAP = "gap"
    GRID = "grid"
    GRID_AREA = "grid-area"
    GRID_COLUMN = "grid-column"
    GRID_ROW = "grid-row"
    GRID_TEMPLATE = "grid-template"
    INSET = "inset"
    INSET_BLOCK = "inset-block"
    INSET_INLINE = "inset-inline"
    MARGIN = "margin"
    MARGIN_BLOCK = "margin-block"
    MARGIN_INLINE = "margin-inline"
    MASK = "mask"
    OUTLINE = "outline"
    OVERFLOW = "overflow"
    PADDING = "padding"
    PADDING_BLOCK = "padding-block"
    PADDING_INLINE = "padding-inline"
    PLACE_CONTENT = "place-content"
    PLACE_ITEMS = "place-items"
    PLACE_SELF = "place-self"
    TEXT_DECORATION = "text-decoration"
    TRANSITION = "transition"
    WHITE_SPACE = "white-space"
    WEBKIT_TEXT_FILL_COLOR = "-webkit-text-fill-color"
    ACCENT_COLOR = "accent-color"
    BORDER_COLLAPSE = "border-collapse"
    BORDER_SPACING = "border-spacing"
    CAPTION_SIDE = "caption-side"
    CARET_COLOR = "caret-color"
    CLIP_RULE = "clip-rule"
    COLOR = "color"
    COLOR_INTERPOLATION = "color-interpolation"
    COLOR_SCHEME = "color-scheme"
    CURSOR = "cursor"
    DIRECTION = "direction"
    EMPTY_CELLS = "empty-cells"
    FILL = "fill"
    FILL_OPACITY = "fill-opacity"
    FILL_RULE = "fill-rule"
    FONT_FAMILY = "font-family"
    FONT_FEATURE_SETTINGS = "font-feature-settings"
    FONT_KERNING = "font-kerning"
    FONT_LANGUAGE_OVERRIDE = "font-language-override"
    FONT_SIZE = "font-size"
    FONT_STYLE = "font-style"
    FONT_VARIANT_ALTERNATES = "font-variant-alternates"
    FONT_VARIANT_CAPS = "font-variant-caps"
    FONT_VARIANT_EAST_ASIAN = "font-variant-east-asian"
    FONT_VARIANT_EMOJI = "font-variant-emoji"
    FONT_VARIANT_LIGATURES = "font-variant-ligatures"
    FONT_VARIANT_NUMERIC = "font-variant-numeric"
    FONT_VARIANT_POSITION = "font-variant-position"
    FONT_VARIATION_SETTINGS = "font-variation-settings"
    FONT_WEIGHT = "font-weight"
    FONT_WIDTH = "font-width"
    IMAGE_RENDERING = "image-rendering"
    LETTER_SPACING = "letter-spacing"
    LINE_HEIGHT = "line-height"
    LIST_STYLE_IMAGE = "list-style-image"
    LIST_STYLE_POSITION = "list-style-position"
    LIST_STYLE_TYPE = "list-style-type"
    MATH_DEPTH = "math-depth"
    MATH_SHIFT = "math-shift"
    MATH_STYLE = "math-style"
    ORPHANS = "orphans"
    OVERFLOW_WRAP = "overflow-wrap"
    PAINT_ORDER = "paint-order"
    POINTER_EVENTS = "pointer-events"
    QUOTES = "quotes"
    SHAPE_RENDERING = "shape-rendering"
    STROKE = "stroke"
    STROKE_DASHARRAY = "stroke-dasharray"
    STROKE_DASHOFFSET = "stroke-dashoffset"
    STROKE_LINECAP = "stroke-linecap"
    STROKE_LINEJOIN = "stroke-linejoin"
    STROKE_MITERLIMIT = "stroke-miterlimit"
    STROKE_OPACITY = "stroke-opacity"
    STROKE_WIDTH = "stroke-width"
    TAB_SIZE = "tab-size"
    TEXT_ALIGN = "text-align"
    TEXT_ANCHOR = "text-anchor"
    TEXT_DECORATION_LINE = "text-decoration-line"
    TEXT_INDENT = "text-indent"
    TEXT_JUSTIFY = "text-justify"
    TEXT_RENDERING = "text-rendering"
    TEXT_SHADOW = "text-shadow"
    TEXT_TRANSFORM = "text-transform"
    TEXT_UNDERLINE_OFFSET = "text-underline-offset"
    TEXT_UNDERLINE_POSITION = "text-underline-position"
    TEXT_WRAP_MODE = "text-wrap-mode"
    TEXT_WRAP_STYLE = "text-wrap-style"
    VISIBILITY = "visibility"
    WHITE_SPACE_COLLAPSE = "white-space-collapse"
    WIDOWS = "widows"
    WORD_BREAK = "word-break"
    WORD_SPACING = "word-spacing"
    WRITING_MODE = "writing-mode"
    ALIGN_CONTENT = "align-content"
    ALIGN_ITEMS = "align-items"
    ALIGN_SELF = "align-self"
    ANCHOR_NAME = "anchor-name"
    ANCHOR_SCOPE = "anchor-scope"
    ANIMATION_COMPOSITION = "animation-composition"
    ANIMATION_DELAY = "animation-delay"
    ANIMATION_DIRECTION = "animation-direction"
    ANIMATION_DURATION = "animation-duration"
    ANIMATION_FILL_MODE = "animation-fill-mode"
    ANIMATION_ITERATION_COUNT = "animation-iteration-count"
    ANIMATION_NAME = "animation-name"
    ANIMATION_PLAY_STATE = "animation-play-state"
    ANIMATION_TIMING_FUNCTION = "animation-timing-function"
    APPEARANCE = "appearance"
    ASPECT_RATIO = "aspect-ratio"
    BACKDROP_FILTER = "backdrop-filter"
    BACKGROUND_ATTACHMENT = "background-attachment"
    BACKGROUND_BLEND_MODE = "background-blend-mode"
    BACKGROUND_CLIP = "background-clip"
    BACKGROUND_COLOR = "background-color"
    BACKGROUND_IMAGE = "background-image"
    BACKGROUND_ORIGIN = "background-origin"
    BACKGROUND_POSITION_X = "background-position-x"
    BACKGROUND_POSITION_Y = "background-position-y"
    BACKGROUND_REPEAT = "background-repeat"
    BACKGROUND_SIZE = "background-size"
    BLOCK_SIZE = "block-size"
    BORDER_BLOCK_END_COLOR = "border-block-end-color"
    BORDER_BLOCK_END_STYLE = "border-block-end-style"
    BORDER_BLOCK_END_WIDTH = "border-block-end-width"
    BORDER_BLOCK_START_COLOR = "border-block-start-color"
    BORDER_BLOCK_START_STYLE = "border-block-start-style"
    BORDER_BLOCK_START_WIDTH = "border-block-start-width"
    BORDER_BOTTOM_COLOR = "border-bottom-color"
    BORDER_BOTTOM_LEFT_RADIUS = "border-bottom-left-radius"
    BORDER_BOTTOM_RIGHT_RADIUS = "border-bottom-right-radius"
    BORDER_BOTTOM_STYLE = "border-bottom-style"
    BORDER_BOTTOM_WIDTH = "border-bottom-width"
    BORDER_END_END_RADIUS = "border-end-end-radius"
    BORDER_END_START_RADIUS = "border-end-start-radius"
    BORDER_IMAGE_OUTSET = "border-image-outset"
    BORDER_IMAGE_REPEAT = "border-image-repeat"
    BORDER_IMAGE_SLICE = "border-image-slice"
    BORDER_IMAGE_SOURCE = "border-image-source"
    BORDER_IMAGE_WIDTH = "border-image-width"
    BORDER_INLINE_END_COLOR = "border-inline-end-color"
    BORDER_INLINE_END_STYLE = "border-inline-end-style"
    BORDER_INLINE_END_WIDTH = "border-inline-end-width"
    BORDER_INLINE_START_COLOR = "border-inline-start-color"
    BORDER_INLINE_START_STYLE = "border-inline-start-style"
    BORDER_INLINE_START_WIDTH = "border-inline-start-width"
    BORDER_LEFT_COLOR = "border-left-color"
    BORDER_LEFT_STYLE = "border-left-style"
    BORDER_LEFT_WIDTH = "border-left-width"
    BORDER_RIGHT_COLOR = "border-right-color"
    BORDER_RIGHT_STYLE = "border-right-style"
    BORDER_RIGHT_WIDTH = "border-right-width"
    BORDER_START_END_RADIUS = "border-start-end-radius"
    BORDER_START_START_RADIUS = "border-start-start-radius"
    BORDER_TOP_COLOR = "border-top-color"
    BORDER_TOP_LEFT_RADIUS = "border-top-left-radius"
    BORDER_TOP_RIGHT_RADIUS = "border-top-right-radius"
    BORDER_TOP_STYLE = "border-top-style"
    BORDER_TOP_WIDTH = "border-top-width"
    BOTTOM = "bottom"
    BOX_SHADOW = "box-shadow"
    BOX_SIZING = "box-sizing"
    CLEAR = "clear"
    CLIP = "clip"
    CLIP_PATH = "clip-path"
    COLUMN_COUNT = "column-count"
    COLUMN_GAP = "column-gap"
    COLUMN_HEIGHT = "column-height"
    COLUMN_SPAN = "column-span"
    COLUMN_WIDTH = "column-width"
    CONTAIN = "contain"
    CONTAINER_TYPE = "container-type"
    CONTENT = "content"
    CONTENT_VISIBILITY = "content-visibility"
    CORNER_BOTTOM_LEFT_SHAPE = "corner-bottom-left-shape"
    CORNER_BOTTOM_RIGHT_SHAPE = "corner-bottom-right-shape"
    CORNER_END_END_SHAPE = "corner-end-end-shape"
    CORNER_END_START_SHAPE = "corner-end-start-shape"
    CORNER_START_END_SHAPE = "corner-start-end-shape"
    CORNER_START_START_SHAPE = "corner-start-start-shape"
    CORNER_TOP_LEFT_SHAPE = "corner-top-left-shape"
    CORNER_TOP_RIGHT_SHAPE = "corner-top-right-shape"
    COUNTER_INCREMENT = "counter-increment"
    COUNTER_RESET = "counter-reset"
    COUNTER_SET = "counter-set"
    CX = "cx"
    CY = "cy"
    DISPLAY = "display"
    FILTER = "filter"
    FLEX_BASIS = "flex-basis"
    FLEX_DIRECTION = "flex-direction"
    FLEX_GROW = "flex-grow"
    FLEX_SHRINK = "flex-shrink"
    FLEX_WRAP = "flex-wrap"
    FLOAT = "float"
    FLOOD_COLOR = "flood-color"
    FLOOD_OPACITY = "flood-opacity"
    GRID_AUTO_COLUMNS = "grid-auto-columns"
    GRID_AUTO_FLOW = "grid-auto-flow"
    GRID_AUTO_ROWS = "grid-auto-rows"
    GRID_COLUMN_END = "grid-column-end"
    GRID_COLUMN_START = "grid-column-start"
    GRID_ROW_END = "grid-row-end"
    GRID_ROW_START = "grid-row-start"
    GRID_TEMPLATE_AREAS = "grid-template-areas"
    GRID_TEMPLATE_COLUMNS = "grid-template-columns"
    GRID_TEMPLATE_ROWS = "grid-template-rows"
    HEIGHT = "height"
    HYPHENS = "hyphens"
    INLINE_SIZE = "inline-size"
    INSET_BLOCK_END = "inset-block-end"
    INSET_BLOCK_START = "inset-block-start"
    INSET_INLINE_END = "inset-inline-end"
    INSET_INLINE_START = "inset-inline-start"
    ISOLATION = "isolation"
    JUSTIFY_CONTENT = "justify-content"
    JUSTIFY_ITEMS = "justify-items"
    JUSTIFY_SELF = "justify-self"
    LEFT = "left"
    MARGIN_BLOCK_END = "margin-block-end"
    MARGIN_BLOCK_START = "margin-block-start"
    MARGIN_BOTTOM = "margin-bottom"
    MARGIN_INLINE_END = "margin-inline-end"
    MARGIN_INLINE_START = "margin-inline-start"
    MARGIN_LEFT = "margin-left"
    MARGIN_RIGHT = "margin-right"
    MARGIN_TOP = "margin-top"
    MASK_CLIP = "mask-clip"
    MASK_COMPOSITE = "mask-composite"
    MASK_IMAGE = "mask-image"
    MASK_MODE = "mask-mode"
    MASK_ORIGIN = "mask-origin"
    MASK_POSITION = "mask-position"
    MASK_REPEAT = "mask-repeat"
    MASK_SIZE = "mask-size"
    MASK_TYPE = "mask-type"
    MAX_BLOCK_SIZE = "max-block-size"
    MAX_HEIGHT = "max-height"
    MAX_INLINE_SIZE = "max-inline-size"
    MAX_WIDTH = "max-width"
    MIN_BLOCK_SIZE = "min-block-size"
    MIN_HEIGHT = "min-height"
    MIN_INLINE_SIZE = "min-inline-size"
    MIN_WIDTH = "min-width"
    MIX_BLEND_MODE = "mix-blend-mode"
    OBJECT_FIT = "object-fit"
    OBJECT_POSITION = "object-position"
    OPACITY = "opacity"
    ORDER = "order"
    OUTLINE_COLOR = "outline-color"
    OUTLINE_OFFSET = "outline-offset"
    OUTLINE_STYLE = "outline-style"
    OUTLINE_WIDTH = "outline-width"
    OVERFLOW_BLOCK = "overflow-block"
    OVERFLOW_INLINE = "overflow-inline"
    OVERFLOW_X = "overflow-x"
    OVERFLOW_Y = "overflow-y"
    PADDING_BLOCK_END = "padding-block-end"
    PADDING_BLOCK_START = "padding-block-start"
    PADDING_BOTTOM = "padding-bottom"
    PADDING_INLINE_END = "padding-inline-end"
    PADDING_INLINE_START = "padding-inline-start"
    PADDING_LEFT = "padding-left"
    PADDING_RIGHT = "padding-right"
    PADDING_TOP = "padding-top"
    PERSPECTIVE = "perspective"
    POSITION = "position"
    POSITION_ANCHOR = "position-anchor"
    POSITION_AREA = "position-area"
    POSITION_TRY_FALLBACKS = "position-try-fallbacks"
    POSITION_TRY_ORDER = "position-try-order"
    POSITION_VISIBILITY = "position-visibility"
    R = "r"
    RIGHT = "right"
    ROTATE = "rotate"
    ROW_GAP = "row-gap"
    RX = "rx"
    RY = "ry"
    SCALE = "scale"
    SCROLLBAR_COLOR = "scrollbar-color"
    SCROLLBAR_GUTTER = "scrollbar-gutter"
    SCROLLBAR_WIDTH = "scrollbar-width"
    SHAPE_IMAGE_THRESHOLD = "shape-image-threshold"
    SHAPE_MARGIN = "shape-margin"
    SHAPE_OUTSIDE = "shape-outside"
    STOP_COLOR = "stop-color"
    STOP_OPACITY = "stop-opacity"
    TABLE_LAYOUT = "table-layout"
    TEXT_DECORATION_COLOR = "text-decoration-color"
    TEXT_DECORATION_STYLE = "text-decoration-style"
    TEXT_DECORATION_THICKNESS = "text-decoration-thickness"
    TEXT_OVERFLOW = "text-overflow"
    TOP = "top"
    TOUCH_ACTION = "touch-action"
    TRANSFORM = "transform"
    TRANSFORM_BOX = "transform-box"
    TRANSFORM_ORIGIN = "transform-origin"
    TRANSFORM_STYLE = "transform-style"
    TRANSITION_BEHAVIOR = "transition-behavior"
    TRANSITION_DELAY = "transition-delay"
    TRANSITION_DURATION = "transition-duration"
    TRANSITION_PROPERTY = "transition-property"
    TRANSITION_TIMING_FUNCTION = "transition-timing-function"
    TRANSLATE = "translate"
    UNICODE_BIDI = "unicode-bidi"
    USER_SELECT = "user-select"
    VERTICAL_ALIGN = "vertical-align"
    VIEW_TRANSITION_NAME = "view-transition-name"
    WHITE_SPACE_TRIM = "white-space-trim"
    WIDTH = "width"
    WILL_CHANGE = "will-change"
    X = "x"
    Y = "y"
    Z_INDEX = "z-index"

    @classmethod
    def from_name(cls, css_name: str) -> "Property":
        try:
            return cls(css_name)
        except ValueError:
            return None


class ValueType(Enum):
    ANCHOR = "anchor"
    ANCHOR_SIZE = "anchor-size"
    ANGLE = "angle"
    ANGLE_PERCENTAGE = "angle-percentage"
    BACKGROUND_POSITION = "background-position"
    BASIC_SHAPE = "basic-shape"
    COLOR = "color"
    CORNER_SHAPE = "corner-shape"
    COUNTER = "counter"
    CUSTOM_IDENT = "custom-ident"
    DASHED_IDENT = "dashed-ident"
    EASING_FUNCTION = "easing-function"
    FILTER_VALUE_LIST = "filter-value-list"
    FIT_CONTENT = "fit-content"
    FLEX = "flex"
    FREQUENCY = "frequency"
    FREQUENCY_PERCENTAGE = "frequency-percentage"
    IMAGE = "image"
    INTEGER = "integer"
    LENGTH = "length"
    LENGTH_PERCENTAGE = "length-percentage"
    NUMBER = "number"
    OPACITY = "opacity"
    OPENTYPE_TAG = "opentype-tag"
    PAINT = "paint"
    PERCENTAGE = "percentage"
    POSITION = "position"
    RATIO = "ratio"
    RECT = "rect"
    RESOLUTION = "resolution"
    STRING = "string"
    TIME = "time"
    TIME_PERCENTAGE = "time-percentage"
    TRANSFORM_FUNCTION = "transform-function"
    TRANSFORM_LIST = "transform-list"
    URL = "url"


# Incomplete, see https://www.w3schools.com/cssref/index.php
class Keyword(str, Enum):
    """Automatically generated from all_keywords.h"""

    NEGATIVE_INFINITY = "negative-infinity"
    A3 = "a3"
    A4 = "a4"
    A5 = "a5"
    ABSOLUTE = "absolute"
    ACCENTCOLOR = "accentcolor"
    ACCENTCOLORTEXT = "accentcolortext"
    ACCUMULATE = "accumulate"
    ACTIVE = "active"
    ACTIVEBORDER = "activeborder"
    ACTIVECAPTION = "activecaption"
    ACTIVETEXT = "activetext"
    ADD = "add"
    ADDITIVE = "additive"
    ALIAS = "alias"
    ALL = "all"
    ALL_PETITE_CAPS = "all-petite-caps"
    ALL_SCROLL = "all-scroll"
    ALL_SMALL_CAPS = "all-small-caps"
    ALLOW_DISCRETE = "allow-discrete"
    ALPHA = "alpha"
    ALTERNATE = "alternate"
    ALTERNATE_REVERSE = "alternate-reverse"
    ALWAYS = "always"
    ANCHORS_VALID = "anchors-valid"
    ANCHORS_VISIBLE = "anchors-visible"
    ANONYMOUS = "anonymous"
    ANYWHERE = "anywhere"
    APPWORKSPACE = "appworkspace"
    AUTO = "auto"
    AUTO_ADD = "auto-add"
    AVAR2 = "avar2"
    B4 = "b4"
    B5 = "b5"
    BACK = "back"
    BACKGROUND = "background"
    BACKWARDS = "backwards"
    BALANCE = "balance"
    BASELINE = "baseline"
    BEVEL = "bevel"
    BIDI_OVERRIDE = "bidi-override"
    BLINK = "blink"
    BLOCK = "block"
    BLOCK_END = "block-end"
    BLOCK_START = "block-start"
    BOLD = "bold"
    BOLDER = "bolder"
    BORDER_BOX = "border-box"
    BOTH = "both"
    BOTH_EDGES = "both-edges"
    BOTTOM = "bottom"
    BREAK_ALL = "break-all"
    BREAK_SPACES = "break-spaces"
    BREAK_WORD = "break-word"
    BROWSER = "browser"
    BUTT = "butt"
    BUTTON = "button"
    BUTTONBORDER = "buttonborder"
    BUTTONFACE = "buttonface"
    BUTTONHIGHLIGHT = "buttonhighlight"
    BUTTONSHADOW = "buttonshadow"
    BUTTONTEXT = "buttontext"
    CANVAS = "canvas"
    CANVASTEXT = "canvastext"
    CAPITALIZE = "capitalize"
    CAPTIONTEXT = "captiontext"
    CELL = "cell"
    CENTER = "center"
    CHECKBOX = "checkbox"
    CIRCLE = "circle"
    CLIP = "clip"
    CLOSE_QUOTE = "close-quote"
    COARSE = "coarse"
    COL_RESIZE = "col-resize"
    COLLAPSE = "collapse"
    COLOR = "color"
    COLOR_BURN = "color-burn"
    COLOR_CBDT = "color-cbdt"
    COLOR_COLRV0 = "color-colrv0"
    COLOR_COLRV1 = "color-colrv1"
    COLOR_DODGE = "color-dodge"
    COLOR_SBIX = "color-sbix"
    COLOR_SVG = "color-svg"
    COLUMN = "column"
    COLUMN_REVERSE = "column-reverse"
    COMMON_LIGATURES = "common-ligatures"
    COMPACT = "compact"
    CONDENSED = "condensed"
    CONTAIN = "contain"
    CONTENT = "content"
    CONTENT_BOX = "content-box"
    CONTENTS = "contents"
    CONTEXT_MENU = "context-menu"
    CONTEXTUAL = "contextual"
    COPY = "copy"
    COVER = "cover"
    CRISP_EDGES = "crisp-edges"
    CRISPEDGES = "crispedges"
    CROP = "crop"
    CROSS = "cross"
    CROSSHAIR = "crosshair"
    CURRENTCOLOR = "currentcolor"
    CURSIVE = "cursive"
    CUSTOM = "custom"
    DARK = "dark"
    DARKEN = "darken"
    DASHED = "dashed"
    DECIMAL = "decimal"
    DECIMAL_LEADING_ZERO = "decimal-leading-zero"
    DECREASING = "decreasing"
    DEFAULT = "default"
    DIAGONAL_FRACTIONS = "diagonal-fractions"
    DIFFERENCE = "difference"
    DISC = "disc"
    DISCARD = "discard"
    DISCARD_BEFORE = "discard-before"
    DISCARD_AFTER = "discard-after"
    DISCARD_INNER = "discard-inner"
    DISCLOSURE_CLOSED = "disclosure-closed"
    DISCLOSURE_OPEN = "disclosure-open"
    DISCRETIONARY_LIGATURES = "discretionary-ligatures"
    DISTRIBUTE = "distribute"
    DOTTED = "dotted"
    DOUBLE = "double"
    DOWN = "down"
    E = "e"
    E_RESIZE = "e-resize"
    EASE = "ease"
    EASE_IN = "ease-in"
    EASE_IN_OUT = "ease-in-out"
    EASE_OUT = "ease-out"
    ELLIPSIS = "ellipsis"
    EMBED = "embed"
    EMOJI = "emoji"
    ENABLED = "enabled"
    END = "end"
    EVENODD = "evenodd"
    EW_RESIZE = "ew-resize"
    EXCLUDE = "exclude"
    EXCLUSION = "exclusion"
    EXPANDED = "expanded"
    EXTRA_CONDENSED = "extra-condensed"
    EXTRA_EXPANDED = "extra-expanded"
    FALLBACK = "fallback"
    FALSE = "false"
    FANTASY = "fantasy"
    FAST = "fast"
    FEATURES_AAT = "features-aat"
    FEATURES_GRAPHITE = "features-graphite"
    FEATURES_OPENTYPE = "features-opentype"
    FIELD = "field"
    FIELDTEXT = "fieldtext"
    FILL = "fill"
    FILL_BOX = "fill-box"
    FINE = "fine"
    FIXED = "fixed"
    FLAT = "flat"
    FLEX = "flex"
    FLEX_END = "flex-end"
    FLEX_START = "flex-start"
    FLIP_BLOCK = "flip-block"
    FLIP_INLINE = "flip-inline"
    FLIP_START = "flip-start"
    FLOW = "flow"
    FLOW_ROOT = "flow-root"
    FORWARDS = "forwards"
    FROM_FONT = "from-font"
    FULL_SIZE_KANA = "full-size-kana"
    FULL_WIDTH = "full-width"
    FULLSCREEN = "fullscreen"
    GEOMETRICPRECISION = "geometricprecision"
    GRAB = "grab"
    GRABBING = "grabbing"
    GRAMMAR_ERROR = "grammar-error"
    GRAYTEXT = "graytext"
    GRID = "grid"
    GROOVE = "groove"
    HARD_LIGHT = "hard-light"
    HEIGHT = "height"
    HELP = "help"
    HIDE = "hide"
    HIDDEN = "hidden"
    HIGH = "high"
    HIGH_QUALITY = "high-quality"
    HIGHLIGHT = "highlight"
    HIGHLIGHTTEXT = "highlighttext"
    HISTORICAL_FORMS = "historical-forms"
    HISTORICAL_LIGATURES = "historical-ligatures"
    HORIZONTAL_TB = "horizontal-tb"
    HOVER = "hover"
    HSL = "hsl"
    HUE = "hue"
    HWB = "hwb"
    INACTIVEBORDER = "inactiveborder"
    INACTIVECAPTION = "inactivecaption"
    INACTIVECAPTIONTEXT = "inactivecaptiontext"
    INCREASING = "increasing"
    INCREMENTAL = "incremental"
    INFINITE = "infinite"
    INFINITY = "infinity"
    INFOBACKGROUND = "infobackground"
    INFOTEXT = "infotext"
    INHERIT = "inherit"
    INITIAL = "initial"
    INITIAL_ONLY = "initial-only"
    INLINE = "inline"
    INLINE_BLOCK = "inline-block"
    INLINE_END = "inline-end"
    INLINE_FLEX = "inline-flex"
    INLINE_GRID = "inline-grid"
    INLINE_SIZE = "inline-size"
    INLINE_START = "inline-start"
    INLINE_TABLE = "inline-table"
    INSET = "inset"
    INSIDE = "inside"
    INTER_CHARACTER = "inter-character"
    INTER_WORD = "inter-word"
    INTERLACE = "interlace"
    INTERSECT = "intersect"
    INVERT = "invert"
    INVERTED = "inverted"
    ISOLATE = "isolate"
    ISOLATE_OVERRIDE = "isolate-override"
    ITALIC = "italic"
    JIS_B4 = "jis-b4"
    JIS_B5 = "jis-b5"
    JIS04 = "jis04"
    JIS78 = "jis78"
    JIS83 = "jis83"
    JIS90 = "jis90"
    JUMP_BOTH = "jump-both"
    JUMP_END = "jump-end"
    JUMP_NONE = "jump-none"
    JUMP_START = "jump-start"
    JUSTIFY = "justify"
    KEEP_ALL = "keep-all"
    LANDSCAPE = "landscape"
    LARGE = "large"
    LARGER = "larger"
    LAYOUT = "layout"
    LCH = "lch"
    LEDGER = "ledger"
    LEFT = "left"
    LEGACY = "legacy"
    LEGAL = "legal"
    LESS = "less"
    LETTER = "letter"
    LIGHT = "light"
    LIGHTEN = "lighten"
    LIGHTER = "lighter"
    LINE_THROUGH = "line-through"
    LINEAR = "linear"
    LINEARRGB = "linearRGB"
    LINING_NUMS = "lining-nums"
    LINKTEXT = "linktext"
    LIST_ITEM = "list-item"
    LISTBOX = "listbox"
    LOCAL = "local"
    LONGER = "longer"
    LOWER_ALPHA = "lower-alpha"
    LOWER_GREEK = "lower-greek"
    LOWER_LATIN = "lower-latin"
    LOWER_ROMAN = "lower-roman"
    LOWERCASE = "lowercase"
    LTR = "ltr"
    LUMINANCE = "luminance"
    LUMINOSITY = "luminosity"
    MANIPULATION = "manipulation"
    MANUAL = "manual"
    MARGIN_BOX = "margin-box"
    MARK = "mark"
    MARKERS = "markers"
    MARKTEXT = "marktext"
    MATCH_PARENT = "match-parent"
    MATCH_SOURCE = "match-source"
    MATH = "math"
    MATH_AUTO = "math-auto"
    MAX_CONTENT = "max-content"
    MEDIUM = "medium"
    MENU = "menu"
    MENULIST = "menulist"
    MENULIST_BUTTON = "menulist-button"
    MENUTEXT = "menutext"
    METER = "meter"
    MIDDLE = "middle"
    MIN_CONTENT = "min-content"
    MINIMAL_UI = "minimal-ui"
    MITER = "miter"
    MONOSPACE = "monospace"
    MORE = "more"
    MOST_BLOCK_SIZE = "most-block-size"
    MOST_HEIGHT = "most-height"
    MOST_INLINE_SIZE = "most-inline-size"
    MOST_WIDTH = "most-width"
    MOVE = "move"
    MULTIPLY = "multiply"
    N_RESIZE = "n-resize"
    NAN = "nan"
    NE_RESIZE = "ne-resize"
    NEAREST = "nearest"
    NESW_RESIZE = "nesw-resize"
    NO_CLIP = "no-clip"
    NO_CLOSE_QUOTE = "no-close-quote"
    NO_COMMON_LIGATURES = "no-common-ligatures"
    NO_CONTEXTUAL = "no-contextual"
    NO_DISCRETIONARY_LIGATURES = "no-discretionary-ligatures"
    NO_DROP = "no-drop"
    NO_HISTORICAL_LIGATURES = "no-historical-ligatures"
    NO_OPEN_QUOTE = "no-open-quote"
    NO_OVERFLOW = "no-overflow"
    NO_PREFERENCE = "no-preference"
    NO_REFERRER = "no-referrer"
    NO_REFERRER_WHEN_DOWNGRADE = "no-referrer-when-downgrade"
    NO_REPEAT = "no-repeat"
    NONE = "none"
    NONZERO = "nonzero"
    NORMAL = "normal"
    NOT_ALLOWED = "not-allowed"
    NOTCH = "notch"
    NOWRAP = "nowrap"
    NS_RESIZE = "ns-resize"
    NW_RESIZE = "nw-resize"
    NWSE_RESIZE = "nwse-resize"
    OBLIQUE = "oblique"
    OFF = "off"
    OKLCH = "oklch"
    OLDSTYLE_NUMS = "oldstyle-nums"
    ON = "on"
    OPAQUE = "opaque"
    OPEN_QUOTE = "open-quote"
    OPTIMIZELEGIBILITY = "optimizelegibility"
    OPTIMIZEQUALITY = "optimizequality"
    OPTIMIZESPEED = "optimizespeed"
    OPTIONAL = "optional"
    ORDINAL = "ordinal"
    ORIGIN = "origin"
    ORIGIN_WHEN_CROSS_ORIGIN = "origin-when-cross-origin"
    OUTSET = "outset"
    OUTSIDE = "outside"
    OVERLAY = "overlay"
    OVERLINE = "overline"
    P3 = "p3"
    PADDING_BOX = "padding-box"
    PAGED = "paged"
    PAINT = "paint"
    PALETTES = "palettes"
    PAN_DOWN = "pan-down"
    PAN_LEFT = "pan-left"
    PAN_RIGHT = "pan-right"
    PAN_UP = "pan-up"
    PAN_X = "pan-x"
    PAN_Y = "pan-y"
    PAUSED = "paused"
    PETITE_CAPS = "petite-caps"
    PI = "pi"
    PICTURE_IN_PICTURE = "picture-in-picture"
    PIXELATED = "pixelated"
    PLAINTEXT = "plaintext"
    PLUS_DARKER = "plus-darker"
    PLUS_LIGHTER = "plus-lighter"
    POINTER = "pointer"
    PORTRAIT = "portrait"
    PRE = "pre"
    PRE_LINE = "pre-line"
    PRE_WRAP = "pre-wrap"
    PRESERVE = "preserve"
    PRESERVE3D = "preserve3d"
    PRESERVE_BREAKS = "preserve-breaks"
    PRESERVE_SPACES = "preserve-spaces"
    PRETTY = "pretty"
    PROGRESS = "progress"
    PROGRESS_BAR = "progress-bar"
    PROGRESSIVE = "progressive"
    PROPORTIONAL_NUMS = "proportional-nums"
    PROPORTIONAL_WIDTH = "proportional-width"
    PUSH_BUTTON = "push-button"
    RADIO = "radio"
    REC2020 = "rec2020"
    REDUCE = "reduce"
    RELATIVE = "relative"
    REPEAT = "repeat"
    REPEAT_X = "repeat-x"
    REPEAT_Y = "repeat-y"
    REPLACE = "replace"
    REVERSE = "reverse"
    REVERT = "revert"
    REVERT_LAYER = "revert-layer"
    RIDGE = "ridge"
    RIGHT = "right"
    ROTATE_LEFT = "rotate-left"
    ROTATE_RIGHT = "rotate-right"
    ROUND = "round"
    ROW = "row"
    ROW_RESIZE = "row-resize"
    ROW_REVERSE = "row-reverse"
    RTL = "rtl"
    RUBY = "ruby"
    RUBY_BASE = "ruby-base"
    RUBY_BASE_CONTAINER = "ruby-base-container"
    RUBY_TEXT = "ruby-text"
    RUBY_TEXT_CONTAINER = "ruby-text-container"
    RUN_IN = "run-in"
    RUNNING = "running"
    S_RESIZE = "s-resize"
    SAFE = "safe"
    SAME_ORIGIN = "same-origin"
    SANS_SERIF = "sans-serif"
    SATURATION = "saturation"
    SCALE_DOWN = "scale-down"
    SCOOP = "scoop"
    SCREEN = "screen"
    SCROLL = "scroll"
    SCROLL_POSITION = "scroll-position"
    SCROLL_STATE = "scroll-state"
    SCROLLBAR = "scrollbar"
    SE_RESIZE = "se-resize"
    SEARCHFIELD = "searchfield"
    SELECTEDITEM = "selecteditem"
    SELECTEDITEMTEXT = "selecteditemtext"
    SELF_BLOCK = "self-block"
    SELF_BLOCK_END = "self-block-end"
    SELF_BLOCK_START = "self-block-start"
    SELF_END = "self-end"
    SELF_INLINE = "self-inline"
    SELF_INLINE_END = "self-inline-end"
    SELF_INLINE_START = "self-inline-start"
    SELF_X_END = "self-x-end"
    SELF_X_START = "self-x-start"
    SELF_Y_END = "self-y-end"
    SELF_Y_START = "self-y-start"
    SELF_START = "self-start"
    SEMI_CONDENSED = "semi-condensed"
    SEMI_EXPANDED = "semi-expanded"
    SEPARATE = "separate"
    SERIF = "serif"
    SHORTER = "shorter"
    SHOW = "show"
    SIDEWAYS_LR = "sideways-lr"
    SIDEWAYS_RL = "sideways-rl"
    SIMPLIFIED = "simplified"
    SIZE = "size"
    SLASHED_ZERO = "slashed-zero"
    SLIDER_HORIZONTAL = "slider-horizontal"
    SLOW = "slow"
    SMALL = "small"
    SMALL_CAPS = "small-caps"
    SMALLER = "smaller"
    SMOOTH = "smooth"
    SOFT_LIGHT = "soft-light"
    SOLID = "solid"
    SPACE = "space"
    SPACE_AROUND = "space-around"
    SPACE_BETWEEN = "space-between"
    SPACE_EVENLY = "space-evenly"
    SPAN_ALL = "span-all"
    SPAN_BLOCK_END = "span-block-end"
    SPAN_BLOCK_START = "span-block-start"
    SPAN_BOTTOM = "span-bottom"
    SPAN_END = "span-end"
    SPAN_INLINE_END = "span-inline-end"
    SPAN_INLINE_START = "span-inline-start"
    SPAN_LEFT = "span-left"
    SPAN_RIGHT = "span-right"
    SPAN_SELF_BLOCK_END = "span-self-block-end"
    SPAN_SELF_BLOCK_START = "span-self-block-start"
    SPAN_SELF_END = "span-self-end"
    SPAN_SELF_INLINE_END = "span-self-inline-end"
    SPAN_SELF_INLINE_START = "span-self-inline-start"
    SPAN_SELF_START = "span-self-start"
    SPAN_SELF_X_END = "span-self-x-end"
    SPAN_SELF_X_START = "span-self-x-start"
    SPAN_SELF_Y_END = "span-self-y-end"
    SPAN_SELF_Y_START = "span-self-y-start"
    SPAN_START = "span-start"
    SPAN_TOP = "span-top"
    SPAN_X_END = "span-x-end"
    SPAN_X_START = "span-x-start"
    SPAN_Y_END = "span-y-end"
    SPAN_Y_START = "span-y-start"
    SPELLING_ERROR = "spelling-error"
    SQUARE = "square"
    SQUARE_BUTTON = "square-button"
    SQUIRCLE = "squircle"
    SRGB = "srgb"
    STABLE = "stable"
    STACKED_FRACTIONS = "stacked-fractions"
    STANDALONE = "standalone"
    STANDARD = "standard"
    START = "start"
    STATIC = "static"
    STICKY = "sticky"
    STRETCH = "stretch"
    STRICT = "strict"
    STRICT_ORIGIN = "strict-origin"
    STRICT_ORIGIN_WHEN_CROSS_ORIGIN = "strict-origin-when-cross-origin"
    STROKE = "stroke"
    STROKE_BOX = "stroke-box"
    STYLE = "style"
    SUB = "sub"
    SUBTRACT = "subtract"
    SUBTRACTIVE = "subtractive"
    SUPER = "super"
    SW_RESIZE = "sw-resize"
    SWAP = "swap"
    TABLE = "table"
    TABLE_CAPTION = "table-caption"
    TABLE_CELL = "table-cell"
    TABLE_COLUMN = "table-column"
    TABLE_COLUMN_GROUP = "table-column-group"
    TABLE_FOOTER_GROUP = "table-footer-group"
    TABLE_HEADER_GROUP = "table-header-group"
    TABLE_ROW = "table-row"
    TABLE_ROW_GROUP = "table-row-group"
    TABULAR_NUMS = "tabular-nums"
    TEXT = "text"
    TEXT_BOTTOM = "text-bottom"
    TEXT_TOP = "text-top"
    TEXTAREA = "textarea"
    TEXTFIELD = "textfield"
    THICK = "thick"
    THIN = "thin"
    THREEDDARKSHADOW = "threeddarkshadow"
    THREEDFACE = "threedface"
    THREEDHIGHLIGHT = "threedhighlight"
    THREEDLIGHTSHADOW = "threedlightshadow"
    THREEDSHADOW = "threedshadow"
    TITLING_CAPS = "titling-caps"
    TO_ZERO = "to-zero"
    TOP = "top"
    TRADITIONAL = "traditional"
    TRUE = "true"
    UI_MONOSPACE = "ui-monospace"
    UI_ROUNDED = "ui-rounded"
    UI_SANS_SERIF = "ui-sans-serif"
    UI_SERIF = "ui-serif"
    ULTRA_CONDENSED = "ultra-condensed"
    ULTRA_EXPANDED = "ultra-expanded"
    UNDER = "under"
    UNDERLINE = "underline"
    UNICASE = "unicase"
    UNICODE = "unicode"
    UNSAFE = "unsafe"
    UNSAFE_URL = "unsafe-url"
    UNSET = "unset"
    UP = "up"
    UPPER_ALPHA = "upper-alpha"
    UPPER_LATIN = "upper-latin"
    UPPER_ROMAN = "upper-roman"
    UPPERCASE = "uppercase"
    UPRIGHT = "upright"
    USE_CREDENTIALS = "use-credentials"
    VARIATIONS = "variations"
    VERTICAL_LR = "vertical-lr"
    VERTICAL_RL = "vertical-rl"
    VERTICAL_TEXT = "vertical-text"
    VIEW_BOX = "view-box"
    VISIBLE = "visible"
    VISITEDTEXT = "visitedtext"
    W_RESIZE = "w-resize"
    WAIT = "wait"
    WAVY = "wavy"
    WIDTH = "width"
    WINDOW = "window"
    WINDOWFRAME = "windowframe"
    WINDOWTEXT = "windowtext"
    WRAP = "wrap"
    WRAP_REVERSE = "wrap-reverse"
    X_END = "x-end"
    X_LARGE = "x-large"
    X_START = "x-start"
    X_SMALL = "x-small"
    XX_LARGE = "xx-large"
    XX_SMALL = "xx-small"
    XXX_LARGE = "xxx-large"
    Y_END = "y-end"
    Y_START = "y-start"
    ZOOM_IN = "zoom-in"
    ZOOM_OUT = "zoom-out"


class KeywordGroup:
    pass


class AbsoluteSize(KeywordGroup, Enum):
    XX_SMALL = "xx-small"
    X_SMALL = "x-small"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    X_LARGE = "x-large"
    XX_LARGE = "xx-large"
    XXX_LARGE = "xxx-large"

FONT_SIZE_SCALING_TABLE = {
    AbsoluteSize.XX_SMALL: 9,
    AbsoluteSize.X_SMALL: 10,
    AbsoluteSize.SMALL: 13,
    AbsoluteSize.MEDIUM: 16,
    AbsoluteSize.LARGE: 18,
    AbsoluteSize.X_LARGE: 24,
    AbsoluteSize.XX_LARGE: 32,
    AbsoluteSize.XXX_LARGE: 48
}

FONT_SIZE_STEPS = [9, 10, 13, 16, 18, 24, 32, 48]


def larger_size(base_size: float):
    for size in FONT_SIZE_STEPS:
        if size > base_size:
            return size
    return base_size * 1.2


def smaller_size(base_size: float):
    for size in reversed(FONT_SIZE_STEPS):
        if size < base_size:
            return size
    return 9 # FIXME: decide whether to avoid smaller than 9px fonts


class AlignContent(KeywordGroup, Enum):
    NORMAL = "normal"
    START = "start"
    FLEX_START = "flex-start"
    END = "end"
    FLEX_END = "flex-end"
    CENTER = "center"
    SPACE_BETWEEN = "space-between"
    SPACE_AROUND = "space-around"
    SPACE_EVENLY = "space-evenly"
    STRETCH = "stretch"


class AlignItems(KeywordGroup, Enum):
    BASELINE = "baseline"
    CENTER = "center"
    END = "end"
    FLEX_END = "flex-end"
    FLEX_START = "flex-start"
    NORMAL = "normal"
    SAFE = "safe"
    SELF_END = "self-end"
    SELF_START = "self-start"
    START = "start"
    STRETCH = "stretch"
    UNSAFE = "unsafe"


class AlignSelf(KeywordGroup, Enum):
    AUTO = "auto"
    BASELINE = "baseline"
    CENTER = "center"
    END = "end"
    FLEX_END = "flex-end"
    FLEX_START = "flex-start"
    NORMAL = "normal"
    SAFE = "safe"
    SELF_END = "self-end"
    SELF_START = "self-start"
    START = "start"
    STRETCH = "stretch"
    UNSAFE = "unsafe"


class AnchorSide(KeywordGroup, Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"
    TOP = "top"
    LEFT = "left"
    RIGHT = "right"
    BOTTOM = "bottom"
    START = "start"
    END = "end"
    SELF_START = "self-start"
    SELF_END = "self-end"
    CENTER = "center"


class AnchorSize(KeywordGroup, Enum):
    BLOCK = "block"
    HEIGHT = "height"
    INLINE = "inline"
    SELF_BLOCK = "self-block"
    SELF_INLINE = "self-inline"
    WIDTH = "width"


class AnimationComposition(KeywordGroup, Enum):
    REPLACE = "replace"
    ADD = "add"
    ACCUMULATE = "accumulate"


class AnimationDirection(KeywordGroup, Enum):
    ALTERNATE = "alternate"
    ALTERNATE_REVERSE = "alternate-reverse"
    NORMAL = "normal"
    REVERSE = "reverse"


class AnimationFillMode(KeywordGroup, Enum):
    BACKWARDS = "backwards"
    BOTH = "both"
    FORWARDS = "forwards"
    NONE = "none"


class AnimationPlayState(KeywordGroup, Enum):
    PAUSED = "paused"
    RUNNING = "running"


class Appearance(KeywordGroup, Enum):
    AUTO = "auto"
    BUTTON = "button"
    CHECKBOX = "checkbox"
    LISTBOX = "listbox"
    MENULIST = "menulist"
    METER = "meter"
    MENULIST_BUTTON = "menulist-button"
    NONE = "none"
    PUSH_BUTTON = "push-button"
    PROGRESS_BAR = "progress-bar"
    RADIO = "radio"
    SEARCHFIELD = "searchfield"
    SLIDER_HORIZONTAL = "slider-horizontal"
    SQUARE_BUTTON = "square-button"
    TEXTAREA = "textarea"
    TEXTFIELD = "textfield"


class BackgroundAttachment(KeywordGroup, Enum):
    FIXED = "fixed"
    LOCAL = "local"
    SCROLL = "scroll"


class BackgroundBox(KeywordGroup, Enum):
    BORDER_BOX = "border-box"
    CONTENT_BOX = "content-box"
    PADDING_BOX = "padding-box"
    TEXT = "text"


class BorderCollapse(KeywordGroup, Enum):
    SEPARATE = "separate"
    COLLAPSE = "collapse"


class BorderImageRepeat(KeywordGroup, Enum):
    STRETCH = "stretch"
    REPEAT = "repeat"
    ROUND = "round"
    SPACE = "space"


class BoxSizing(KeywordGroup, Enum):
    BORDER_BOX = "border-box"
    CONTENT_BOX = "content-box"


class CaptionSide(KeywordGroup, Enum):
    TOP = "top"
    BOTTOM = "bottom"


class Clear(KeywordGroup, Enum):
    NONE = "none"
    LEFT = "left"
    RIGHT = "right"
    BOTH = "both"
    INLINE_START = "inline-start"
    INLINE_END = "inline-end"


class ColorInterpolation(KeywordGroup, Enum):
    AUTO = "auto"
    LINEARRGB = "linearRGB"
    SRGB = "srgb"


class ColumnSpan(KeywordGroup, Enum):
    NONE = "none"
    ALL = "all"


class CompositingOperator(KeywordGroup, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    INTERSECT = "intersect"
    EXCLUDE = "exclude"


class Contain(KeywordGroup, Enum):
    NONE = "none"
    STRICT = "strict"
    CONTENT = "content"
    SIZE = "size"
    INLINE_SIZE = "inline-size"
    LAYOUT = "layout"
    STYLE = "style"
    PAINT = "paint"


class ContentVisibility(KeywordGroup, Enum):
    VISIBLE = "visible"
    AUTO = "auto"
    HIDDEN = "hidden"


class CoordBox(KeywordGroup, Enum):
    CONTENT_BOX = "content-box"
    PADDING_BOX = "padding-box"
    BORDER_BOX = "border-box"
    FILL_BOX = "fill-box"
    STROKE_BOX = "stroke-box"
    VIEW_BOX = "view-box"


class CounterStyleNameKeyword(KeywordGroup, Enum):
    CIRCLE = "circle"
    DECIMAL = "decimal"
    DECIMAL_LEADING_ZERO = "decimal-leading-zero"
    DISC = "disc"
    DISCLOSURE_CLOSED = "disclosure-closed"
    DISCLOSURE_OPEN = "disclosure-open"
    LOWER_ALPHA = "lower-alpha"
    LOWER_GREEK = "lower-greek"
    LOWER_LATIN = "lower-latin"
    LOWER_ROMAN = "lower-roman"
    NONE = "none"
    SQUARE = "square"
    UPPER_ALPHA = "upper-alpha"
    UPPER_LATIN = "upper-latin"
    UPPER_ROMAN = "upper-roman"


class CrossOriginModifierValue(KeywordGroup, Enum):
    ANONYMOUS = "anonymous"
    USE_CREDENTIALS = "use-credentials"


class CursorPredefined(KeywordGroup, Enum):
    AUTO = "auto"
    DEFAULT = "default"
    NONE = "none"
    CONTEXT_MENU = "context-menu"
    HELP = "help"
    POINTER = "pointer"
    PROGRESS = "progress"
    WAIT = "wait"
    CELL = "cell"
    CROSSHAIR = "crosshair"
    TEXT = "text"
    VERTICAL_TEXT = "vertical-text"
    ALIAS = "alias"
    COPY = "copy"
    MOVE = "move"
    NO_DROP = "no-drop"
    NOT_ALLOWED = "not-allowed"
    GRAB = "grab"
    GRABBING = "grabbing"
    E_RESIZE = "e-resize"
    N_RESIZE = "n-resize"
    NE_RESIZE = "ne-resize"
    NW_RESIZE = "nw-resize"
    S_RESIZE = "s-resize"
    SE_RESIZE = "se-resize"
    SW_RESIZE = "sw-resize"
    W_RESIZE = "w-resize"
    EW_RESIZE = "ew-resize"
    NS_RESIZE = "ns-resize"
    NESW_RESIZE = "nesw-resize"
    NWSE_RESIZE = "nwse-resize"
    COL_RESIZE = "col-resize"
    ROW_RESIZE = "row-resize"
    ALL_SCROLL = "all-scroll"
    ZOOM_IN = "zoom-in"
    ZOOM_OUT = "zoom-out"


class Direction(KeywordGroup, Enum):
    LTR = "ltr"
    RTL = "rtl"


class DisplayBox(KeywordGroup, Enum):
    CONTENTS = "contents"
    NONE = "none"


class DisplayInside(KeywordGroup, Enum):
    FLOW = "flow"
    FLOW_ROOT = "flow-root"
    TABLE = "table"
    FLEX = "flex"
    GRID = "grid"
    RUBY = "ruby"
    MATH = "math"


class DisplayInternal(KeywordGroup, Enum):
    TABLE_ROW_GROUP = "table-row-group"
    TABLE_HEADER_GROUP = "table-header-group"
    TABLE_FOOTER_GROUP = "table-footer-group"
    TABLE_ROW = "table-row"
    TABLE_CELL = "table-cell"
    TABLE_COLUMN_GROUP = "table-column-group"
    TABLE_COLUMN = "table-column"
    TABLE_CAPTION = "table-caption"
    RUBY_BASE = "ruby-base"
    RUBY_TEXT = "ruby-text"
    RUBY_BASE_CONTAINER = "ruby-base-container"
    RUBY_TEXT_CONTAINER = "ruby-text-container"


class DisplayLegacy(KeywordGroup, Enum):
    INLINE_BLOCK = "inline-block"
    INLINE_TABLE = "inline-table"
    INLINE_FLEX = "inline-flex"
    INLINE_GRID = "inline-grid"


class DisplayOutside(KeywordGroup, Enum):
    BLOCK = "block"
    INLINE = "inline"
    RUN_IN = "run-in"


class EasingKeyword(KeywordGroup, Enum):
    LINEAR = "linear"
    EASE = "ease"
    EASE_IN = "ease-in"
    EASE_OUT = "ease-out"
    EASE_IN_OUT = "ease-in-out"


class EmptyCells(KeywordGroup, Enum):
    SHOW = "show"
    HIDE = "hide"


class FillRule(KeywordGroup, Enum):
    NONZERO = "nonzero"
    EVENODD = "evenodd"


class FlexDirection(KeywordGroup, Enum):
    ROW = "row"
    ROW_REVERSE = "row-reverse"
    COLUMN = "column"
    COLUMN_REVERSE = "column-reverse"


class FlexWrap(KeywordGroup, Enum):
    NOWRAP = "nowrap"
    WRAP = "wrap"
    WRAP_REVERSE = "wrap-reverse"


class Float(KeywordGroup, Enum):
    NONE = "none"
    LEFT = "left"
    RIGHT = "right"
    INLINE_START = "inline-start"
    INLINE_END = "inline-end"


class FontDisplay(KeywordGroup, Enum):
    AUTO = "auto"
    BLOCK = "block"
    SWAP = "swap"
    FALLBACK = "fallback"
    OPTIONAL = "optional"


class FontKerning(KeywordGroup, Enum):
    AUTO = "auto"
    NORMAL = "normal"
    NONE = "none"


class FontStyle(KeywordGroup, Enum):
    NORMAL = "normal"
    ITALIC = "italic"
    LEFT = "left"
    RIGHT = "right"
    OBLIQUE = "oblique"


class FontTech(KeywordGroup, Enum):
    AVAR2 = "avar2"
    COLOR_CBDT = "color-cbdt"
    COLOR_COLRV0 = "color-colrv0"
    COLOR_COLRV1 = "color-colrv1"
    COLOR_SBIX = "color-sbix"
    COLOR_SVG = "color-svg"
    FEATURES_AAT = "features-aat"
    FEATURES_GRAPHITE = "features-graphite"
    FEATURES_OPENTYPE = "features-opentype"
    INCREMENTAL = "incremental"
    PALETTES = "palettes"
    VARIATIONS = "variations"


class FontVariantAlternates(KeywordGroup, Enum):
    NORMAL = "normal"
    HISTORICAL_FORMS = "historical-forms"


class FontVariantCaps(KeywordGroup, Enum):
    NORMAL = "normal"
    SMALL_CAPS = "small-caps"
    ALL_SMALL_CAPS = "all-small-caps"
    PETITE_CAPS = "petite-caps"
    ALL_PETITE_CAPS = "all-petite-caps"
    UNICASE = "unicase"
    TITLING_CAPS = "titling-caps"


class FontVariantEastAsian(KeywordGroup, Enum):
    NORMAL = "normal"
    RUBY = "ruby"
    JIS78 = "jis78"
    JIS83 = "jis83"
    JIS90 = "jis90"
    JIS04 = "jis04"
    SIMPLIFIED = "simplified"
    TRADITIONAL = "traditional"
    FULL_WIDTH = "full-width"
    PROPORTIONAL_WIDTH = "proportional-width"


class FontVariantEmoji(KeywordGroup, Enum):
    NORMAL = "normal"
    TEXT = "text"
    EMOJI = "emoji"
    UNICODE = "unicode"


class FontVariantLigatures(KeywordGroup, Enum):
    NORMAL = "normal"
    NONE = "none"
    COMMON_LIGATURES = "common-ligatures"
    NO_COMMON_LIGATURES = "no-common-ligatures"
    DISCRETIONARY_LIGATURES = "discretionary-ligatures"
    NO_DISCRETIONARY_LIGATURES = "no-discretionary-ligatures"
    HISTORICAL_LIGATURES = "historical-ligatures"
    NO_HISTORICAL_LIGATURES = "no-historical-ligatures"
    CONTEXTUAL = "contextual"
    NO_CONTEXTUAL = "no-contextual"


class FontVariantNumeric(KeywordGroup, Enum):
    NORMAL = "normal"
    ORDINAL = "ordinal"
    SLASHED_ZERO = "slashed-zero"
    LINING_NUMS = "lining-nums"
    OLDSTYLE_NUMS = "oldstyle-nums"
    PROPORTIONAL_NUMS = "proportional-nums"
    TABULAR_NUMS = "tabular-nums"
    DIAGONAL_FRACTIONS = "diagonal-fractions"
    STACKED_FRACTIONS = "stacked-fractions"


class FontVariantPosition(KeywordGroup, Enum):
    NORMAL = "normal"
    SUB = "sub"
    SUPER = "super"


class FontWidth(KeywordGroup, Enum):
    ULTRA_CONDENSED = "ultra-condensed"
    EXTRA_CONDENSED = "extra-condensed"
    CONDENSED = "condensed"
    SEMI_CONDENSED = "semi-condensed"
    NORMAL = "normal"
    SEMI_EXPANDED = "semi-expanded"
    EXPANDED = "expanded"
    EXTRA_EXPANDED = "extra-expanded"
    ULTRA_EXPANDED = "ultra-expanded"


class GenericFontFamily(KeywordGroup, Enum):
    SERIF = "serif"
    SANS_SERIF = "sans-serif"
    CURSIVE = "cursive"
    FANTASY = "fantasy"
    MONOSPACE = "monospace"
    MATH = "math"
    UI_SERIF = "ui-serif"
    UI_SANS_SERIF = "ui-sans-serif"
    UI_MONOSPACE = "ui-monospace"
    UI_ROUNDED = "ui-rounded"


class HueInterpolationMethod(KeywordGroup, Enum):
    SHORTER = "shorter"
    LONGER = "longer"
    INCREASING = "increasing"
    DECREASING = "decreasing"


class ImageRendering(KeywordGroup, Enum):
    AUTO = "auto"
    CRISP_EDGES = "crisp-edges"
    HIGH_QUALITY = "high-quality"
    PIXELATED = "pixelated"
    SMOOTH = "smooth"


class Isolation(KeywordGroup, Enum):
    AUTO = "auto"
    ISOLATE = "isolate"


class JustifyContent(KeywordGroup, Enum):
    NORMAL = "normal"
    START = "start"
    END = "end"
    FLEX_START = "flex-start"
    FLEX_END = "flex-end"
    CENTER = "center"
    SPACE_BETWEEN = "space-between"
    SPACE_AROUND = "space-around"
    SPACE_EVENLY = "space-evenly"
    STRETCH = "stretch"
    LEFT = "left"
    RIGHT = "right"


class JustifyItems(KeywordGroup, Enum):
    BASELINE = "baseline"
    CENTER = "center"
    END = "end"
    FLEX_END = "flex-end"
    FLEX_START = "flex-start"
    LEGACY = "legacy"
    NORMAL = "normal"
    SAFE = "safe"
    SELF_END = "self-end"
    SELF_START = "self-start"
    START = "start"
    STRETCH = "stretch"
    UNSAFE = "unsafe"
    LEFT = "left"
    RIGHT = "right"


class JustifySelf(KeywordGroup, Enum):
    AUTO = "auto"
    BASELINE = "baseline"
    CENTER = "center"
    END = "end"
    FLEX_END = "flex-end"
    FLEX_START = "flex-start"
    NORMAL = "normal"
    SAFE = "safe"
    SELF_END = "self-end"
    SELF_START = "self-start"
    START = "start"
    STRETCH = "stretch"
    UNSAFE = "unsafe"
    LEFT = "left"
    RIGHT = "right"


class LineStyle(KeywordGroup, Enum):
    NONE = "none"
    HIDDEN = "hidden"
    DOTTED = "dotted"
    DASHED = "dashed"
    SOLID = "solid"
    DOUBLE = "double"
    GROOVE = "groove"
    RIDGE = "ridge"
    INSET = "inset"
    OUTSET = "outset"


class LineWidth(KeywordGroup, Enum):
    THIN = "thin"
    MEDIUM = "medium"
    THICK = "thick"


class ListStylePosition(KeywordGroup, Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"


class MaskType(KeywordGroup, Enum):
    LUMINANCE = "luminance"
    ALPHA = "alpha"


class MaskingMode(KeywordGroup, Enum):
    ALPHA = "alpha"
    LUMINANCE = "luminance"
    MATCH_SOURCE = "match-source"


class MathShift(KeywordGroup, Enum):
    NORMAL = "normal"
    COMPACT = "compact"


class MathStyle(KeywordGroup, Enum):
    NORMAL = "normal"
    COMPACT = "compact"


class MixBlendMode(KeywordGroup, Enum):
    NORMAL = "normal"
    MULTIPLY = "multiply"
    SCREEN = "screen"
    OVERLAY = "overlay"
    DARKEN = "darken"
    LIGHTEN = "lighten"
    COLOR_DODGE = "color-dodge"
    COLOR_BURN = "color-burn"
    HARD_LIGHT = "hard-light"
    SOFT_LIGHT = "soft-light"
    DIFFERENCE = "difference"
    EXCLUSION = "exclusion"
    HUE = "hue"
    SATURATION = "saturation"
    COLOR = "color"
    LUMINOSITY = "luminosity"
    PLUS_DARKER = "plus-darker"
    PLUS_LIGHTER = "plus-lighter"


class ObjectFit(KeywordGroup, Enum):
    FILL = "fill"
    CONTAIN = "contain"
    COVER = "cover"
    NONE = "none"
    SCALE_DOWN = "scale-down"


class OutlineStyle(KeywordGroup, Enum):
    AUTO = "auto"
    NONE = "none"
    DOTTED = "dotted"
    DASHED = "dashed"
    SOLID = "solid"
    DOUBLE = "double"
    GROOVE = "groove"
    RIDGE = "ridge"
    INSET = "inset"
    OUTSET = "outset"


class Overflow(KeywordGroup, Enum):
    AUTO = "auto"
    CLIP = "clip"
    HIDDEN = "hidden"
    SCROLL = "scroll"
    VISIBLE = "visible"


class PageSize(KeywordGroup, Enum):
    A5 = "a5"
    A4 = "a4"
    A3 = "a3"
    B5 = "b5"
    B4 = "b4"
    JIS_B5 = "jis-b5"
    JIS_B4 = "jis-b4"
    LETTER = "letter"
    LEGAL = "legal"
    LEDGER = "ledger"


class PaintOrder(KeywordGroup, Enum):
    FILL = "fill"
    STROKE = "stroke"
    MARKERS = "markers"


class PointerEvents(KeywordGroup, Enum):
    AUTO = "auto"
    ALL = "all"
    NONE = "none"


class PolarColorSpace(KeywordGroup, Enum):
    HSL = "hsl"
    HWB = "hwb"
    LCH = "lch"
    OKLCH = "oklch"


class PositionArea(KeywordGroup, Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    SPAN_LEFT = "span-left"
    SPAN_RIGHT = "span-right"
    X_START = "x-start"
    X_END = "x-end"
    SPAN_X_START = "span-x-start"
    SPAN_X_END = "span-x-end"
    SELF_X_START = "self-x-start"
    SELF_X_END = "self-x-end"
    SPAN_SELF_X_START = "span-self-x-start"
    SPAN_SELF_X_END = "span-self-x-end"
    SPAN_ALL = "span-all"
    TOP = "top"
    BOTTOM = "bottom"
    SPAN_TOP = "span-top"
    SPAN_BOTTOM = "span-bottom"
    Y_START = "y-start"
    Y_END = "y-end"
    SPAN_Y_START = "span-y-start"
    SPAN_Y_END = "span-y-end"
    SELF_Y_START = "self-y-start"
    SELF_Y_END = "self-y-end"
    SPAN_SELF_Y_START = "span-self-y-start"
    SPAN_SELF_Y_END = "span-self-y-end"
    BLOCK_START = "block-start"
    BLOCK_END = "block-end"
    SPAN_BLOCK_START = "span-block-start"
    SPAN_BLOCK_END = "span-block-end"
    INLINE_START = "inline-start"
    INLINE_END = "inline-end"
    SPAN_INLINE_START = "span-inline-start"
    SPAN_INLINE_END = "span-inline-end"
    SELF_BLOCK_START = "self-block-start"
    SELF_BLOCK_END = "self-block-end"
    SPAN_SELF_BLOCK_START = "span-self-block-start"
    SPAN_SELF_BLOCK_END = "span-self-block-end"
    SELF_INLINE_START = "self-inline-start"
    SELF_INLINE_END = "self-inline-end"
    SPAN_SELF_INLINE_START = "span-self-inline-start"
    SPAN_SELF_INLINE_END = "span-self-inline-end"
    START = "start"
    END = "end"
    SPAN_START = "span-start"
    SPAN_END = "span-end"
    SELF_START = "self-start"
    SELF_END = "self-end"
    SPAN_SELF_START = "span-self-start"
    SPAN_SELF_END = "span-self-end"


class PositionEdge(KeywordGroup, Enum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"


class Positioning(KeywordGroup, Enum):
    ABSOLUTE = "absolute"
    FIXED = "fixed"
    RELATIVE = "relative"
    STATIC = "static"
    STICKY = "sticky"


class ReferrerPolicyModifierValue(KeywordGroup, Enum):
    NO_REFERRER = "no-referrer"
    NO_REFERRER_WHEN_DOWNGRADE = "no-referrer-when-downgrade"
    SAME_ORIGIN = "same-origin"
    ORIGIN = "origin"
    STRICT_ORIGIN = "strict-origin"
    ORIGIN_WHEN_CROSS_ORIGIN = "origin-when-cross-origin"
    STRICT_ORIGIN_WHEN_CROSS_ORIGIN = "strict-origin-when-cross-origin"
    UNSAFE_URL = "unsafe-url"


class RelativeSize(KeywordGroup, Enum):
    SMALLER = "smaller"
    LARGER = "larger"


class Repetition(KeywordGroup, Enum):
    NO_REPEAT = "no-repeat"
    REPEAT = "repeat"
    ROUND = "round"
    SPACE = "space"


class RoundingStrategy(KeywordGroup, Enum):
    DOWN = "down"
    NEAREST = "nearest"
    TO_ZERO = "to-zero"
    UP = "up"


class ScrollbarGutter(KeywordGroup, Enum):
    AUTO = "auto"
    STABLE = "stable"
    BOTH_EDGES = "both-edges"


class ScrollbarWidth(KeywordGroup, Enum):
    AUTO = "auto"
    THIN = "thin"
    NONE = "none"


class ShapeBox(KeywordGroup, Enum):
    CONTENT_BOX = "content-box"
    PADDING_BOX = "padding-box"
    BORDER_BOX = "border-box"
    MARGIN_BOX = "margin-box"


class ShapeRendering(KeywordGroup, Enum):
    AUTO = "auto"
    OPTIMIZESPEED = "optimizespeed"
    CRISPEDGES = "crispedges"
    GEOMETRICPRECISION = "geometricprecision"


class StepPosition(KeywordGroup, Enum):
    JUMP_START = "jump-start"
    JUMP_END = "jump-end"
    JUMP_NONE = "jump-none"
    JUMP_BOTH = "jump-both"
    START = "start"
    END = "end"


class StrokeLinecap(KeywordGroup, Enum):
    BUTT = "butt"
    SQUARE = "square"
    ROUND = "round"


class StrokeLinejoin(KeywordGroup, Enum):
    MITER = "miter"
    ROUND = "round"
    BEVEL = "bevel"


class TableLayout(KeywordGroup, Enum):
    AUTO = "auto"
    FIXED = "fixed"


class TextAlign(KeywordGroup, Enum):
    CENTER = "center"
    JUSTIFY = "justify"
    START = "start"
    END = "end"
    LEFT = "left"
    RIGHT = "right"
    MATCH_PARENT = "match-parent"


class TextAnchor(KeywordGroup, Enum):
    START = "start"
    MIDDLE = "middle"
    END = "end"


class TextDecorationLine(KeywordGroup, Enum):
    NONE = "none"
    UNDERLINE = "underline"
    OVERLINE = "overline"
    LINE_THROUGH = "line-through"
    BLINK = "blink"
    SPELLING_ERROR = "spelling-error"
    GRAMMAR_ERROR = "grammar-error"


class TextDecorationStyle(KeywordGroup, Enum):
    DASHED = "dashed"
    DOTTED = "dotted"
    DOUBLE = "double"
    SOLID = "solid"
    WAVY = "wavy"


class TextJustify(KeywordGroup, Enum):
    AUTO = "auto"
    NONE = "none"
    INTER_WORD = "inter-word"
    INTER_CHARACTER = "inter-character"


class TextOverflow(KeywordGroup, Enum):
    CLIP = "clip"
    ELLIPSIS = "ellipsis"


class TextRendering(KeywordGroup, Enum):
    AUTO = "auto"
    OPTIMIZESPEED = "optimizespeed"
    OPTIMIZELEGIBILITY = "optimizelegibility"
    GEOMETRICPRECISION = "geometricprecision"


class TextTransform(KeywordGroup, Enum):
    CAPITALIZE = "capitalize"
    FULL_SIZE_KANA = "full-size-kana"
    FULL_WIDTH = "full-width"
    LOWERCASE = "lowercase"
    MATH_AUTO = "math-auto"
    NONE = "none"
    UPPERCASE = "uppercase"


class TextUnderlinePositionHorizontal(KeywordGroup, Enum):
    AUTO = "auto"
    FROM_FONT = "from-font"
    UNDER = "under"


class TextUnderlinePositionVertical(KeywordGroup, Enum):
    AUTO = "auto"
    LEFT = "left"
    RIGHT = "right"


class TextWrapMode(KeywordGroup, Enum):
    WRAP = "wrap"
    NOWRAP = "nowrap"


class TextWrapStyle(KeywordGroup, Enum):
    AUTO = "auto"
    BALANCE = "balance"
    STABLE = "stable"
    PRETTY = "pretty"


class TouchAction(KeywordGroup, Enum):
    AUTO = "auto"
    MANIPULATION = "manipulation"
    NONE = "none"
    PAN_DOWN = "pan-down"
    PAN_LEFT = "pan-left"
    PAN_RIGHT = "pan-right"
    PAN_UP = "pan-up"
    PAN_X = "pan-x"
    PAN_Y = "pan-y"


class TransformBox(KeywordGroup, Enum):
    CONTENT_BOX = "content-box"
    BORDER_BOX = "border-box"
    FILL_BOX = "fill-box"
    STROKE_BOX = "stroke-box"
    VIEW_BOX = "view-box"


class TransformStyle(KeywordGroup, Enum):
    FLAT = "flat"
    PRESERVE3D = "preserve3d"


class TransitionBehavior(KeywordGroup, Enum):
    NORMAL = "normal"
    ALLOW_DISCRETE = "allow-discrete"


class TryOrder(KeywordGroup, Enum):
    MOST_WIDTH = "most-width"
    MOST_HEIGHT = "most-height"
    MOST_BLOCK_SIZE = "most-block-size"
    MOST_INLINE_SIZE = "most-inline-size"


class TryTactic(KeywordGroup, Enum):
    FLIP_BLOCK = "flip-block"
    FLIP_INLINE = "flip-inline"
    FLIP_START = "flip-start"


class UnicodeBidi(KeywordGroup, Enum):
    BIDI_OVERRIDE = "bidi-override"
    EMBED = "embed"
    ISOLATE = "isolate"
    ISOLATE_OVERRIDE = "isolate-override"
    NORMAL = "normal"
    PLAINTEXT = "plaintext"


class UserSelect(KeywordGroup, Enum):
    ALL = "all"
    AUTO = "auto"
    CONTAIN = "contain"
    NONE = "none"
    TEXT = "text"


class VerticalAlign(KeywordGroup, Enum):
    BASELINE = "baseline"
    BOTTOM = "bottom"
    MIDDLE = "middle"
    SUB = "sub"
    SUPER = "super"
    TEXT_BOTTOM = "text-bottom"
    TEXT_TOP = "text-top"
    TOP = "top"


class Visibility(KeywordGroup, Enum):
    COLLAPSE = "collapse"
    HIDDEN = "hidden"
    VISIBLE = "visible"


class WhiteSpace(KeywordGroup, Enum):
    NORMAL = "normal"
    PRE = "pre"
    PRE_LINE = "pre-line"
    PRE_WRAP = "pre-wrap"


class WhiteSpaceCollapse(KeywordGroup, Enum):
    COLLAPSE = "collapse"
    DISCARD = "discard"
    PRESERVE = "preserve"
    PRESERVE_BREAKS = "preserve-breaks"
    PRESERVE_SPACES = "preserve-spaces"
    BREAK_SPACES = "break-spaces"


class WordBreak(KeywordGroup, Enum):
    NORMAL = "normal"
    KEEP_ALL = "keep-all"
    BREAK_ALL = "break-all"
    BREAK_WORD = "break-word"


class WritingMode(KeywordGroup, Enum):
    HORIZONTAL_TB = "horizontal-tb"
    VERTICAL_RL = "vertical-rl"
    VERTICAL_LR = "vertical-lr"
    SIDEWAYS_RL = "sideways-rl"
    SIDEWAYS_LR = "sideways-lr"


KEYWORD_GROUPS = {
    "absolute-size": AbsoluteSize,
    "align-content": AlignContent,
    "align-items": AlignItems,
    "align-self": AlignSelf,
    "anchor-side": AnchorSide,
    "anchor-size": AnchorSize,
    "animation-composition": AnimationComposition,
    "animation-direction": AnimationDirection,
    "animation-fill-mode": AnimationFillMode,
    "animation-play-state": AnimationPlayState,
    "appearance": Appearance,
    "background-attachment": BackgroundAttachment,
    "background-box": BackgroundBox,
    "border-collapse": BorderCollapse,
    "border-image-repeat": BorderImageRepeat,
    "box-sizing": BoxSizing,
    "caption-side": CaptionSide,
    "clear": Clear,
    "color-interpolation": ColorInterpolation,
    "column-span": ColumnSpan,
    "compositing-operator": CompositingOperator,
    "contain": Contain,
    "content-visibility": ContentVisibility,
    "coord-box": CoordBox,
    "counter-style-name-keyword": CounterStyleNameKeyword,
    "cross-origin-modifier-value": CrossOriginModifierValue,
    "cursor-predefined": CursorPredefined,
    "direction": Direction,
    "display-box": DisplayBox,
    "display-inside": DisplayInside,
    "display-internal": DisplayInternal,
    "display-legacy": DisplayLegacy,
    "display-outside": DisplayOutside,
    "easing-keyword": EasingKeyword,
    "empty-cells": EmptyCells,
    "fill-rule": FillRule,
    "flex-direction": FlexDirection,
    "flex-wrap": FlexWrap,
    "float": Float,
    "font-display": FontDisplay,
    "font-kerning": FontKerning,
    "font-style": FontStyle,
    "font-tech": FontTech,
    "font-variant-alternates": FontVariantAlternates,
    "font-variant-caps": FontVariantCaps,
    "font-variant-east-asian": FontVariantEastAsian,
    "font-variant-emoji": FontVariantEmoji,
    "font-variant-ligatures": FontVariantLigatures,
    "font-variant-numeric": FontVariantNumeric,
    "font-variant-position": FontVariantPosition,
    "font-width": FontWidth,
    "generic-font-family": GenericFontFamily,
    "hue-interpolation-method": HueInterpolationMethod,
    "image-rendering": ImageRendering,
    "isolation": Isolation,
    "justify-content": JustifyContent,
    "justify-items": JustifyItems,
    "justify-self": JustifySelf,
    "line-style": LineStyle,
    "line-width": LineWidth,
    "list-style-position": ListStylePosition,
    "mask-type": MaskType,
    "masking-mode": MaskingMode,
    "math-shift": MathShift,
    "math-style": MathStyle,
    "mix-blend-mode": MixBlendMode,
    "object-fit": ObjectFit,
    "outline-style": OutlineStyle,
    "overflow": Overflow,
    "page-size": PageSize,
    "paint-order": PaintOrder,
    "pointer-events": PointerEvents,
    "polar-color-space": PolarColorSpace,
    "position-area": PositionArea,
    "position-edge": PositionEdge,
    "positioning": Positioning,
    "referrer-policy-modifier-value": ReferrerPolicyModifierValue,
    "relative-size": RelativeSize,
    "repetition": Repetition,
    "rounding-strategy": RoundingStrategy,
    "scrollbar-gutter": ScrollbarGutter,
    "scrollbar-width": ScrollbarWidth,
    "shape-box": ShapeBox,
    "shape-rendering": ShapeRendering,
    "step-position": StepPosition,
    "stroke-linecap": StrokeLinecap,
    "stroke-linejoin": StrokeLinejoin,
    "table-layout": TableLayout,
    "text-align": TextAlign,
    "text-anchor": TextAnchor,
    "text-decoration-line": TextDecorationLine,
    "text-decoration-style": TextDecorationStyle,
    "text-justify": TextJustify,
    "text-overflow": TextOverflow,
    "text-rendering": TextRendering,
    "text-transform": TextTransform,
    "text-underline-position-horizontal": TextUnderlinePositionHorizontal,
    "text-underline-position-vertical": TextUnderlinePositionVertical,
    "text-wrap-mode": TextWrapMode,
    "text-wrap-style": TextWrapStyle,
    "touch-action": TouchAction,
    "transform-box": TransformBox,
    "transform-style": TransformStyle,
    "transition-behavior": TransitionBehavior,
    "try-order": TryOrder,
    "try-tactic": TryTactic,
    "unicode-bidi": UnicodeBidi,
    "user-select": UserSelect,
    "vertical-align": VerticalAlign,
    "visibility": Visibility,
    "white-space": WhiteSpace,
    "white-space-collapse": WhiteSpaceCollapse,
    "word-break": WordBreak,
    "writing-mode": WritingMode,
}


# ==================================== misc ==================================== #
class Origin(Enum):
    USER_AGENT = 0
    USER = 1
    AUTHOR_ORIGIN = 2
    ANIMATION = 3
    IMPORTANT_AUTHOR_ORIGIN = 4
    IMPORTANT_USER = 5
    IMPORTANT_USER_AGENT = 6
    TRANSITION = 4
