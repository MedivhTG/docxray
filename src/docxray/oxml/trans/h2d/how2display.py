"""Main module that tells `How to display` those XML-representation of DOCX file.

Common use is for HTML-transform.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Generic, Literal, TypeVar, cast

# docxray stuff
from docxray.oxml.trans.enums import WD_CNF_FORMAT
from docxray.oxml.trans.proxy.shared import (
    NotFound,
    PropertyPath,
    safe_get_prop,
)
from docxray.oxml.trans.proxy.styles.style import (
    CharacterStyle,
    NumberingStyle,
    TableStyle,
)
from docxray.oxml.trans.styles import CT_TblStylePr

if TYPE_CHECKING:
    # docxray stuff
    from docxray.oxml.trans.parts.document import DocumentPart

PROXY_T = TypeVar("PROXY_T")

type ResolveAlgorithm = Literal["direct", "style", "both"]


class How2Display(Generic[PROXY_T]):
    """Main class for resolving xml-properties of an proxy-instances such as `Run`, `Paragraph`, etc."""

    def __init__(
        self,
        story: PROXY_T,
        document_part: DocumentPart,
        property_base: str,
    ) -> None:
        self._proxy = story
        self._document_part = document_part
        self._styles = document_part.styles
        self._settings = document_part.settings_part.settings
        num_part = document_part.numbering_part
        if num_part is None:
            self._numbering = None
        else:
            self._numbering = num_part.numbering
        self._path_base = property_base

    def _prop_path(self, name: str, path_base: str = "") -> PropertyPath:
        """Get path to an xml-property.

        For example, you construct path to run italic value:
        ```python
           path = run_h2d._prop_path("val", "rPr.i")
           print(path) # will print `rPr.i.val`
        ```

        Args:
            name (str): Endname of property, e.g. `val`.
            path_base (str, optional): Path to endname property with dot-notation,
            e.g. `pPr.i`. Defaults to "".

        Returns:
            PropertyPath: String inherited instance with path.
        """
        return PropertyPath.base(name, path_base)

    def _prop_direct(self, path: PropertyPath, optional: bool = False) -> Any:
        """Get property directly from an element.

        Args:
            path (PropertyPath): Path to an element in element tree.
            optional (bool, optional): If endname property can be `None` and you
                won't get `NotFound` instance instead. Defaults to False.

        Returns:
            Any: `NotFound` instance or Any value.
        """
        elm = getattr(self._proxy, "element")
        return safe_get_prop(elm, path, optional)

    def _prop_style(self, path: PropertyPath, optional: bool = False) -> Any:
        """Get property from style hierarchy.

        Args:
            path (PropertyPath): Path to an element in element tree.
            optional (bool, optional): If endname property can be `None` and you
                won't get `NotFound` instance instead. Defaults to False.

        Returns:
            Any: `NotFound` instance or Any value.
        """
        return self._from_styles_hierarchy(path, optional)

    def _prop_both(self, path: PropertyPath, optional: bool = False) -> Any:
        """Get property directly and if it's `NotFound` instance return from style hierarchy.

        Args:
            path (PropertyPath): Path to an element in element tree.
            optional (bool, optional): If endname property can be `None` and you
                won't get `NotFound` instance instead. Defaults to False.

        Returns:
            Any: `NotFound` instance or Any value.
        """
        elm = getattr(self._proxy, "element")
        direct_val = safe_get_prop(elm, path, optional)
        if isinstance(direct_val, NotFound):
            return self._from_styles_hierarchy(path, optional)
        return direct_val

    def _prop(
        self,
        name_or_path: str | PropertyPath,
        optional: bool = False,
        algorithm: ResolveAlgorithm = "direct",
    ) -> Any:
        """Main method for getting properties.

        If given param `name_or_path` is string, then it will be converted to
        `PropertyPath` isntance with endname as is and with path to tag from `property_base`
        given for instance earlier, e.g. for endname `i` and path_base `rPr` it will be converted to
        `rPr.i` representation.

        Args:
            name_or_path (str | PropertyPath): Endname of desired tag or override path to tag.
            optional (bool, optional): If endname property can be `None` and you
                won't get `NotFound` instance instead. Defaults to False.
            algorithm (ResolveAlgorithm, optional): Desired method for getting property.
                Defaults to "direct".

        Returns:
            Any: `NotFound` instance or Any value.
        """
        if isinstance(name_or_path, PropertyPath):
            path = name_or_path
        else:
            path = self._prop_path(name_or_path, self._path_base)
        match algorithm:
            case "direct":
                return self._prop_direct(path, optional)
            case "style":
                return self._prop_style(path, optional)
            case "both":
                return self._prop_both(path, optional)

    def _prop_val(
        self,
        name_or_path: str | PropertyPath,
        optional: bool = False,
        algorithm: ResolveAlgorithm = "direct",
    ) -> Any:
        """Main method for getting property values.

        Same as `_prop` method but if your param `name_or_path` is an string you will
        get attribute with endname `val`, e.g. for endname `i` and path_base `rPr` you will
        get `rPr.i.val` representation.

        Args:
            name_or_path (str | PropertyPath): Endname of desired tag or override path to tag.
            optional (bool, optional): If endname property can be `None` and you
                won't get `NotFound` instance instead. Defaults to False.
            algorithm (ResolveAlgorithm, optional): Desired method for getting property.
                Defaults to "direct".

        Returns:
            Any: `NotFound` instance or Any value.
        """
        path = (
            name_or_path
            if isinstance(name_or_path, PropertyPath)
            else self._prop_path("val", f"{self._path_base}.{name_or_path}")
        )
        return self._prop(path, optional, algorithm)

    def _table_style_props(
        self, table_style: TableStyle, cnf: WD_CNF_FORMAT
    ) -> list[CT_TblStylePr]:
        """Get desired table style properties from given tables using an cnf bit mask.

        Args:
            table_style (TableStyle): Given table style
            cnf (WD_CNF_FORMAT): Fiven conditional formatting for table (CNF) bit mask.

        Returns:
            list[CT_TblStylePr]: List of table style properties.
        """
        props = []
        for flag in WD_CNF_FORMAT.ordered_flags():
            format = cnf & flag
            if format:
                tblStylePr_elm = table_style.bitwise_tbl_style_prop(flag)
                if tblStylePr_elm is not None:
                    props.append(tblStylePr_elm)
        if table_style.wholeTable:
            props.append(table_style.wholeTable)
        return props

    def _from_tbl_style_hierarchy(
        self,
        tbl_style_props_deep: list[tuple[TableStyle, list[CT_TblStylePr]]],
        path: PropertyPath,
        optional: bool = False,
    ) -> tuple[Any, TableStyle | CT_TblStylePr | None]:
        """Get property value from complex table style hierarchy.

        Here is 4 cases for 2nd value in tuple:
        1) For `None` there is no value from style hierarchy (can be found directly).
        2) For `CT_TblStylePr` you've got value from an grid group of and table style property.
        3) For `TableStyle` you've got an value from table style (can be an fallback or not).

        Args:
            tbl_style_props_deep (list[tuple[TableStyle, list[CT_TblStylePr]]]): Full list of an applied
                pairs `TableStyle` and table style properties inside from style hierarchy.
            path (PropertyPath): Path to an element in element tree.
            optional (bool, optional): If endname property can be `None` and you
                won't get `NotFound` instance instead. Defaults to False.

        Returns:
            tuple[Any, TableStyle | CT_TblStylePr | None]: Context as pair of
                an got property value an applied table style or table style property (grid group)
                or `None`.
        """
        style_direct_val = NotFound(self, path)
        found_in_style = None
        for tbl_style, tbl_style_props in tbl_style_props_deep:
            if isinstance(style_direct_val, NotFound):
                style_direct_val = safe_get_prop(
                    tbl_style.element, path, optional
                )
                found_in_style = tbl_style
            tbl_val, tbl_style_prop = self._from_tbl_style_props(
                tbl_style_props, path, optional
            )
            if not isinstance(tbl_val, NotFound):
                return tbl_val, cast("CT_TblStylePr", tbl_style_prop)
        return style_direct_val, found_in_style

    def _from_tbl_style_props(
        self,
        table_style_props: list[CT_TblStylePr],
        path: PropertyPath,
        optional: bool = False,
    ) -> tuple[Any, CT_TblStylePr | None]:
        """Get property value from table style properties (grid group).

        Args:
            table_style_props (list[CT_TblStylePr]): Provided table style properties on an given table style level.
            path (PropertyPath): Path to an element in element tree.
            optional (bool, optional): If endname property can be `None` and you
                won't get `NotFound` instance instead. Defaults to False.

        Returns:
            tuple[Any, CT_TblStylePr | None]: Tuple of found (`NotFound` instance or Any value) and in which
                table style property was found chosen property.
        """
        for tbl_style_prop in table_style_props:
            table_val = safe_get_prop(tbl_style_prop, path, optional)
            if isinstance(table_val, NotFound):
                continue
            return table_val, tbl_style_prop
        return NotFound(table_style_props, path), None

    def _from_doc_dflts(
        self, path: PropertyPath, optional: bool = False
    ) -> Any:
        """Get property value directly from document deafults in styles.

        Args:
            path (PropertyPath): Path to an element in element tree.
            optional (bool, optional): If endname property can be `None` and you
                won't get `NotFound` instance instead. Defaults to False.

        Returns:
            Any: `NotFound` instance or Any value.
        """
        doc_dflts = self._styles.document_defaults
        if doc_dflts is None:
            return NotFound(self._styles, path)
        return safe_get_prop(doc_dflts.element, path, optional)

    def _from_style_inheritance(
        self,
        style: CharacterStyle | NumberingStyle,
        path: PropertyPath,
        optional: bool = False,
    ) -> Any:
        """Iterate over style hierarchy with same style from given to get property value.

        Args:
            style (CharacterStyle | NumberingStyle): Given style.
            path (PropertyPath): Path to an element in element tree.
            optional (bool, optional): If endname property can be `None` and you
                won't get `NotFound` instance instead. Defaults to False.

        Returns:
            Any: `NotFound` instance or Any value.
        """
        val = NotFound(style, path)
        while isinstance(val, NotFound):
            val = safe_get_prop(style.element, path, optional)
            base_style = self._styles.base_style(style)
            if not isinstance(base_style, style.__class__):
                return val
            style = base_style
        return val

    @abstractmethod
    def _from_styles_hierarchy(
        self, path: PropertyPath, optional: bool = False, **kwargs: Any
    ) -> Any:
        """Main method for getting property values from style hierarchy.

        Common order (from spec ECMA-376, Part 1, 17.7.2 Style Hierarchy):
        1) First, the document defaults are applied to all runs and paragraphs in the document.
        2) Next, the table style properties are applied to each table in the document, following the conditional
        formatting inclusions and exclusions specified per table.
        3) Next, numbered item and paragraph properties are applied to each paragraph formatted with a
        numbering style.
        4) Next, paragraph and run properties are applied to each paragraph as defined by the paragraph style.
        5) Next, run properties are applied to each run with a specific character style applied.
        6) Finally, we apply direct formatting (paragraph or run properties not from styles). If this direct formatting
        includes numbering, that numbering + the associated paragraph properties are applied.

        But for speeding up process we getting values in reversed order (from highest to lowest),
        first value that is not `NotFound` instance will be used as primary.

        Args:
            path (PropertyPath): Path to an element in element tree.
            optional (bool, optional): If endname property can be `None` and you
                won't get `NotFound` instance instead. Defaults to False.

        Returns:
            Any: `NotFound` instance or Any value.
        """
