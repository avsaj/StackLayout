from kivy.uix.layout import Layout
from kivy.properties import OptionProperty

class StackLayout(Layout):
    orientation = OptionProperty('horizontal', options=(
        'horizontal', 'vertical'))

    def __init__(self, **kwargs):
        super(StackLayout, self).__init__(**kwargs)
        self.bind(
            children=self._trigger_layout,
            orientation=self._trigger_layout,
            parent=self._trigger_layout,
            size=self._trigger_layout,
            pos=self._trigger_layout)

    def do_layout(self, *largs):
        len_children = len(self.children)
        if len_children == 0:
            return
        selfx = self.x
        selfy = self.y
        selfw = self.width
        selfh = self.height
        orientation = self.orientation

        row_list = []
        row = []
        if orientation == 'horizontal':
            cursor = 0.0
            for c in reversed(self.children):
                row.append(c)
                cursor += c.size_hint_x
                if cursor > selfw:
                    if len(row) == 1:
                        cursor = 0.0
                        row_list.append(row[:])
                        row = []
                    else:
                        cursor = c.size_hint_x
                        new_row = [row.pop()]
                        row_list.append(row[:])
                        row = new_row
            if row:
                row_list.append(row)

            def get_y(l, r, i):
                if i == 0:
                    return selfh
                row_above = row_list[i - 1]

                def get_index(side):
                    for si, c in enumerate(row_above):
                        if not (round(c.x) < round(side) <= round(c.x + c.width)):
                            continue
                        return si

                li = get_index(l)
                ri = get_index(r)
                return min(c.y for c in row_above[li:ri + 1])

            for i, row in enumerate(row_list):
                base_row_width = sum([float(c.size_hint_x) for c in row])
                cursor = 0.0
                for c in row:
                    percent = c.size_hint_x / base_row_width
                    w = percent * selfw
                    if w > selfw:
                        w = selfw
                    c.width = w
                    c.height = c.size_hint_y * (w / c.size_hint_x)
                    c.x = cursor
                    c.y = get_y(cursor, cursor + w, i) - c.height
                    cursor += w

    def add_widget(self, widget, index=0):
        widget.bind(
            size_hint=self._trigger_layout)
        return super(StackLayout, self).add_widget(widget, index)

    def remove_widget(self, widget):
        widget.unbind(
            size_hint=self._trigger_layout)
        return super(StackLayout, self).remove_widget(widget)