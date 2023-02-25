import streamlit as st
import scipy.stats
import math

st.set_page_config(page_title = "A/B Hat", page_icon=":tophat:", layout = 'wide')
# emojis https://www.webfx.com/tools/emoji-cheat-sheet/

# --- Header Section ---
with st.container(): 
    st.title(":tophat: A/B Hat: Easy sample size calculations for your next A/B test") 

# --- Sample size calculation ---
def sample_size(baseline, mde, mde_type, sig_level, power, two_tailed, binomial):

    if binomial:
        variance = (baseline/100.) * (1 - (baseline/100.))
    else:
        variance = baseline/100. 
    
    if two_tailed:
        sig_level = (sig_level/100.) / 2
    else:
        sig_level = sig_level/100.

    if mde_type == 'Absolute':
        mde = mde/100.
    else:
        mde = ((mde/100.) * baseline)/100.
        
    Zp = scipy.stats.norm.ppf(1 - sig_level)
    Zpower = scipy.stats.norm.ppf(power/100.)
    n = (2 * variance * (Zp + Zpower)**2) / (mde**2)
    #return math.ceil(n)
    #return round(n)
    return (f"{round(n):,d}")

# --- Container and columns ---
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)

    with left_column:
        st.header("Describe your experiment")
       # st.write("Let's learn more about what you want to test")
        metric = st.selectbox(
            "What metric are you testing?",
            ("conversion rate", "some average per user or session"), help="What is the metric that your experiment is testing?")
        if metric == 'conversion rate':
            binomial = True 
        else:
            binomial = False
        mde = st.slider(
            "What is the minimum detectable effect (MDE) you are interested in?",
            value = 10, format="%d%%", help="The absolute % minimum effect size you want to be able to detect")
        if metric != "conversion rate":
            baseline = st.number_input('What is the baseline variance?',
                                       value = 50, help = "The variance of your control group")

            mde_type = 'Absolute'
        else:
            baseline = st.slider(
                "What is the baseline conversion rate? (%)",
                value = 50, format="%d%%", help="The conversion rate of your control group")  
               
            mde_type = st.radio(
                    "Is the MDE absolute or relative to the baseline?",
                    ("Absolute", "Relative"))

        power = st.slider(
            "Define the statistical power (1−β)",
            value = 80, format="%d%%", help = "Percent of the time the MDE will be detected, assuming it exists"
        )

        sig_level = st.slider(
            "Define the significance level (α)",
            value = 5, max_value=10, format="%d%%", help= "Percent of the time a difference will be detected, assuming one does not exist"
        )    

        two_tailed = st.radio(
            "Are you testing a two-sided hypothesis?",
            (True, False)
        )

    with right_column:
        st.header("The minimum sample size that you need is")

        st.markdown(
                            """
                        <style>
                        [data-testid="stMetricValue"] {
                            font-size: 100px;
                        }

                        /*center metric label*/
                        [data-testid="stMetricLabel"] > div:nth-child(1) {
                            justify-content: center;
                        }

                        /*center metric value*/
                        [data-testid="stMetricValue"] > div:nth-child(1) {
                            justify-content: center;
                        }
                        </style>


                        """,
    unsafe_allow_html=True
        
        )

        st.metric(label='per treatment', value=sample_size(baseline, mde, mde_type, sig_level, power, two_tailed, binomial))
        




