from __future__ import annotations

from typing import TypedDict

__all__ = ("HCaptchaCustomTheme",)


class Palette(TypedDict, total=False):
    mode: str
    grey: dict[str, str]
    primary: ColorMain
    warn: ColorMain
    text: ColorText


class ColorMain(TypedDict, total=False):
    main: str


class ColorText(TypedDict, total=False):
    heading: str
    body: str


class FillBorder(TypedDict, total=False):
    fill: str
    border: str


class FillIconText(TypedDict, total=False):
    fill: str
    icon: str
    text: str


class FocusOutline(TypedDict, total=False):
    outline: str
    icon: str
    text: str
    fill: str
    border: str


class CheckboxComponent(TypedDict, total=False):
    main: FillBorder
    hover: dict[str, str]


class ModalComponent(TypedDict, total=False):
    main: dict[str, str]
    hover: dict[str, str]
    focus: FocusOutline


class ButtonComponent(TypedDict, total=False):
    main: FillIconText
    hover: dict[str, str]
    focus: FocusOutline
    active: FillIconText


class ListItemComponent(TypedDict, total=False):
    main: dict[str, str]
    hover: dict[str, str]
    selected: dict[str, str]
    focus: FocusOutline


class InputComponent(TypedDict, total=False):
    main: FillBorder
    focus: FocusOutline


class RadioComponent(TypedDict, total=False):
    main: dict[str, str]
    selected: dict[str, str]
    focus: FocusOutline


class TaskComponent(TypedDict, total=False):
    main: dict[str, str]
    selected: dict[str, str]
    report: dict[str, str]
    focus: dict[str, str]


class PromptComponent(TypedDict, total=False):
    main: dict[str, str]
    report: dict[str, str]


class ActionButtonComponent(TypedDict, total=False):
    main: dict[str, str]
    hover: dict[str, str]
    focus: FocusOutline


class SliderComponent(TypedDict, total=False):
    main: dict[str, str]
    focus: dict[str, str]


class TextareaComponent(TypedDict, total=False):
    main: FillBorder
    focus: dict[str, str]
    disabled: dict[str, str]


class Components(TypedDict, total=False):
    checkbox: CheckboxComponent
    modal: ModalComponent
    challenge: CheckboxComponent
    breadcrumb: dict[str, dict[str, str]]
    button: ButtonComponent
    link: dict[str, FocusOutline]
    list: dict[str, FillBorder]
    listItem: ListItemComponent
    input: InputComponent
    radio: RadioComponent
    task: TaskComponent
    prompt: PromptComponent
    skipButton: ActionButtonComponent
    verifyButton: ActionButtonComponent
    slider: SliderComponent
    textarea: TextareaComponent


class HCaptchaCustomTheme(TypedDict, total=False):
    """
    Custom theme for hCaptcha widget styling.

    :param palette: The global color mode and primary/grey palettes.
    :param component: Detailed overrides for every UI element in the widget.
    """

    palette: Palette
    component: Components
