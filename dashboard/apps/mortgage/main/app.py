import numpy as np
import pandas as pd
import streamlit as st
from streamlit import session_state as state
from streamlit_echarts import st_echarts

from dashboard.apps.mortgage.mortgage import Mortgage, dollar, RefactorMortgage



def main():
    tab1,tab2,tab3 = st.tabs(["basic", "refactor", "compare"])
    with tab1:
        col1, col2 = st.columns([1, 1])

        with col1:
            inter = st.slider("Interest_Rate", min_value=0.0, max_value=10.0, step=0.1, value=2.0, key="basic_interest_rate")
            debt = st.slider("Mortgage Debt", min_value=0.0, max_value=1_000_000.0, step=5000.0, value=100_000.0,
                             key="basic_debt")
            terms = st.slider("Mortgage Terms", min_value=0.0, max_value=50.0, step=1.0, value=10.0, key="basic_terms")
            cl1, cl2, cl3 = st.columns([1, 1, 1])


            one_off = st.number_input("One Time Payment", key="basic_one_time", step=50)


        with col2:
            options = {
                "xAxis": {
                    "type": "value"},
                "yAxis": {"type": "value"},
                "series": [

                    # {"data":m2d, "type": "line"}
                ],
            }
            m1 = Mortgage(interest=state.basic_interest_rate / 100, amount=dollar(state.basic_debt),
                          months=state.basic_terms * 12)
            m2 = RefactorMortgage.byPrinciple(m1, dollar(state.basic_debt - state.basic_one_time))

            # m2 = RefactorMortgage.byInterest(m1,interest=state.interest_rate[1]/100)
            m1d = [[x / 12, i[0]] for x, i in enumerate(m1.monthly_payment_schedule())]
            m2d = [[x / 12, i[0]] for x, i in enumerate(m2.monthly_payment_schedule())]
            monthly_payment = m1.monthly_payment()
            # m2d = [[x,i[0]] for x,i in enumerate(m2.monthly_payment_schedule())]
            options["series"].append({"data": m1d, "type": "line"}, )
            options["series"].append({"data": m2d, "type": "line"}, )
            st.text(
                f"monthly installment {m1.monthly_payment()}. Overall Payment {m1.total_payout()}. Interest Payed {m1.total_interest()}")
            st.text(
                f"monthly installment {m2.monthly_payment()}. Overall Payment {m2.total_payout()}. Interest Payed {m2.total_interest()}")
            # st.text(f"mortgage 2 monthly installment {m2.monthly_payment()}")
            st_echarts(options=options, key="ddfffddf")
            monthly = m1.monthly_payment()-m2.monthly_payment()
            tot = m1.total_interest() - m2.total_interest()
            st.text(f"monthly saved :{monthly}. total saved: {tot}")
    with tab2:
        col1, col2 = st.columns([1, 1])
        with col1:
            cl1, cl2 = st.columns([1,1])
            with cl1:
                inter = st.slider("Interest_Rate", min_value=0.0, max_value=10.0, step=0.1, value=2.0, key="convert_interest_rate")
                debt = st.slider("Mortgage Debt", min_value=0.0, max_value=1_000_000.0, step=5000.0, value=100_000.0,
                                 key="convert_debt")
                terms = st.slider("Mortgage Terms", min_value=0.0, max_value=50.0, step=1.0, value=10.0, key="convert_terms")
            monthly_payment = st.number_input("monthly_payment", key="convert_one_time", step=50, value=1000)
            with cl2:
                inter_sol = st.slider("Interest_Rate", min_value=0.0, max_value=10.0, step=0.1, value=inter,
                                  disabled=True, key="refactor_inter")
                debt_sol = st.slider("Mortgage Debt", min_value=0.0, max_value=1_000_000.0, step=5000.0, value=debt,
                                 disabled=True, key="refactor_debt")
                terms_sol = st.slider("Mortgage Terms", min_value=0.0, max_value=50.0, step=1.0, value=float(RefactorMortgage.byMonthlyPayment(Mortgage(inter/100,terms*12, dollar(debt)), monthly_payment).months)/12,
                                  disabled=True, key="refactor_terms")

            # def refactor(inter,debt,terms, amt):
            #     m1 = Mortgage(interest=inter, amount=debt, months=terms)
            #     try:
            #         m2 = RefactorMortgage.byMonthlyPayment(m1, amt)
            #     except Exception as e:
            #         st.text("Invalid Parameters Try Again")
            #         return
            #     state.refactor_inter = m2.interest
            #     state.refactor_debt = m2.amount
            #     state.refactor_terms = m2.months
            # apply = st.button("Apply", on_click=refactor, args=[inter,debt,terms,monthly_payment])
        with col2:
            m1 = Mortgage(interest=state.convert_interest_rate / 100, amount=dollar(state.convert_debt),
                          months=state.convert_terms * 12)
            m2 = RefactorMortgage.byMonthlyPayment(m1,state.convert_one_time)
            print(m2,m1)
            # m2 = RefactorMortgage.byInterest(m1,interest=state.interest_rate[1]/100)
            m1d = [ i[0] for x, i in enumerate(m1.monthly_payment_schedule())]
            m2d = [ i[0] for x, i in enumerate(m2.monthly_payment_schedule())]
            c1,c2,c3 = st.columns([1,1,1])
            monthly = float(m2.monthly_payment()-m1.monthly_payment())
            tot = float(m1.total_interest() - m2.total_interest())

            with c1:st.metric(label="Monthly Cost", value=float(m2.monthly_payment()),delta=monthly, delta_color="inverse")
            with c2:st.metric(label="Years Till Paid", value=int(float(m2.months)/12),delta=round((m2.months-m1.months)/12), delta_color="inverse")
            with c3:st.metric(label="Total Interest", value=float(m2.total_interest()),delta=-tot, delta_color="inverse")

            df = pd.DataFrame(columns=["A","B", "Years"])
            df.A = pd.Series(m1d)
            df.B = pd.Series(m2d)
            df.Years = df.index/12
            st.line_chart(df, x="Years")



if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
