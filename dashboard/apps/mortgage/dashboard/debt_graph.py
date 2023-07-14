from streamlit_echarts import st_echarts
import json
import streamlit_elements
import streamlit as st
from streamlit import session_state as state
from streamlit_elements import nivo

from .dashboard import Dashboard
from .mortgage import Mortgage, RefactorMortgage, dollar


class DebtGraph(Dashboard.Item):

    def __call__(self, *args, **kwargs):
        options = {
                "xAxis": {
                    "type": "value"},
                        "yAxis": {"type": "value"},
                        "series": [
                            
                            # {"data":m2d, "type": "line"}
                        ],
                    }
        for i in state.interest_rate:

            m1 = Mortgage(interest=state.interest_rate[0]/100,amount=dollar(state.debt-state.one_time),months=state.terms*12)
            
            # m2 = RefactorMortgage.byInterest(m1,interest=state.interest_rate[1]/100)
            m1d = [[x,i[0]] for x,i in enumerate(m1.monthly_payment_schedule())]
            # m2d = [[x,i[0]] for x,i in enumerate(m2.monthly_payment_schedule())]
            options["series"].append({"data": m1d, "type": "line"},)
            st.text(f"monthly installment {m1.monthly_payment()}. Overall Payment {m1.total_payout()}. Interest Payed {m1.total_interest()}")
            # st.text(f"mortgage 2 monthly installment {m2.monthly_payment()}")
        st_echarts(options=options)
