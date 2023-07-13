import json
import streamlit as st

from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace

from .dashboard import Dashboard, Variables, DebtGraph


def main():




    st.title("title ")

    if "widget_order" not in state:
        board = Dashboard()
        widget_order = SimpleNamespace(
            dashboard=board,
            variables=Variables(board,0,0,6,11, minW=3, minH=3),
            debt_graph=DebtGraph(board,6,0,6,11, minW=3,minH=3)
            # editor=Editor(board, 0, 0, 6, 11, minW=3, minH=3),
            # player=Player(board, 0, 12, 6, 10, minH=5),
            # pie=Pie(board, 6, 0, 6, 7, minW=3, minH=4),
            # radar=Radar(board, 12, 7, 3, 7, minW=2, minH=4),
            # card=Card(board, 6, 7, 3, 7, minW=2, minH=4),
            # data_grid=DataGrid(board, 6, 13, 6, 7, minH=4),
        )
        state.widget_order = widget_order

        # widget_order.editor.add_tab("Card content", Card.DEFAULT_CONTENT, "plaintext")
        # widget_order.editor.add_tab("Data grid", json.dumps(DataGrid.DEFAULT_ROWS, indent=2), "json")
        # widget_order.editor.add_tab("Radar chart", json.dumps(Radar.DEFAULT_DATA, indent=2), "json")
        # widget_order.editor.add_tab("Pie chart", json.dumps(Pie.DEFAULT_DATA, indent=2), "json")
    else:
        widget_order = state.widget_order

    with elements("hboard"):
        event.Hotkey("shift+s", sync(), bindInputs=True, overrideDefault=True)
        with widget_order.dashboard(rowHeight=57):

            widget_order.variables()
            widget_order.debt_graph()

            # widget_order.editor()
            # widget_order.player()
            # widget_order.pie(widget_order.editor.get_content("Pie chart"))
            # widget_order.radar(widget_order.editor.get_content("Radar chart"))
            # widget_order.card(widget_order.editor.get_content("Card content"))
            # widget_order.data_grid(widget_order.editor.get_content("Data grid"))


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
