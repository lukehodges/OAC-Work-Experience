import streamlit as st
from streamlit import session_state as state
from streamlit_echarts import st_echarts

from dashboard.apps.mortgage.mortgage import Mortgage, dollar, RefactorMortgage



def main():

    col1, col2 = st.columns([1, 1])

    with col1:
        inter = st.slider("Interest_Rate", min_value=0.0, max_value=10.0, step=0.1, value=2.0, key="interest_rate")
        debt = st.slider("Mortgage Debt", min_value=0.0, max_value=1_000_000.0, step=5000.0, value=100_000.0,
                         key="debt")
        terms = st.slider("Mortgage Terms", min_value=0.0, max_value=50.0, step=1.0, value=10.0, key="terms")
        cl1, cl2, cl3 = st.columns([1, 1, 1])


        one_off = st.number_input("One Time Payment", key="one_time", step=50)


    with col2:
        options = {
            "xAxis": {
                "type": "value"},
            "yAxis": {"type": "value"},
            "series": [

                # {"data":m2d, "type": "line"}
            ],
        }
        m1 = Mortgage(interest=state.interest_rate / 100, amount=dollar(state.debt),
                      months=state.terms * 12)
        m2 = RefactorMortgage.byPrinciple(m1, dollar(state.debt - state.one_time))
        print(m1)

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
        st_echarts(options=options)
        monthly = m1.monthly_payment()-m2.monthly_payment()
        tot = m1.total_interest() - m2.total_interest()
        print(monthly)
        print(tot)
        st.text(f"monthly saved :{monthly}. total saved: {tot}")




if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
