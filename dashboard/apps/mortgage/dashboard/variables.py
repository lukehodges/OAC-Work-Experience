from streamlit_echarts import st_echarts
import json
import streamlit_elements
import streamlit as st
from streamlit import session_state as state
from streamlit_elements import sync

from .dashboard import Dashboard


class Variables(Dashboard.Item):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = {
        "interest": [2.0, 4.0],
        "debt": 100_000,
        "term": 360
    }

    def __call__(self, *args, **kwargs):

        # options = {
        #     "xAxis": {
        #         "type": "category",
        #         #         "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        #         #     },
        #         #     "yAxis": {"type": "value"},
        #         #     "series": [
        #         #         {"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}
        #         #     ],
        #         # }
        # st_echarts(options=options)
        if "interest_rate" not in state:state.interest_rate = [2.0,4.0]
        if "debt" not in state:state.debt = 100_000
        if "rate" not in state: state.rate = 300
        inter = st.slider("Interest_Rate", min_value=0.0, max_value=10.0, step=0.1, value=[2., 4.], key="interest_rate")
        debt = st.slider("Mortgage Debt", min_value=000.0, max_value=1_000_000.0, step=5000.0, value=100_000.0, key="debt")
        terms = st.slider("Mortgage Terms", min_value=000.0, max_value=600.0, step=12.0, value=300.0, key="terms")
        print(inter,debt,terms)

