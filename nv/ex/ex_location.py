# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

from sublime import Region


def get_line_nr(view, point):
    # type: (...) -> int
    """Return 1-based line number for `point`."""
    return view.rowcol(point)[0] + 1


# TODO: Move this to sublime_lib; make it accept a point or a region.
def find_eol(view, point):
    # type: (...) -> int
    return view.line(point).end()


# TODO: Move this to sublime_lib; make it accept a point or a region.
def find_bol(view, point):
    # type: (...) -> int
    return view.line(point).begin()


# TODO: make this return None for failures.
def find_line(view, start=0, end=-1, target=0):
    """
    Do a binary search to find :target: line number.

    Return: If `target` is found, `Region` comprising entire line no. `target`.
            If `target`is not found, `-1`.
    """
    # Don't bother if sought line is beyond buffer boundaries.
    if target < 0 or target > view.rowcol(view.size())[0] + 1:
        return -1

    if end == -1:
        end = view.size()

    lo, hi = start, end
    while lo <= hi:
        middle = lo + (hi - lo) / 2
        if get_line_nr(view, middle) < target:
            lo = find_eol(view, middle) + 1
        elif get_line_nr(view, middle) > target:
            hi = find_bol(view, middle) - 1
        else:
            return view.full_line(middle)

    return -1


def search_in_range(view, what, start, end, flags=0):
    match = view.find(what, start, flags)
    if match and ((match.begin() >= start) and (match.end() <= end)):
        return True


def find_last_match(view, what, start, end, flags=0):
    """Find last occurrence of `what` between `start`, `end`."""
    match = view.find(what, start, flags)
    new_match = None
    while match:
        new_match = view.find(what, match.end(), flags)
        if new_match and new_match.end() <= end:
            match = new_match
        else:
            return match


def reverse_search(view, what, start=0, end=-1, flags=0):
    """Do binary search to find `what` walking backwards in the buffer."""
    if end == -1:
        end = view.size()

    end = find_eol(view, view.line(end).a)

    last_match = None

    lo, hi = start, end
    while True:
        middle = (lo + hi) / 2
        line = view.line(middle)
        middle, eol = find_bol(view, line.a), find_eol(view, line.a)  # FIXME # noqa: F841

        if search_in_range(view, what, middle, hi, flags):
            lo = middle
        elif search_in_range(view, what, lo, middle - 1, flags):
            hi = middle - 1

        # Don't search forever the same line.
        if last_match and line.contains(last_match):
            match = find_last_match(view, what, lo, hi, flags=flags)

            return view.rowcol(match.begin())[0] + 1

        last_match = Region(line.begin(), line.end())


def calculate_relative_ref(view, where, start_line=None):
    if where == '$':
        return view.rowcol(view.size())[0] + 1

    if where == '.':
        if start_line:
            return view.rowcol(view.text_point(start_line, 0))[0] + 1

        return view.rowcol(view.sel()[0].begin())[0] + 1


def search(view, what, start_line=None, flags=0):
    # TODO: don't make start_line default to the first sel's begin(). It's
    # confusing. ???
    if start_line:
        start = view.text_point(start_line, 0)
    else:
        start = view.sel()[0].begin()

    reg = view.find(what, start, flags)

    if reg is not None:
        row = (view.rowcol(reg.begin())[0] + 1)
    else:
        row = calculate_relative_ref(view, '.', start_line=start_line)

    return row
