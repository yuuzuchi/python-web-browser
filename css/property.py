from typing import Type
from enum import Enum
from css.enums import Keyword, Property, ValueType, KEYWORD_GROUPS, KeywordGroup
from log import log, err, warn, set_debug

# adapted from ladybird's properties.json
# fmt: off
PROPERTIES = {
    "-webkit-align-content": {"legacy-alias-for": "align-content"},
    "-webkit-align-items": {"legacy-alias-for": "align-items"},
    "-webkit-align-self": {"legacy-alias-for": "align-self"},
    "-webkit-animation": {"legacy-alias-for": "animation"},
    "-webkit-animation-delay": {"legacy-alias-for": "animation-delay"},
    "-webkit-animation-direction": {"legacy-alias-for": "animation-direction"},
    "-webkit-animation-duration": {"legacy-alias-for": "animation-duration"},
    "-webkit-animation-fill-mode": {"legacy-alias-for": "animation-fill-mode"},
    "-webkit-animation-iteration-count": {
        "legacy-alias-for": "animation-iteration-count"
    },
    "-webkit-animation-name": {"legacy-alias-for": "animation-name"},
    "-webkit-animation-play-state": {"legacy-alias-for": "animation-play-state"},
    "-webkit-animation-timing-function": {
        "legacy-alias-for": "animation-timing-function"
    },
    "-webkit-appearance": {"legacy-alias-for": "appearance"},
    "-webkit-background-clip": {"legacy-alias-for": "background-clip"},
    "-webkit-background-origin": {"legacy-alias-for": "background-origin"},
    "-webkit-background-size": {"legacy-alias-for": "background-size"},
    "-webkit-border-bottom-left-radius": {
        "legacy-alias-for": "border-bottom-left-radius"
    },
    "-webkit-border-bottom-right-radius": {
        "legacy-alias-for": "border-bottom-right-radius"
    },
    "-webkit-border-radius": {"legacy-alias-for": "border-radius"},
    "-webkit-border-top-left-radius": {"legacy-alias-for": "border-top-left-radius"},
    "-webkit-border-top-right-radius": {"legacy-alias-for": "border-top-right-radius"},
    "-webkit-box-align": {"legacy-alias-for": "align-items"},
    "-webkit-box-flex": {"legacy-alias-for": "flex-grow"},
    "-webkit-box-ordinal-group": {"legacy-alias-for": "order"},
    "-webkit-box-orient": {"legacy-alias-for": "flex-direction"},
    "-webkit-box-pack": {"legacy-alias-for": "justify-content"},
    "-webkit-box-shadow": {"legacy-alias-for": "box-shadow"},
    "-webkit-box-sizing": {"legacy-alias-for": "box-sizing"},
    "-webkit-filter": {"legacy-alias-for": "filter"},
    "-webkit-flex": {"legacy-alias-for": "flex"},
    "-webkit-flex-basis": {"legacy-alias-for": "flex-basis"},
    "-webkit-flex-direction": {"legacy-alias-for": "flex-direction"},
    "-webkit-flex-flow": {"legacy-alias-for": "flex-flow"},
    "-webkit-flex-grow": {"legacy-alias-for": "flex-grow"},
    "-webkit-flex-shrink": {"legacy-alias-for": "flex-shrink"},
    "-webkit-flex-wrap": {"legacy-alias-for": "flex-wrap"},
    "-webkit-justify-content": {"legacy-alias-for": "justify-content"},
    "-webkit-mask": {"legacy-alias-for": "mask"},
    "-webkit-mask-image": {"legacy-alias-for": "mask-image"},
    "-webkit-order": {"legacy-alias-for": "order"},
    "-webkit-text-fill-color": {
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "currentColor",
        "valid-types": ["color"],
    },
    "-webkit-transform": {"legacy-alias-for": "transform"},
    "-webkit-transform-origin": {"legacy-alias-for": "transform-origin"},
    "-webkit-transition": {"legacy-alias-for": "transition"},
    "-webkit-transition-delay": {"legacy-alias-for": "transition-delay"},
    "-webkit-transition-duration": {"legacy-alias-for": "transition-duration"},
    "-webkit-transition-property": {"legacy-alias-for": "transition-property"},
    "-webkit-transition-timing-function": {
        "legacy-alias-for": "transition-timing-function"
    },
    "-webkit-user-select": {"legacy-alias-for": "user-select"},
    "accent-color": {
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "auto",
        "valid-types": ["color"],
        "valid-identifiers": ["auto"],
    },
    "align-content": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "normal",
        "valid-types": ["align-content"],
    },
    "align-items": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "normal",
        "valid-types": ["align-items"],
    },
    "align-self": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["align-self"],
    },
    "all": {
        "affects-layout": True,
        "affects-stacking-context": True,
        "inherited": False,
        "initial": "initial",
        "longhands": [],
        "_comment": "The 'longhands' array is populated in the code generator to avoid having to maintain it manually",
    },
    "anchor-name": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "none",
        "valid-types": ["dashed-ident"],
        "valid-identifiers": ["none"],
    },
    "anchor-scope": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": False,
        "initial": "none",
        "valid-types": ["dashed-ident"],
        "valid-identifiers": ["none", "all"],
    },
    "animation": {
        "affects-layout": False,
        "inherited": False,
        "initial": "none 0s ease 1 normal running 0s none",
        "__comment": "FIXME: animation properties should be coordinating-lists",
        "multiplicity": "single",
        "longhands": [
            "animation-duration",
            "animation-timing-function",
            "animation-delay",
            "animation-iteration-count",
            "animation-direction",
            "animation-fill-mode",
            "animation-play-state",
            "animation-name",
        ],
    },
    "animation-composition": {
        "affects-layout": False,
        "animation-type": "none",
        "inherited": False,
        "initial": "replace",
        "valid-types": ["animation-composition"],
    },
    "animation-delay": {
        "affects-layout": False,
        "animation-type": "none",
        "inherited": False,
        "initial": "0s",
        "__comment": "FIXME: animation properties should be coordinating-lists",
        "multiplicity": "single",
        "valid-types": ["time [-∞,∞]"],
    },
    "animation-direction": {
        "affects-layout": False,
        "animation-type": "none",
        "inherited": False,
        "initial": "normal",
        "__comment": "FIXME: animation properties should be coordinating-lists",
        "multiplicity": "single",
        "valid-identifiers": ["normal", "reverse", "alternate", "alternate-reverse"],
    },
    "animation-duration": {
        "affects-layout": False,
        "animation-type": "none",
        "inherited": False,
        "initial": "0s",
        "__comment": "FIXME: animation properties should be coordinating-lists",
        "multiplicity": "single",
        "valid-types": ["time [0,∞]"],
        "valid-identifiers": ["auto"],
    },
    "animation-fill-mode": {
        "affects-layout": False,
        "animation-type": "none",
        "inherited": False,
        "initial": "none",
        "__comment": "FIXME: animation properties should be coordinating-lists",
        "multiplicity": "single",
        "valid-identifiers": ["none", "forwards", "backwards", "both"],
    },
    "animation-iteration-count": {
        "affects-layout": False,
        "animation-type": "none",
        "inherited": False,
        "initial": "1",
        "__comment": "FIXME: animation properties should be coordinating-lists",
        "multiplicity": "single",
        "valid-types": ["number [0,∞]"],
        "valid-identifiers": ["infinite"],
    },
    "animation-name": {
        "affects-layout": False,
        "animation-type": "none",
        "inherited": False,
        "initial": "none",
        "__comment": "FIXME: animation properties should be coordinating-lists",
        "multiplicity": "single",
        "valid-types": ["string", "custom-ident ![none]"],
        "valid-identifiers": ["none"],
    },
    "animation-play-state": {
        "affects-layout": False,
        "animation-type": "none",
        "inherited": False,
        "initial": "running",
        "__comment": "FIXME: animation properties should be coordinating-lists",
        "multiplicity": "single",
        "valid-identifiers": ["running", "paused"],
    },
    "animation-timing-function": {
        "affects-layout": False,
        "animation-type": "none",
        "inherited": False,
        "initial": "ease",
        "__comment": "FIXME: animation properties should be coordinating-lists",
        "multiplicity": "single",
        "valid-types": ["easing-function", "easing-keyword"],
    },
    "appearance": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "none",
        "valid-types": ["appearance"],
    },
    "aspect-ratio": {
        "affects-layout": True,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["ratio"],
        "valid-identifiers": ["auto"],
    },
    "backdrop-filter": {
        "affects-layout": False,
        "affects-stacking-context": True,
        "animation-type": "custom",
        "inherited": False,
        "initial": "none",
        "__comment": "FIXME: List `filter-value-list` as a valid-type once it's generically supported.",
        "multiplicity": "list",
        "valid-identifiers": ["none"],
    },
    "background": {
        "affects-layout": False,
        "inherited": False,
        "initial": "transparent",
        "longhands": [
            "background-attachment",
            "background-clip",
            "background-color",
            "background-image",
            "background-origin",
            "background-position",
            "background-repeat",
            "background-size",
        ],
        "multiplicity": "coordinating-list",
    },
    "background-attachment": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": False,
        "initial": "scroll",
        "multiplicity": "coordinating-list",
        "valid-types": ["background-attachment"],
    },
    "background-blend-mode": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "normal",
        "multiplicity": "coordinating-list",
        "valid-types": ["mix-blend-mode"],
    },
    "background-clip": {
        "affects-layout": False,
        "animation-type": "repeatable-list",
        "inherited": False,
        "initial": "border-box",
        "multiplicity": "coordinating-list",
        "valid-types": ["background-box"],
    },
    "background-color": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "transparent",
        "valid-types": ["color"],
        "quirks": ["hashless-hex-color"],
    },
    "background-image": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": False,
        "initial": "none",
        "multiplicity": "coordinating-list",
        "valid-types": ["image"],
        "valid-identifiers": ["none"],
    },
    "background-origin": {
        "affects-layout": False,
        "animation-type": "repeatable-list",
        "inherited": False,
        "initial": "padding-box",
        "multiplicity": "coordinating-list",
        "valid-types": ["background-box"],
    },
    "background-position": {
        "affects-layout": False,
        "inherited": False,
        "initial": "0% 0%",
        "max-values": 4,
        "multiplicity": "coordinating-list",
        "valid-types": ["background-position"],
        "quirks": ["unitless-length"],
        "longhands": ["background-position-x", "background-position-y"],
        "percentages-resolve-to": "length",
    },
    "background-position-x": {
        "affects-layout": False,
        "animation-type": "repeatable-list",
        "inherited": False,
        "initial": "0%",
        "multiplicity": "coordinating-list",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["center", "left", "right"],
        "percentages-resolve-to": "length",
    },
    "background-position-y": {
        "affects-layout": False,
        "animation-type": "repeatable-list",
        "inherited": False,
        "initial": "0%",
        "multiplicity": "coordinating-list",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["center", "bottom", "top"],
        "percentages-resolve-to": "length",
    },
    "background-repeat": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": False,
        "initial": "repeat",
        "multiplicity": "coordinating-list",
        "max-values": 2,
        "valid-types": ["repetition"],
        "valid-identifiers": ["repeat-x", "repeat-y"],
    },
    "background-size": {
        "affects-layout": False,
        "animation-type": "repeatable-list",
        "inherited": False,
        "initial": "auto",
        "multiplicity": "coordinating-list",
        "max-values": 2,
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["auto", "cover", "contain"],
        "percentages-resolve-to": "length",
    },
    "block-size": {
        "logical-alias-for": {"group": "size", "mapping": "block-size"},
        "initial": "auto",
        "max-values": 1,
        "needs-layout-for-getcomputedstyle": True,
    },
    "border": {
        "inherited": False,
        "initial": "medium currentcolor none",
        "longhands": ["border-width", "border-style", "border-color", "border-image"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "border-block": {
        "inherited": False,
        "initial": "medium currentcolor none",
        "longhands": ["border-block-width", "border-block-style", "border-block-color"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "border-block-color": {
        "inherited": False,
        "initial": "currentcolor",
        "positional-value-list-shorthand": True,
        "longhands": ["border-block-start-color", "border-block-end-color"],
        "valid-types": ["color"],
    },
    "border-block-end": {
        "inherited": False,
        "initial": "medium currentcolor none",
        "longhands": [
            "border-block-end-width",
            "border-block-end-style",
            "border-block-end-color",
        ],
        "needs-layout-for-getcomputedstyle": True,
    },
    "border-block-end-color": {
        "logical-alias-for": {"group": "border-color", "mapping": "block-end"},
        "max-values": 1,
    },
    "border-block-end-style": {
        "logical-alias-for": {"group": "border-style", "mapping": "block-end"},
        "max-values": 1,
    },
    "border-block-end-width": {
        "logical-alias-for": {"group": "border-width", "mapping": "block-end"},
        "max-values": 1,
        "needs-layout-for-getcomputedstyle": True,
    },
    "border-block-start": {
        "inherited": False,
        "initial": "medium currentcolor none",
        "longhands": [
            "border-block-start-width",
            "border-block-start-style",
            "border-block-start-color",
        ],
        "needs-layout-for-getcomputedstyle": True,
    },
    "border-block-start-color": {
        "logical-alias-for": {"group": "border-color", "mapping": "block-start"},
        "max-values": 1,
    },
    "border-block-start-style": {
        "logical-alias-for": {"group": "border-style", "mapping": "block-start"},
        "max-values": 1,
    },
    "border-block-start-width": {
        "logical-alias-for": {"group": "border-width", "mapping": "block-start"},
        "max-values": 1,
        "needs-layout-for-getcomputedstyle": True,
    },
    "border-block-style": {
        "inherited": False,
        "initial": "none",
        "positional-value-list-shorthand": True,
        "longhands": ["border-block-start-style", "border-block-end-style"],
        "valid-types": ["line-style"],
    },
    "border-block-width": {
        "inherited": False,
        "initial": "medium",
        "positional-value-list-shorthand": True,
        "longhands": ["border-block-start-width", "border-block-end-width"],
        "valid-types": ["length [0,∞]", "line-width"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "border-bottom": {
        "inherited": False,
        "initial": "medium currentcolor none",
        "longhands": [
            "border-bottom-width",
            "border-bottom-style",
            "border-bottom-color",
        ],
        "needs-layout-for-getcomputedstyle": True,
    },
    "border-bottom-color": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "initial": "currentcolor",
        "inherited": False,
        "valid-types": ["color"],
        "quirks": ["hashless-hex-color"],
    },
    "border-bottom-left-radius": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "initial": "0",
        "inherited": False,
        "max-values": 2,
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
    },
    "border-bottom-right-radius": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "initial": "0",
        "inherited": False,
        "max-values": 2,
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
    },
    "border-bottom-style": {
        "animation-type": "discrete",
        "initial": "none",
        "inherited": False,
        "valid-types": ["line-style"],
    },
    "border-bottom-width": {
        "animation-type": "by-computed-value",
        "initial": "medium",
        "inherited": False,
        "valid-types": ["length [0,∞]", "line-width"],
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "border-collapse": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "separate",
        "valid-types": ["border-collapse"],
    },
    "border-color": {
        "affects-layout": False,
        "initial": "currentcolor",
        "positional-value-list-shorthand": True,
        "longhands": [
            "border-top-color",
            "border-right-color",
            "border-bottom-color",
            "border-left-color",
        ],
        "valid-types": ["color"],
        "quirks": ["hashless-hex-color"],
    },
    "border-end-end-radius": {
        "logical-alias-for": {"group": "border-radius", "mapping": "end-end"},
        "max-values": 1,
    },
    "border-end-start-radius": {
        "logical-alias-for": {"group": "border-radius", "mapping": "end-start"},
        "max-values": 1,
    },
    "border-image": {
        "inherited": False,
        "initial": "none 100% / 1 / 0 stretch",
        "longhands": [
            "border-image-source",
            "border-image-slice",
            "border-image-width",
            "border-image-outset",
            "border-image-repeat",
        ],
    },
    "border-image-outset": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "max-values": 4,
        "valid-types": ["length [0,∞]", "number [0,∞]"],
    },
    "border-image-repeat": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": False,
        "initial": "stretch",
        "max-values": 2,
        "valid-types": ["border-image-repeat"],
    },
    "border-image-slice": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "100%",
        "valid-identifiers": ["fill"],
        "valid-types": ["number [0,∞]", "percentage [0,∞]"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "border-image-source": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": False,
        "initial": "none",
        "valid-types": ["image"],
        "valid-identifiers": ["none"],
    },
    "border-image-width": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "1",
        "max-values": 4,
        "valid-types": ["length [0,∞]", "percentage [0,∞]", "number [0,∞]"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "needs-layout-for-getcomputedstyle": True,
    },
    "border-inline": {
        "inherited": False,
        "initial": "medium currentcolor none",
        "longhands": [
            "border-inline-width",
            "border-inline-style",
            "border-inline-color",
        ],
        "needs-layout-for-getcomputedstyle": True,
    },
    "border-inline-color": {
        "inherited": False,
        "initial": "currentcolor",
        "positional-value-list-shorthand": True,
        "longhands": ["border-inline-start-color", "border-inline-end-color"],
        "valid-types": ["color"],
    },
    "border-inline-end": {
        "inherited": False,
        "initial": "medium currentcolor none",
        "longhands": [
            "border-inline-end-width",
            "border-inline-end-style",
            "border-inline-end-color",
        ],
        "needs-layout-for-getcomputedstyle": True,
    },
    "border-inline-end-color": {
        "logical-alias-for": {"group": "border-color", "mapping": "inline-end"},
        "max-values": 1,
    },
    "border-inline-end-style": {
        "logical-alias-for": {"group": "border-style", "mapping": "inline-end"},
        "max-values": 1,
    },
    "border-inline-end-width": {
        "logical-alias-for": {"group": "border-width", "mapping": "inline-end"},
        "max-values": 1,
    },
    "border-inline-start": {
        "inherited": False,
        "initial": "medium currentcolor none",
        "longhands": [
            "border-inline-start-width",
            "border-inline-start-style",
            "border-inline-start-color",
        ],
    },
    "border-inline-start-color": {
        "logical-alias-for": {"group": "border-color", "mapping": "inline-start"},
        "max-values": 1,
    },
    "border-inline-start-style": {
        "logical-alias-for": {"group": "border-style", "mapping": "inline-start"},
        "max-values": 1,
    },
    "border-inline-start-width": {
        "logical-alias-for": {"group": "border-width", "mapping": "inline-start"},
        "max-values": 1,
    },
    "border-inline-style": {
        "inherited": False,
        "initial": "none",
        "positional-value-list-shorthand": True,
        "longhands": ["border-inline-start-style", "border-inline-end-style"],
        "valid-types": ["line-style"],
    },
    "border-inline-width": {
        "inherited": False,
        "initial": "medium",
        "positional-value-list-shorthand": True,
        "longhands": ["border-inline-start-width", "border-inline-end-width"],
        "valid-types": ["length [0,∞]", "line-width"],
    },
    "border-left": {
        "inherited": False,
        "initial": "medium currentcolor none",
        "longhands": ["border-left-width", "border-left-style", "border-left-color"],
    },
    "border-left-color": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "initial": "currentcolor",
        "inherited": False,
        "valid-types": ["color"],
        "quirks": ["hashless-hex-color"],
    },
    "border-left-style": {
        "animation-type": "discrete",
        "initial": "none",
        "inherited": False,
        "valid-types": ["line-style"],
    },
    "border-left-width": {
        "animation-type": "by-computed-value",
        "initial": "medium",
        "inherited": False,
        "valid-types": ["length [0,∞]", "line-width"],
        "quirks": ["unitless-length"],
    },
    "border-radius": {
        "affects-layout": False,
        "inherited": False,
        "initial": "0",
        "longhands": [
            "border-top-left-radius",
            "border-top-right-radius",
            "border-bottom-left-radius",
            "border-bottom-right-radius",
        ],
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
    },
    "border-right": {
        "inherited": False,
        "initial": "medium currentcolor none",
        "longhands": ["border-right-width", "border-right-style", "border-right-color"],
    },
    "border-right-color": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "initial": "currentcolor",
        "inherited": False,
        "valid-types": ["color"],
        "quirks": ["hashless-hex-color"],
    },
    "border-right-style": {
        "animation-type": "discrete",
        "initial": "none",
        "inherited": False,
        "valid-types": ["line-style"],
    },
    "border-right-width": {
        "animation-type": "by-computed-value",
        "initial": "medium",
        "inherited": False,
        "valid-types": ["length [0,∞]", "line-width"],
        "quirks": ["unitless-length"],
    },
    "border-spacing": {
        "_comment": "Follows the newer definition from: https://drafts.csswg.org/css-tables-3/#border-spacing-property",
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "0",
        "max-values": 2,
        "valid-types": ["length [0,∞]"],
        "quirks": ["unitless-length"],
    },
    "border-start-end-radius": {
        "logical-alias-for": {"group": "border-radius", "mapping": "start-end"},
        "max-values": 1,
    },
    "border-start-start-radius": {
        "logical-alias-for": {"group": "border-radius", "mapping": "start-start"},
        "max-values": 1,
    },
    "border-style": {
        "initial": "none",
        "positional-value-list-shorthand": True,
        "longhands": [
            "border-top-style",
            "border-right-style",
            "border-bottom-style",
            "border-left-style",
        ],
        "valid-types": ["line-style"],
    },
    "border-top": {
        "inherited": False,
        "initial": "medium currentcolor none",
        "longhands": ["border-top-width", "border-top-style", "border-top-color"],
    },
    "border-top-color": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "initial": "currentcolor",
        "inherited": False,
        "valid-types": ["color"],
        "quirks": ["hashless-hex-color"],
    },
    "border-top-left-radius": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "initial": "0",
        "inherited": False,
        "max-values": 2,
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
    },
    "border-top-right-radius": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "initial": "0",
        "inherited": False,
        "max-values": 2,
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
    },
    "border-top-style": {
        "animation-type": "discrete",
        "initial": "none",
        "inherited": False,
        "valid-types": ["line-style"],
    },
    "border-top-width": {
        "animation-type": "by-computed-value",
        "initial": "medium",
        "inherited": False,
        "valid-types": ["length [0,∞]", "line-width"],
        "quirks": ["unitless-length"],
    },
    "border-width": {
        "initial": "medium",
        "positional-value-list-shorthand": True,
        "longhands": [
            "border-top-width",
            "border-right-width",
            "border-bottom-width",
            "border-left-width",
        ],
        "valid-types": ["length [0,∞]", "line-width"],
        "quirks": ["unitless-length"],
    },
    "bottom": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]", "anchor"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "box-shadow": {
        "affects-layout": False,
        "animation-type": "custom",
        "inherited": False,
        "initial": "none",
        "multiplicity": "list",
        "valid-identifiers": ["none"],
    },
    "box-sizing": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "content-box",
        "valid-types": ["box-sizing"],
    },
    "caption-side": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "top",
        "valid-types": ["caption-side"],
    },
    "caret-color": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "auto",
        "valid-identifiers": ["auto"],
        "valid-types": ["color"],
    },
    "clear": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "none",
        "valid-types": ["clear"],
    },
    "clip": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-identifiers": ["auto"],
        "valid-types": ["rect"],
        "quirks": ["unitless-length"],
    },
    "clip-path": {
        "animation-type": "by-computed-value",
        "affects-layout": False,
        "affects-stacking-context": True,
        "inherited": False,
        "valid-identifiers": ["none"],
        "__comment": "FIXME: This should be a <clip-source> | [ <basic-shape> || <geometry-box> ]",
        "valid-types": ["basic-shape", "url"],
        "initial": "none",
    },
    "clip-rule": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": True,
        "initial": "nonzero",
        "valid-types": ["fill-rule"],
    },
    "color": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "canvastext",
        "valid-types": ["color"],
        "quirks": ["hashless-hex-color"],
    },
    "color-interpolation": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": True,
        "initial": "srgb",
        "valid-types": ["color-interpolation"],
    },
    "color-scheme": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["custom-ident ![normal,light,dark,only]"],
        "valid-identifiers": ["normal", "light", "dark"],
    },
    "column-count": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["integer [1,∞]"],
        "valid-identifiers": ["auto"],
    },
    "column-gap": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "normal",
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["normal"],
        "percentages-resolve-to": "length",
    },
    "column-height": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["length [0,∞]"],
        "valid-identifiers": ["auto"],
    },
    "column-span": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "none",
        "valid-types": ["column-span"],
    },
    "column-width": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["length [0,∞]"],
        "valid-identifiers": ["auto"],
    },
    "columns": {
        "inherited": False,
        "initial": "auto auto / auto",
        "longhands": ["column-width", "column-count", "column-height"],
    },
    "contain": {
        "affects-stacking-context": True,
        "animation-type": "none",
        "inherited": False,
        "initial": "none",
        "valid-types": ["contain"],
    },
    "container-type": {
        "affects-stacking-context": True,
        "animation-type": "none",
        "inherited": False,
        "initial": "normal",
        "valid-identifiers": ["normal", "size", "inline-size", "scroll-state"],
    },
    "content": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "normal",
        "__comment": "FIXME: This accepts a whole lot of other types and identifiers!",
        "valid-types": ["counter", "image", "string"],
        "valid-identifiers": [
            "normal",
            "none",
            "open-quote",
            "close-quote",
            "no-open-quote",
            "no-close-quote",
        ],
    },
    "content-visibility": {
        "animation-type": "custom",
        "inherited": False,
        "initial": "visible",
        "valid-types": ["content-visibility"],
    },
    "corner-block-end-shape": {
        "initial": "round round",
        "positional-value-list-shorthand": True,
        "longhands": ["corner-end-start-shape", "corner-end-end-shape"],
        "valid-types": ["corner-shape"],
    },
    "corner-block-start-shape": {
        "initial": "round round",
        "positional-value-list-shorthand": True,
        "longhands": ["corner-start-start-shape", "corner-start-end-shape"],
        "valid-types": ["corner-shape"],
    },
    "corner-bottom-left-shape": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "round",
        "valid-types": ["corner-shape"],
    },
    "corner-bottom-right-shape": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "round",
        "valid-types": ["corner-shape"],
    },
    "corner-bottom-shape": {
        "initial": "round round",
        "positional-value-list-shorthand": True,
        "longhands": ["corner-bottom-left-shape", "corner-bottom-right-shape"],
        "valid-types": ["corner-shape"],
    },
    "corner-end-end-shape": {
        "logical-alias-for": {"group": "corner-shape", "mapping": "end-end"}
    },
    "corner-end-start-shape": {
        "logical-alias-for": {"group": "corner-shape", "mapping": "end-start"}
    },
    "corner-inline-end-shape": {
        "initial": "round round",
        "positional-value-list-shorthand": True,
        "longhands": ["corner-start-end-shape", "corner-end-end-shape"],
        "valid-types": ["corner-shape"],
    },
    "corner-inline-start-shape": {
        "initial": "round round",
        "positional-value-list-shorthand": True,
        "longhands": ["corner-start-start-shape", "corner-end-start-shape"],
        "valid-types": ["corner-shape"],
    },
    "corner-left-shape": {
        "initial": "round round",
        "positional-value-list-shorthand": True,
        "longhands": ["corner-top-left-shape", "corner-bottom-left-shape"],
        "valid-types": ["corner-shape"],
    },
    "corner-right-shape": {
        "initial": "round round",
        "positional-value-list-shorthand": True,
        "longhands": ["corner-top-right-shape", "corner-bottom-right-shape"],
        "valid-types": ["corner-shape"],
    },
    "corner-shape": {
        "initial": "round round round round",
        "positional-value-list-shorthand": True,
        "longhands": [
            "corner-top-left-shape",
            "corner-top-right-shape",
            "corner-bottom-right-shape",
            "corner-bottom-left-shape",
        ],
        "valid-types": ["corner-shape"],
    },
    "corner-start-end-shape": {
        "logical-alias-for": {"group": "corner-shape", "mapping": "start-end"}
    },
    "corner-start-start-shape": {
        "logical-alias-for": {"group": "corner-shape", "mapping": "start-start"}
    },
    "corner-top-left-shape": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "round",
        "valid-types": ["corner-shape"],
    },
    "corner-top-right-shape": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "round",
        "valid-types": ["corner-shape"],
    },
    "corner-top-shape": {
        "initial": "round round",
        "positional-value-list-shorthand": True,
        "longhands": ["corner-top-left-shape", "corner-top-right-shape"],
        "valid-types": ["corner-shape"],
    },
    "counter-increment": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "none",
        "multiplicity": "list",
        "valid-types": ["custom-ident ![none]", "integer [-∞,∞]"],
        "valid-identifiers": ["none"],
    },
    "counter-reset": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "none",
        "multiplicity": "list",
        "valid-types": ["custom-ident ![none]", "integer [-∞,∞]"],
        "valid-identifiers": ["none"],
    },
    "counter-set": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "none",
        "multiplicity": "list",
        "valid-types": ["custom-ident ![none]", "integer [-∞,∞]"],
        "valid-identifiers": ["none"],
    },
    "cursor": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": True,
        "initial": "auto",
        "valid-types": ["url", "cursor-predefined", "number [-∞,∞]"],
    },
    "cx": {
        "__comment": "This is an SVG 2 geometry property, see: https://www.w3.org/TR/SVG/geometry.html#CX.",
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "cy": {
        "__comment": "This is an SVG 2 geometry property, see: https://www.w3.org/TR/SVG/geometry.html#CY.",
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "direction": {
        "animation-type": "none",
        "inherited": True,
        "initial": "ltr",
        "valid-types": ["direction"],
    },
    "display": {
        "animation-type": "custom",
        "inherited": False,
        "initial": "inline",
        "max-values": 3,
        "valid-identifiers": ["list-item"],
        "valid-types": [
            "display-outside",
            "display-inside",
            "display-internal",
            "display-box",
            "display-legacy",
        ],
    },
    "empty-cells": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "show",
        "valid-types": ["empty-cells"],
    },
    "fill": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "black",
        "valid-types": ["paint"],
    },
    "fill-opacity": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "1",
        "valid-types": ["opacity"],
    },
    "fill-rule": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": True,
        "initial": "nonzero",
        "valid-types": ["fill-rule"],
    },
    "filter": {
        "affects-layout": False,
        "affects-stacking-context": True,
        "animation-type": "custom",
        "inherited": False,
        "initial": "none",
        "__comment": "FIXME: List `filter-value-list` as a valid-type once it's generically supported.",
        "multiplicity": "list",
        "valid-identifiers": ["none"],
    },
    "flex": {
        "inherited": False,
        "initial": "0 1 auto",
        "valid-identifiers": ["none"],
        "longhands": ["flex-grow", "flex-shrink", "flex-basis"],
    },
    "flex-basis": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["fit-content", "length [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["auto", "content", "max-content", "min-content"],
        "percentages-resolve-to": "length",
    },
    "flex-direction": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "row",
        "valid-types": ["flex-direction"],
    },
    "flex-flow": {
        "inherited": False,
        "initial": "row nowrap",
        "longhands": ["flex-direction", "flex-wrap"],
    },
    "flex-grow": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["number [0,∞]"],
    },
    "flex-shrink": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "1",
        "valid-types": ["number [0,∞]"],
    },
    "flex-wrap": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "nowrap",
        "valid-types": ["flex-wrap"],
    },
    "float": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "none",
        "valid-types": ["float"],
    },
    "flood-color": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "black",
        "valid-types": ["color"],
    },
    "flood-opacity": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "1",
        "valid-types": ["opacity"],
    },
    "font": {
        "inherited": True,
        "initial": "normal medium serif",
        "__comment": "FIXME: Handle properties that are reset implicitly. https://drafts.csswg.org/css-fonts/#reset-implicitly",
        "longhands": [
            "font-family",
            "font-size",
            "font-width",
            "font-style",
            "font-variant",
            "font-weight",
            "line-height",
        ],
    },
    "font-family": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "serif",
        "multiplicity": "list",
        "valid-types": ["custom-ident", "string"],
    },
    "font-feature-settings": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "normal",
        "multiplicity": "list",
        "valid-types": ["integer [0,∞]", "opentype-tag"],
        "valid-identifiers": ["normal", "on", "off"],
    },
    "font-kerning": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "auto",
        "valid-types": ["font-kerning"],
    },
    "font-language-override": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["string"],
        "valid-identifiers": ["normal"],
    },
    "font-size": {
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "medium",
        "valid-types": [
            "length [0,∞]",
            "percentage [0,∞]",
            "absolute-size",
            "relative-size",
        ],
        "valid-identifiers": ["math"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "font-stretch": {"legacy-alias-for": "font-width"},
    "font-style": {
        "animation-type": "custom",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["font-style", "angle [-90,90]"],
    },
    "font-variant": {
        "inherited": True,
        "initial": "normal",
        "longhands": [
            "font-variant-alternates",
            "font-variant-caps",
            "font-variant-east-asian",
            "font-variant-emoji",
            "font-variant-ligatures",
            "font-variant-numeric",
            "font-variant-position",
        ],
        "valid-types": ["string"],
    },
    "font-variant-alternates": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["font-variant-alternates"],
    },
    "font-variant-caps": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["font-variant-caps"],
    },
    "font-variant-east-asian": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["font-variant-east-asian"],
    },
    "font-variant-emoji": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["font-variant-emoji"],
    },
    "font-variant-ligatures": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["font-variant-ligatures"],
    },
    "font-variant-numeric": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["font-variant-numeric"],
    },
    "font-variant-position": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["font-variant-position"],
    },
    "font-variation-settings": {
        "animation-type": "custom",
        "inherited": True,
        "initial": "normal",
        "multiplicity": "list",
        "valid-types": ["number", "opentype-tag"],
        "valid-identifiers": ["normal"],
    },
    "font-weight": {
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["number [1,1000]"],
        "valid-identifiers": ["bold", "bolder", "lighter", "normal"],
    },
    "font-width": {
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["percentage [0,∞]", "font-width"],
    },
    "gap": {
        "inherited": False,
        "initial": "normal",
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["normal"],
        "percentages-resolve-to": "length",
        "positional-value-list-shorthand": True,
        "longhands": ["row-gap", "column-gap"],
    },
    "grid": {
        "inherited": False,
        "initial": "auto",
        "valid-identifiers": ["auto"],
        "valid-types": ["length", "percentage", "string"],
        "percentages-resolve-to": "length",
        "longhands": [
            "grid-template-areas",
            "grid-template-rows",
            "grid-template-columns",
        ],
    },
    "grid-area": {
        "inherited": False,
        "initial": "auto",
        "valid-identifiers": ["auto"],
        "valid-types": ["custom-ident ![auto,span]"],
        "longhands": [
            "grid-column-end",
            "grid-column-start",
            "grid-row-end",
            "grid-row-start",
        ],
    },
    "grid-auto-columns": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-identifiers": ["auto"],
        "valid-types": ["length", "percentage", "string"],
        "percentages-resolve-to": "length",
    },
    "grid-auto-flow": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "row",
    },
    "grid-auto-rows": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-identifiers": ["auto"],
        "valid-types": ["length", "percentage", "string"],
        "percentages-resolve-to": "length",
    },
    "grid-column": {
        "inherited": False,
        "initial": "auto",
        "valid-identifiers": ["auto"],
        "valid-types": ["custom-ident ![auto,span]"],
        "longhands": ["grid-column-end", "grid-column-start"],
    },
    "grid-column-end": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "auto",
        "valid-identifiers": ["auto"],
        "valid-types": ["custom-ident ![auto,span]"],
    },
    "grid-column-gap": {"legacy-alias-for": "column-gap"},
    "grid-column-start": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "auto",
        "valid-identifiers": ["auto"],
        "valid-types": ["custom-ident ![auto,span]"],
    },
    "grid-gap": {"legacy-alias-for": "gap"},
    "grid-row": {
        "inherited": False,
        "initial": "auto",
        "valid-identifiers": ["auto"],
        "valid-types": ["custom-ident ![auto,span]"],
        "longhands": ["grid-row-end", "grid-row-start"],
    },
    "grid-row-end": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "auto",
        "valid-identifiers": ["auto"],
        "valid-types": ["custom-ident ![auto,span]"],
    },
    "grid-row-gap": {"legacy-alias-for": "row-gap"},
    "grid-row-start": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "auto",
        "valid-identifiers": ["auto"],
        "valid-types": ["custom-ident ![auto,span]"],
    },
    "grid-template": {
        "inherited": False,
        "initial": "auto",
        "valid-identifiers": ["auto"],
        "valid-types": ["length", "percentage", "string"],
        "percentages-resolve-to": "length",
        "longhands": [
            "grid-template-areas",
            "grid-template-rows",
            "grid-template-columns",
        ],
        "needs-layout-for-getcomputedstyle": True,
    },
    "grid-template-areas": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "none",
        "valid-identifiers": ["none"],
        "valid-types": ["string"],
    },
    "grid-template-columns": {
        "animation-type": "custom",
        "inherited": False,
        "initial": "none",
        "max-values": 4,
        "valid-identifiers": ["auto"],
        "valid-types": ["length", "percentage", "string"],
        "percentages-resolve-to": "length",
        "needs-layout-for-getcomputedstyle": True,
    },
    "grid-template-rows": {
        "animation-type": "custom",
        "inherited": False,
        "initial": "none",
        "max-values": 4,
        "valid-identifiers": ["auto"],
        "valid-types": ["length", "percentage", "string"],
        "percentages-resolve-to": "length",
        "needs-layout-for-getcomputedstyle": True,
    },
    "height": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["fit-content", "length [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["auto", "max-content", "min-content"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "image-rendering": {
        "animation-type": "discrete",
        "affects-layout": False,
        "inherited": True,
        "initial": "auto",
        "valid-types": ["image-rendering"],
    },
    "inline-size": {
        "logical-alias-for": {"group": "size", "mapping": "inline-size"},
        "initial": "auto",
        "max-values": 1,
        "needs-layout-for-getcomputedstyle": True,
    },
    "inset": {
        "inherited": False,
        "initial": "auto",
        "positional-value-list-shorthand": True,
        "longhands": ["top", "right", "bottom", "left"],
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "needs-layout-for-getcomputedstyle": True,
    },
    "inset-block": {
        "initial": "auto",
        "positional-value-list-shorthand": True,
        "longhands": ["inset-block-start", "inset-block-end"],
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "needs-layout-for-getcomputedstyle": True,
    },
    "inset-block-end": {
        "logical-alias-for": {"group": "inset", "mapping": "block-end"},
        "max-values": 1,
        "needs-layout-for-getcomputedstyle": True,
    },
    "inset-block-start": {
        "logical-alias-for": {"group": "inset", "mapping": "block-start"},
        "max-values": 1,
        "needs-layout-for-getcomputedstyle": True,
    },
    "inset-inline": {
        "initial": "auto",
        "positional-value-list-shorthand": True,
        "longhands": ["inset-inline-start", "inset-inline-end"],
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "needs-layout-for-getcomputedstyle": True,
    },
    "inset-inline-end": {
        "logical-alias-for": {"group": "inset", "mapping": "inline-end"},
        "max-values": 1,
        "needs-layout-for-getcomputedstyle": True,
    },
    "inset-inline-start": {
        "logical-alias-for": {"group": "inset", "mapping": "inline-start"},
        "max-values": 1,
        "needs-layout-for-getcomputedstyle": True,
    },
    "isolation": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["isolation"],
    },
    "justify-content": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "normal",
        "valid-types": ["justify-content"],
    },
    "justify-items": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "legacy",
        "valid-types": ["justify-items"],
    },
    "justify-self": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["justify-self"],
    },
    "left": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]", "anchor"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "letter-spacing": {
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "percentages-resolve-to": "length",
        "valid-identifiers": ["normal"],
        "quirks": ["unitless-length"],
    },
    "line-height": {
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["length [0,∞]", "number [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["normal"],
        "percentages-resolve-to": "length",
        "needs-layout-for-getcomputedstyle": True,
    },
    "list-style": {
        "inherited": True,
        "initial": "outside none disc",
        "longhands": ["list-style-position", "list-style-image", "list-style-type"],
    },
    "list-style-image": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "none",
        "valid-types": ["image"],
        "valid-identifiers": ["none"],
    },
    "list-style-position": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "outside",
        "valid-types": ["list-style-position"],
    },
    "list-style-type": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "disc",
        "valid-types": ["counter-style-name-keyword", "string"],
    },
    "margin": {
        "inherited": False,
        "initial": "0",
        "positional-value-list-shorthand": True,
        "longhands": ["margin-top", "margin-right", "margin-bottom", "margin-left"],
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "margin-block": {
        "initial": "0",
        "positional-value-list-shorthand": True,
        "longhands": ["margin-block-start", "margin-block-end"],
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "needs-layout-for-getcomputedstyle": True,
    },
    "margin-block-end": {
        "logical-alias-for": {"group": "margin", "mapping": "block-end"},
        "needs-layout-for-getcomputedstyle": True,
    },
    "margin-block-start": {
        "logical-alias-for": {"group": "margin", "mapping": "block-start"},
        "needs-layout-for-getcomputedstyle": True,
    },
    "margin-bottom": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "margin-inline": {
        "initial": "0",
        "positional-value-list-shorthand": True,
        "longhands": ["margin-inline-start", "margin-inline-end"],
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "needs-layout-for-getcomputedstyle": True,
    },
    "margin-inline-end": {
        "logical-alias-for": {"group": "margin", "mapping": "inline-end"},
        "needs-layout-for-getcomputedstyle": True,
    },
    "margin-inline-start": {
        "logical-alias-for": {"group": "margin", "mapping": "inline-start"},
        "needs-layout-for-getcomputedstyle": True,
    },
    "margin-left": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "margin-right": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "margin-top": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "mask": {
        "__comment": "FIXME: reset mask-border",
        "inherited": False,
        "affects-layout": False,
        "initial": "none",
        "multiplicity": "coordinating-list",
        "longhands": [
            "mask-clip",
            "mask-composite",
            "mask-image",
            "mask-mode",
            "mask-origin",
            "mask-position",
            "mask-repeat",
            "mask-size",
        ],
    },
    "mask-clip": {
        "animation-type": "discrete",
        "inherited": False,
        "affects-layout": False,
        "multiplicity": "coordinating-list",
        "valid-types": ["coord-box"],
        "valid-identifiers": ["no-clip"],
        "initial": "border-box",
    },
    "mask-composite": {
        "animation-type": "discrete",
        "inherited": False,
        "affects-layout": False,
        "multiplicity": "coordinating-list",
        "valid-types": ["compositing-operator"],
        "initial": "add",
    },
    "mask-image": {
        "animation-type": "discrete",
        "inherited": False,
        "affects-layout": False,
        "affects-stacking-context": True,
        "multiplicity": "coordinating-list",
        "valid-types": ["image", "url"],
        "valid-identifiers": ["none"],
        "initial": "none",
    },
    "mask-mode": {
        "animation-type": "discrete",
        "inherited": False,
        "affects-layout": False,
        "multiplicity": "coordinating-list",
        "valid-types": ["masking-mode"],
        "initial": "match-source",
    },
    "mask-origin": {
        "animation-type": "discrete",
        "inherited": False,
        "affects-layout": False,
        "multiplicity": "coordinating-list",
        "valid-types": ["coord-box"],
        "initial": "border-box",
    },
    "mask-position": {
        "animation-type": "repeatable-list",
        "affects-layout": False,
        "inherited": False,
        "initial": "0% 0%",
        "multiplicity": "coordinating-list",
        "valid-types": ["position"],
        "percentages-resolve-to": "length",
    },
    "mask-repeat": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": False,
        "initial": "repeat",
        "multiplicity": "coordinating-list",
        "max-values": 2,
        "valid-types": ["repetition"],
        "valid-identifiers": ["repeat-x", "repeat-y"],
    },
    "mask-size": {
        "affects-layout": False,
        "animation-type": "repeatable-list",
        "inherited": False,
        "initial": "auto",
        "multiplicity": "coordinating-list",
        "max-values": 2,
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["auto", "cover", "contain"],
        "percentages-resolve-to": "length",
    },
    "mask-type": {
        "animation-type": "discrete",
        "inherited": False,
        "affects-layout": False,
        "multiplicity": "coordinating-list",
        "valid-types": ["mask-type"],
        "initial": "luminance",
    },
    "math-depth": {
        "animation-type": "none",
        "inherited": True,
        "initial": "0",
        "__comment": "FIXME: `add(<integer>)` is also valid but we can't represent that here yet.",
        "valid-types": ["integer"],
        "valid-identifiers": ["auto-add"],
    },
    "math-shift": {
        "animation-type": "none",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["math-shift"],
    },
    "math-style": {
        "animation-type": "none",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["math-style"],
    },
    "max-block-size": {
        "logical-alias-for": {"group": "max-size", "mapping": "block-size"},
        "initial": "none",
    },
    "max-height": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "none",
        "valid-types": ["fit-content", "length [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["max-content", "min-content", "none"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "max-inline-size": {
        "logical-alias-for": {"group": "max-size", "mapping": "inline-size"},
        "initial": "none",
    },
    "max-width": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "none",
        "valid-types": ["fit-content", "length [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["max-content", "min-content", "none"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "min-block-size": {
        "logical-alias-for": {"group": "min-size", "mapping": "block-size"},
        "initial": "0",
    },
    "min-height": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["fit-content", "length [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["auto", "max-content", "min-content"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "min-inline-size": {
        "logical-alias-for": {"group": "min-size", "mapping": "inline-size"},
        "initial": "0",
    },
    "min-width": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["fit-content", "length [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["auto", "max-content", "min-content"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "mix-blend-mode": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "normal",
        "valid-types": ["mix-blend-mode"],
    },
    "object-fit": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "fill",
        "valid-types": ["object-fit"],
    },
    "object-position": {
        "animation-type": "repeatable-list",
        "affects-layout": False,
        "inherited": False,
        "initial": "50% 50%",
        "valid-types": ["position"],
        "percentages-resolve-to": "length",
    },
    "opacity": {
        "animation-type": "by-computed-value",
        "affects-layout": False,
        "affects-stacking-context": True,
        "inherited": False,
        "initial": "1",
        "valid-types": ["opacity"],
    },
    "order": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["integer [-∞,∞]"],
    },
    "orphans": {
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "2",
        "valid-types": ["integer [1,∞]"],
        "__comment": "FIXME: We don't implement this property any further than compute time",
    },
    "outline": {
        "affects-layout": False,
        "inherited": False,
        "initial": "medium currentColor none",
        "longhands": ["outline-color", "outline-style", "outline-width"],
    },
    "outline-color": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "__comment": "FIXME: We don't yet support `invert`. Until we do, the spec directs us to use `currentColor` as the default instead, and reject `invert`",
        "initial": "currentColor",
        "valid-types": ["color"],
    },
    "outline-offset": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [-∞,∞]"],
    },
    "outline-style": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "none",
        "valid-types": ["outline-style"],
    },
    "outline-width": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "medium",
        "valid-types": ["length [0,∞]", "line-width"],
    },
    "overflow": {
        "longhands": ["overflow-x", "overflow-y"],
        "positional-value-list-shorthand": True,
        "inherited": False,
        "initial": "visible",
        "valid-types": ["overflow"],
    },
    "overflow-block": {
        "logical-alias-for": {"group": "overflow", "mapping": "block-xy"}
    },
    "overflow-inline": {
        "logical-alias-for": {"group": "overflow", "mapping": "inline-xy"}
    },
    "overflow-wrap": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "normal",
        "valid-identifiers": ["anywhere", "break-word", "normal"],
    },
    "overflow-x": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "visible",
        "valid-types": ["overflow"],
        "valid-identifiers": ["overlay>auto"],
    },
    "overflow-y": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "visible",
        "valid-types": ["overflow"],
        "valid-identifiers": ["overlay>auto"],
    },
    "padding": {
        "inherited": False,
        "initial": "0",
        "positional-value-list-shorthand": True,
        "longhands": ["padding-top", "padding-right", "padding-bottom", "padding-left"],
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "padding-block": {
        "initial": "0",
        "positional-value-list-shorthand": True,
        "longhands": ["padding-block-start", "padding-block-end"],
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
        "needs-layout-for-getcomputedstyle": True,
    },
    "padding-block-end": {
        "logical-alias-for": {"group": "padding", "mapping": "block-end"},
        "needs-layout-for-getcomputedstyle": True,
    },
    "padding-block-start": {
        "logical-alias-for": {"group": "padding", "mapping": "block-start"},
        "needs-layout-for-getcomputedstyle": True,
    },
    "padding-bottom": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "padding-inline": {
        "initial": "0",
        "positional-value-list-shorthand": True,
        "longhands": ["padding-inline-start", "padding-inline-end"],
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
        "needs-layout-for-getcomputedstyle": True,
    },
    "padding-inline-end": {
        "logical-alias-for": {"group": "padding", "mapping": "inline-end"}
    },
    "padding-inline-start": {
        "logical-alias-for": {"group": "padding", "mapping": "inline-start"},
        "needs-layout-for-getcomputedstyle": True,
    },
    "padding-left": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "padding-right": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "padding-top": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "paint-order": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "normal",
        "valid-identifiers": ["normal"],
        "valid-types": ["paint-order"],
    },
    "perspective": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "none",
        "valid-identifiers": ["none"],
        "valid-types": ["length [0,∞]"],
    },
    "place-content": {
        "inherited": False,
        "initial": "normal",
        "longhands": ["align-content", "justify-content"],
    },
    "place-items": {
        "inherited": False,
        "initial": "normal",
        "longhands": ["align-items", "justify-items"],
    },
    "place-self": {
        "inherited": False,
        "initial": "normal",
        "longhands": ["align-self", "justify-self"],
    },
    "pointer-events": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": True,
        "initial": "auto",
        "valid-types": ["pointer-events"],
    },
    "position": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "static",
        "valid-types": ["positioning"],
    },
    "position-anchor": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["dashed-ident"],
        "valid-identifiers": ["auto"],
    },
    "position-area": {
        "animation-type": "discrete",
        "__comment": "Animation type is currently listed as TBD in the specification",
        "inherited": False,
        "initial": "none",
        "valid-types": ["position-area"],
        "valid-identifiers": ["none"],
    },
    "position-try-fallbacks": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "none",
        "valid-types": ["dashed-ident", "try-tactic"],
        "valid-identifiers": ["none"],
    },
    "position-try-order": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "normal",
        "valid-types": ["try-order"],
        "valid-identifiers": ["normal"],
    },
    "position-visibility": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "anchors-visible",
        "valid-identifiers": [
            "always",
            "anchors-valid",
            "anchors-visible",
            "no-overflow",
        ],
    },
    "quotes": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "auto",
        "multiplicity": "list",
        "valid-types": ["string"],
        "valid-identifiers": ["auto", "none"],
    },
    "r": {
        "__comment": "This is an SVG 2 geometry property, see: https://www.w3.org/TR/SVG/geometry.html#R.",
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "right": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]", "anchor"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "rotate": {
        "animation-type": "custom",
        "inherited": False,
        "initial": "none",
        "affects-layout": False,
        "affects-stacking-context": True,
    },
    "row-gap": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "normal",
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["normal"],
        "percentages-resolve-to": "length",
    },
    "rx": {
        "__comment": "This is an SVG 2 geometry property, see: https://www.w3.org/TR/SVG/geometry.html#RX.",
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "ry": {
        "__comment": "This is an SVG 2 geometry property, see: https://www.w3.org/TR/SVG/geometry.html#RY.",
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "scale": {
        "animation-type": "custom",
        "inherited": False,
        "initial": "none",
        "affects-layout": False,
        "affects-stacking-context": True,
    },
    "scrollbar-color": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "auto",
    },
    "scrollbar-gutter": {
        "affects-layout": False,
        "animation-type": "discrete",
        "__comment": "This property should affect layout per-spec, but ladybird always uses overlay scrollbars so it doesn't in practice.",
        "inherited": False,
        "initial": "auto",
    },
    "scrollbar-width": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["scrollbar-width"],
        "valid-identifiers": ["auto", "thin", "none"],
    },
    "shape-image-threshold": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["opacity"],
    },
    "shape-margin": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
    },
    "shape-outside": {
        "affects-layout": True,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "none",
    },
    "shape-rendering": {
        "affects-layout": True,
        "animation-type": "discrete",
        "inherited": True,
        "initial": "auto",
        "valid-types": ["shape-rendering"],
    },
    "stop-color": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "black",
        "valid-types": ["color"],
    },
    "stop-opacity": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "1",
        "valid-types": ["opacity"],
    },
    "stroke": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "none",
        "valid-types": ["paint"],
    },
    "stroke-dasharray": {
        "animation-type": "custom",
        "inherited": True,
        "initial": "none",
        "affects-layout": False,
        "percentages-resolve-to": "length",
    },
    "stroke-dashoffset": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "0px",
        "valid-types": ["length [0,∞]", "number [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
    },
    "stroke-linecap": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": True,
        "initial": "butt",
        "valid-types": ["stroke-linecap"],
    },
    "stroke-linejoin": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": True,
        "initial": "miter",
        "valid-types": ["stroke-linejoin"],
    },
    "stroke-miterlimit": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "4",
        "valid-types": ["number [0,∞]"],
    },
    "stroke-opacity": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "1",
        "valid-types": ["opacity"],
    },
    "stroke-width": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "1px",
        "valid-types": ["length [0,∞]", "number [0,∞]", "percentage [0,∞]"],
        "percentages-resolve-to": "length",
    },
    "tab-size": {
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "8",
        "valid-types": ["length [0,∞]", "number [0,∞]"],
    },
    "table-layout": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["table-layout"],
    },
    "text-align": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "start",
        "valid-types": ["text-align"],
    },
    "text-anchor": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "start",
        "valid-types": ["text-anchor"],
    },
    "text-decoration": {
        "affects-layout": False,
        "inherited": False,
        "initial": "none",
        "longhands": [
            "text-decoration-color",
            "text-decoration-line",
            "text-decoration-style",
            "text-decoration-thickness",
        ],
    },
    "text-decoration-color": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "currentcolor",
        "valid-types": ["color"],
    },
    "text-decoration-line": {
        "affects-layout": False,
        "animation-type": "discrete",
        "__comment": "FIXME: This property is not supposed to be inherited, but we currently rely on inheritance to propagate decorations into line boxes.",
        "inherited": True,
        "initial": "none",
        "valid-types": ["text-decoration-line"],
    },
    "text-decoration-style": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": False,
        "initial": "solid",
        "valid-types": ["text-decoration-style"],
    },
    "text-decoration-thickness": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["auto", "from-font"],
        "percentages-resolve-to": "length",
    },
    "text-indent": {
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "0",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "text-justify": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "auto",
        "valid-types": ["text-justify"],
        "valid-identifiers": ["distribute>inter-character"],
    },
    "text-overflow": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": False,
        "initial": "clip",
        "valid-types": ["text-overflow"],
    },
    "text-rendering": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": True,
        "initial": "auto",
        "valid-types": ["text-rendering"],
    },
    "text-shadow": {
        "affects-layout": False,
        "animation-type": "custom",
        "inherited": True,
        "initial": "none",
        "valid-identifiers": ["none"],
    },
    "text-transform": {
        "__comment": "NOTE: This property has custom invalidation handling.",
        "animation-type": "discrete",
        "inherited": True,
        "initial": "none",
        "valid-types": ["text-transform"],
    },
    "text-underline-offset": {
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "auto",
        "valid-identifiers": ["auto"],
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "percentages-resolve-to": "length",
    },
    "text-underline-position": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "auto",
        "valid-types": [
            "text-underline-position-horizontal",
            "text-underline-position-vertical",
        ],
    },
    "text-wrap": {
        "inherited": True,
        "initial": "wrap",
        "longhands": ["text-wrap-mode", "text-wrap-style"],
    },
    "text-wrap-mode": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "wrap",
        "valid-types": ["text-wrap-mode"],
    },
    "text-wrap-style": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "auto",
        "valid-types": ["text-wrap-style"],
    },
    "top": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]", "anchor"],
        "valid-identifiers": ["auto"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "touch-action": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "auto",
        "max-values": 2,
        "valid-types": ["touch-action"],
    },
    "transform": {
        "animation-type": "custom",
        "inherited": False,
        "initial": "none",
        "affects-layout": False,
        "affects-stacking-context": True,
        "percentages-resolve-to": "length",
        "valid-types": ["transform-list"],
        "valid-identifiers": ["none"],
    },
    "transform-box": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "view-box",
        "affects-layout": False,
        "valid-types": ["transform-box"],
    },
    "transform-origin": {
        "affects-layout": False,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "50% 50%",
        "max-values": 3,
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["bottom", "center", "left", "right", "top"],
        "percentages-resolve-to": "length",
    },
    "transform-style": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "flat",
        "valid-identifiers": ["flat", "preserve-3d"],
    },
    "transition": {
        "affects-layout": False,
        "inherited": False,
        "initial": "none",
        "multiplicity": "coordinating-list",
        "longhands": [
            "transition-property",
            "transition-duration",
            "transition-timing-function",
            "transition-delay",
            "transition-behavior",
        ],
    },
    "transition-behavior": {
        "affects-layout": False,
        "animation-type": "none",
        "inherited": False,
        "initial": "normal",
        "multiplicity": "coordinating-list",
        "valid-types": ["transition-behavior"],
    },
    "transition-delay": {
        "affects-layout": False,
        "animation-type": "none",
        "inherited": False,
        "initial": "0s",
        "multiplicity": "coordinating-list",
        "valid-types": ["time"],
    },
    "transition-duration": {
        "affects-layout": False,
        "animation-type": "none",
        "inherited": False,
        "initial": "0s",
        "multiplicity": "coordinating-list",
        "valid-types": ["time [0,∞]"],
    },
    "transition-property": {
        "affects-layout": False,
        "animation-type": "none",
        "inherited": False,
        "initial": "all",
        "multiplicity": "coordinating-list",
        "valid-types": ["custom-ident ![none]"],
        "valid-identifiers": ["none"],
    },
    "transition-timing-function": {
        "affects-layout": False,
        "animation-type": "none",
        "inherited": False,
        "initial": "ease",
        "multiplicity": "coordinating-list",
        "valid-types": ["easing-function", "easing-keyword"],
    },
    "translate": {
        "animation-type": "custom",
        "inherited": False,
        "initial": "none",
        "affects-layout": False,
        "affects-stacking-context": True,
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "percentages-resolve-to": "length",
    },
    "unicode-bidi": {
        "animation-type": "none",
        "inherited": False,
        "initial": "normal",
        "valid-types": ["unicode-bidi"],
    },
    "user-select": {
        "affects-layout": False,
        "animation-type": "discrete",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["user-select"],
    },
    "vertical-align": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "baseline",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]", "vertical-align"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "view-transition-name": {
        "affects-layout": False,
        "affects-stacking-context": True,
        "animation-type": "discrete",
        "inherited": False,
        "initial": "none",
        "valid-types": ["custom-ident ![auto,none]"],
        "valid-identifiers": ["none"],
    },
    "visibility": {
        "animation-type": "custom",
        "inherited": True,
        "initial": "visible",
        "valid-types": ["visibility"],
    },
    "white-space": {
        "inherited": False,
        "initial": "normal",
        "valid-types": ["white-space"],
        "longhands": ["white-space-collapse", "text-wrap-mode", "white-space-trim"],
    },
    "white-space-collapse": {
        "animation-type": "discrete",
        "inherited": True,
        "initial": "collapse",
        "valid-types": ["white-space-collapse"],
    },
    "white-space-trim": {
        "animation-type": "discrete",
        "inherited": False,
        "initial": "none",
        "valid-identifiers": [
            "none",
            "discard-before",
            "discard-after",
            "discard-inner",
        ],
    },
    "widows": {
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "2",
        "valid-types": ["integer [1,∞]"],
        "__comment": "FIXME: We don't implement this property any further than compute time",
    },
    "width": {
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["fit-content", "length [0,∞]", "percentage [0,∞]"],
        "valid-identifiers": ["auto", "max-content", "min-content"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
        "needs-layout-for-getcomputedstyle": True,
    },
    "will-change": {
        "affects-layout": False,
        "affects-stacking-context": True,
        "animation-type": "none",
        "inherited": False,
        "initial": "auto",
        "multiplicity": "list",
        "valid-types": [
            "custom-ident ![all,auto,contents,none,scroll-position,will-change]"
        ],
        "valid-identifiers": ["auto", "scroll-position", "contents"],
    },
    "word-break": {
        "animation-type": "discrete",
        "initial": "normal",
        "inherited": True,
        "valid-identifiers": ["normal", "keep-all", "break-all", "break-word"],
    },
    "word-spacing": {
        "animation-type": "by-computed-value",
        "inherited": True,
        "initial": "normal",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "valid-identifiers": ["normal"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "word-wrap": {"legacy-alias-for": "overflow-wrap"},
    "writing-mode": {
        "animation-type": "none",
        "inherited": True,
        "initial": "horizontal-tb",
        "valid-types": ["writing-mode"],
    },
    "x": {
        "__comment": "This is an SVG 2 geometry property, see: https://www.w3.org/TR/SVG/geometry.html#X.",
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "y": {
        "__comment": "This is an SVG 2 geometry property, see: https://www.w3.org/TR/SVG/geometry.html#Y.",
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "0",
        "valid-types": ["length [-∞,∞]", "percentage [-∞,∞]"],
        "percentages-resolve-to": "length",
        "quirks": ["unitless-length"],
    },
    "z-index": {
        "affects-layout": False,
        "affects-stacking-context": True,
        "animation-type": "by-computed-value",
        "inherited": False,
        "initial": "auto",
        "valid-types": ["integer [-∞,∞]"],
        "valid-identifiers": ["auto"],
    },
}  # fmt: on

def shorthand_to_longhands(prop: Property) -> list[Property]:
    out: list[Property] = []
    longhands = PROPERTIES.get(prop.value, {}).get("longhands", [])
    assert isinstance(longhands, list)
    for longhand in longhands:
        assert longhand in Property
        out.append(Property(longhand))
    
    return out
    

def keyword_group_to_keywords(kw_group: str) -> dict[Keyword, KeywordGroup]:
    if kw_group in KEYWORD_GROUPS:
        enum_cls = KEYWORD_GROUPS[kw_group]
        return {Keyword(member.value): member for member in enum_cls}
    return {}


def keyword_to_keyword_group_keyword(
    keyword: Keyword, group: Type[Enum]
) -> Enum | None:
    """ex: (Keyword.INSIDE, group=AnchorSide) -> AnchorSide.INSIDE"""
    if keyword.value in group._value2member_map_:
        return group(keyword.value)


# type_range = "type [low,high]"
def _is_in_range(type_range: str, value) -> bool:
    assert "[" in type_range
    lo, hi = type_range.split(" ", 1)[1][1:-1].split(",")
    lo = float("-inf") if "∞" in lo else int(lo)
    hi = float("inf") if "∞" in hi else int(hi)
    return lo <= value <= hi


def property_accepted_types(property: Property) -> set[ValueType]:
    valid_types = PROPERTIES.get(property.value, {}).get("valid-types", [])
    assert isinstance(valid_types, list)
    out = set()
    for type in valid_types:
        type_name = type.split(" ")[0]
        if type_name in ValueType._value2member_map_:
            out.add(ValueType._value2member_map_[type_name])
    return out if out else set()


def property_accepted_keywords(property: Property) -> set[Keyword]:
    prop = PROPERTIES.get(property.value, {})
    valid_types = prop.get("valid-types", [])
    valid_idents = prop.get("valid-identifiers", [])
    assert isinstance(valid_types, list)
    assert isinstance(valid_idents, list)
    out = set()
    for type in valid_types:
        type_name = type.split(" ")[0]
        if type_name not in ValueType._value2member_map_:

            kws = keyword_group_to_keywords(type_name)
            if kws:
                out.update(kws)
            else:
                warn(
                    f"! {property} accepts keyword type {type_name}, but no such keyword exists"
                )

    for ident in valid_idents:
        try:
            out.add(Keyword(ident))
        except Exception:
            err(
                f"valid-identifiers for {property} has {ident}, which does not map to any Keyword enum"
            )
    return out if out else set()


def property_accepts_type(property: Property, type: ValueType) -> bool:
    valid_types = PROPERTIES.get(property.value, {}).get("valid-types", [])
    assert isinstance(valid_types, list)
    if not valid_types:
        return False

    for t in valid_types:
        t = t.split(" ")[0]  # ignore any numerical constraints like [0, ∞]
        if type.value == t:
            return True
    return False


def property_accepts_keyword(property: Property, keyword: Keyword):
    # checks keyword against valid-identifiers
    # then against valid-types, but only if type is non-generic
    prop = PROPERTIES.get(property.value, {})
    valid_types = prop.get("valid-types", [])
    valid_idents = prop.get("valid-identifiers", [])
    assert isinstance(valid_types, list)
    assert isinstance(valid_idents, list)
    if valid_idents:
        for i in valid_idents:
            if keyword.value == i:
                return True

    # if not in valid_identifiers, check in valid-types for non-generic identifiers
    if not valid_types:
        return False

    for t in valid_types:
        t = t.split(" ")[0]
        # non-generic identifiers are the ones that are not found in ValueType (enum)
        if t in ValueType._member_map_:
            continue

        if keyword in keyword_group_to_keywords(t):
            return True
    return False


def property_accepts_integer(property: Property, i: int) -> bool:
    valid_types = PROPERTIES.get(property.value, {}).get("valid-types", [])
    assert isinstance(valid_types, list)
    for t in valid_types:
        if "integer [" in t:
            return _is_in_range(t, i)
        elif "integer" in t:
            return True
    return False


def property_accepts_number(property: Property, num: float) -> bool:
    valid_types = PROPERTIES.get(property.value, {}).get("valid-types", [])
    assert isinstance(valid_types, list)
    for t in valid_types:
        if "number [" in t:
            return _is_in_range(t, num)
        elif "number" in t:
            return True
    return False


def property_accepts_angle(property: Property, degs: float) -> bool:
    valid_types = PROPERTIES.get(property.value, {}).get("valid-types", [])
    assert isinstance(valid_types, list)
    for t in valid_types:
        if "angle [" in t:
            return _is_in_range(t, degs)
        elif "angle" in t:
            return True
    return False


def property_accepts_percentage(property: Property, percentage: float) -> bool:
    valid_types = PROPERTIES.get(property.value, {}).get("valid-types", [])
    assert isinstance(valid_types, list)
    for t in valid_types:
        if "percentage [" in t:
            return _is_in_range(t, percentage)
        elif "percentage" in t:
            return True
    return False


def property_accepts_length(property: Property, length: float) -> bool:
    valid_types = PROPERTIES.get(property.value, {}).get("valid-types", [])
    assert isinstance(valid_types, list)
    for t in valid_types:
        if "length [" in t:
            return _is_in_range(t, length)
        elif "length" in t:
            return True
    return False


def property_accepts_time(property: Property, time: float) -> bool:
    valid_types = PROPERTIES.get(property.value, {}).get("valid-types", [])
    assert isinstance(valid_types, list)
    for t in valid_types:
        if "time [" in t:
            return _is_in_range(t, time)
        elif "time" in t:
            return True
    return False


def property_is_inherited(property: Property) -> bool:
    is_inherited = PROPERTIES.get(property.value, {}).get("inherited", False)
    assert isinstance(is_inherited, bool), is_inherited
    return is_inherited


def property_is_positional_value_list_shorthand(property: Property) -> bool:
    is_positional_value_list_shorthand = PROPERTIES.get(property.value, {}).get(
        "positional-value-list-shorthand", False
    )
    assert isinstance(is_positional_value_list_shorthand, bool)
    return is_positional_value_list_shorthand


if __name__ == "__main__":
    set_debug()

    PROP = Property.COLOR

    log(property_accepts_type(PROP, ValueType.LENGTH))
    log(property_accepts_keyword(PROP, Keyword.X_SMALL))
    log(property_is_inherited(PROP))

    log("Accepted types:", property_accepted_types(PROP))
    log("Accepted keywords:", property_accepted_keywords(PROP))

    # print ALL unique keyword groups (aka value objects)
    unique = set()
    for prop in PROPERTIES.values():
        if not isinstance(prop, dict):
            continue
        valid = prop.get("valid-types")
        assert isinstance(valid, list)
        if not valid:
            continue
        for type in valid:
            if type.split(" ")[0] in ValueType._value2member_map_:
                continue
            unique.add(type)

    unique = sorted(list(unique))

    log("Unique keyword groups: ", unique)
