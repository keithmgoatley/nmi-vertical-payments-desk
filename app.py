import pandas as pd
import plotly.express as px, plotly.graph_objects as go
import streamlit as st
import data as D

st.set_page_config(page_title="Vertical Payments GTM Desk", layout="wide")

@st.cache_data
def load():
    return D.build_vertical_opportunity(), D.build_competitive_grid(), \
           D.build_launch_tracker(), D.build_channel_health()

opp, comp, launch, ch = load()

st.title("Vertical Payments GTM Desk")
st.write("Product marketing tool for a payment gateway and device business: sizes vertical "
         "opportunities, tracks competitive positioning, monitors launch readiness, and scores "
         "messaging on a solution-vs-feature scale. Data is synthetic.")

tabs = st.tabs(["Vertical opportunity", "Competitive positioning", "Launch tracker",
                "Solution-vs-feature scorer", "Channel enablement"])

with tabs[0]:
    st.subheader("Where the vertical opportunity actually is")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total TAM", f"£{opp.tam_gbp_bn.sum():.1f}bn")
    c2.metric("Weighted pipeline", f"£{opp.pipeline_gbp.sum()/1e6:.1f}m")
    c3.metric("Avg win rate", f"{opp.win_rate.mean():.1%}")
    fig = px.scatter(opp, x="tam_gbp_bn", y="cagr", size="pipeline_gbp",
                     color="priority_score", hover_data=["vertical", "dynamic", "win_rate"])
    fig.update_layout(height=400, xaxis_title="TAM (£bn)", yaxis_title="CAGR",
                      yaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(opp.style.format({"tam_gbp_bn": "£{:.1f}bn", "cagr": "{:.1%}",
        "win_rate": "{:.1%}", "pipeline_gbp": "£{:,.0f}", "nmi_share": "{:.1%}"}),
        hide_index=True, use_container_width=True)

with tabs[1]:
    st.subheader("Competitive positioning grid")
    vs = st.multiselect("Compare NMI against",
                        [c for c in comp.vendor.unique() if c != "NMI"],
                        default=["Stripe Terminal", "Adyen", "Verifone Cloud"])
    plot_df = comp[comp.vendor.isin(["NMI"] + vs)]
    fig = go.Figure()
    for v in plot_df.vendor.unique():
        d = plot_df[plot_df.vendor == v]
        fig.add_trace(go.Scatterpolar(r=d.score, theta=d.axis, fill="toself", name=v))
    fig.update_layout(height=480, polar=dict(radialaxis=dict(range=[0, 5])))
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.subheader("Launch readiness by initiative")
    st.dataframe(launch, hide_index=True, use_container_width=True)

with tabs[3]:
    st.subheader("Solution-vs-feature message scorer")
    st.write("Paste marketing copy. The tool counts feature/spec words against solution/outcome "
             "words and gives a verdict. Below 65% solution language means rewrite.")
    sample = ("Our unattended kiosk terminal supports EMV, contactless, and API integration "
              "over USB, with 500ms latency and full ISO certification.")
    text = st.text_area("Message copy", value=sample, height=140)
    if text.strip():
        r = D.score_message(text)
        c1, c2, c3 = st.columns(3)
        c1.metric("Feature/spec words", r["feature"])
        c2.metric("Solution/outcome words", r["solution"])
        c3.metric("Solution ratio", f"{r['ratio']:.0%}")
        st.info(f"**Verdict:** {r['verdict']}")
        with st.expander("Solution-forward rewrite example"):
            rewrite = ("For unattended operators: our kiosk solution turns downtime into "
                       "revenue - faster checkout, higher acceptance, and reliable uptime "
                       "across sites, so customers keep buying and operators keep growing.")
            st.write(rewrite)
            st.metric("Rewrite ratio", f"{D.score_message(rewrite)['ratio']:.0%}")

with tabs[4]:
    st.subheader("Channel enablement coverage")
    pivot = ch.pivot_table(index="channel", columns="vertical", values="adoption", aggfunc="mean")
    fig = px.imshow(pivot, aspect="auto", color_continuous_scale="RdYlGn")
    fig.update_layout(height=340)
    st.plotly_chart(fig, use_container_width=True)
    gaps = ch[ch.enablement == "Gap"][["channel", "vertical", "pipeline", "adoption"]]
    if len(gaps):
        st.markdown("**Enablement gaps to close**")
        st.dataframe(gaps.style.format({"pipeline": "£{:,.0f}", "adoption": "{:.1%}"}),
                     hide_index=True, use_container_width=True)

st.caption("Built by Keith Goatley - synthetic data.")
