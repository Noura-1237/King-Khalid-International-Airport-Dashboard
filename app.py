import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# --- 1. إعدادات الصفحة الأساسية للمتصفح ---
st.set_page_config(
    page_title="KKIA Flights Dashboard",
    page_icon="✈️",
    layout="wide"
)

# --- 2. تصفيف مخصص بالـ CSS للعنوان الرئيسي والعناوين الجانبية ---
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1E3A8A;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E5E7EB;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. تحميل البيانات ومعالجتها التلقائية ---
@st.cache_data
def load_data():
    # تأكدي أن ملف الـ CSV موجود في نفس مجلد ملف الكود app.py
    df = pd.read_csv('final_cleaned_flights_RUH.csv')
    df['scheduled_time_local'] = pd.to_datetime(df['scheduled_time_local'])
    df['hour'] = df['scheduled_time_local'].dt.hour
    return df

df = load_data()
sns.set_theme(style="whitegrid")

# --- 4. تصميم الشريط الجانبي (Sidebar الفلاتر) ---
st.sidebar.header("🔍 Filter Options")

# فلتر اختيار الصالة
all_terminals = sorted([str(t) for t in df['terminal'].unique() if str(t) not in ['Unknown', 'nan']])
selected_terminals = st.sidebar.multiselect(
    "Select Terminal(s):",
    options=all_terminals,
    default=all_terminals
)

# فلتر نوع الرحلة (وصول / مغادرة)
all_flight_types = df['flight_type'].unique()
selected_flight_types = st.sidebar.multiselect(
    "Select Flight Type(s):",
    options=all_flight_types,
    default=all_flight_types
)

# تحويل عمود الصالة لنصوص مؤقتاً لضمان مطابقة الفلتر بدقة
df_filtered_prep = df.copy()
df_filtered_prep['terminal'] = df_filtered_prep['terminal'].astype(str)

# تطبيق الفلاتر التفاعلية
filtered_df = df_filtered_prep[
    (df_filtered_prep['terminal'].isin(selected_terminals)) & 
    (df_filtered_prep['flight_type'].isin(selected_flight_types))
]

# حسابات المؤشرات (KPIs) بناءً على الفلتر الحالي
canceled_flights_df = filtered_df[filtered_df['status'] == 'Canceled']
canceled_count = len(canceled_flights_df)
total_flights = len(filtered_df)
canceled_rate = (canceled_count / total_flights * 100) if total_flights > 0 else 0.0

# --- 5. الواجهة الرئيسية والعنوان ---
st.markdown("<div class='main-title'>✈️ King Khalid International Airport (KKIA) Descriptive Analytics Dashboard</div>", unsafe_allow_html=True)

# --- 6. قسم المؤشرات العلوية (KPIs) ---
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.metric(label="📊 Total Filtered Flights", value=f"{total_flights:,}")

with kpi_col2:
    unique_airlines = filtered_df['airline_name'].nunique()
    st.metric(label="🏢 Active Airlines", value=unique_airlines)

with kpi_col3:
    st.metric(
        label="🚨 Canceled Flights", 
        value=canceled_count, 
        delta=f"{canceled_rate:.1f}% Cancel Rate", 
        delta_color="inverse"
    )

st.markdown("<br/>", unsafe_allow_html=True)

# --- 7. قسم الرسوم البيانية المتجاورة (1 و 2) ---
plot_col1, plot_col2 = st.columns(2)

with plot_col1:
    st.markdown("<div class='section-header'>🏢 1. Flight Distribution by Terminal</div>", unsafe_allow_html=True)
    temp_df = filtered_df[~filtered_df['terminal'].isin(['Unknown', 'nan'])].copy()
    terminal_counts = temp_df['terminal'].value_counts().sort_index()
    
    if not terminal_counts.empty:
        fig, ax = plt.subplots(figsize=(6, 3.5))
        sns.barplot(x=terminal_counts.index, y=terminal_counts.values, palette='Blues_r', ax=ax)
        ax.set_ylabel("Number of Flights", fontsize=9)
        ax.set_xlabel("Terminal Number", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        st.pyplot(fig)
    else:
        st.warning("No terminal data found for the current filters.")
        
    st.info("**💡 Insight:** Shows workload imbalances among terminals to help management optimize staffing and facility resource allocation.")

with plot_col2:
    st.markdown("<div class='section-header'>📌 2. Top 5 Most Used Aircraft Models</div>", unsafe_allow_html=True)
    top_aircraft = filtered_df[filtered_df['aircraft_model'] != 'Unknown']['aircraft_model'].value_counts().head(5)
    
    if not top_aircraft.empty:
        fig, ax = plt.subplots(figsize=(6, 3.5))
        sns.barplot(x=top_aircraft.values, y=top_aircraft.index, palette='crest', ax=ax)
        ax.set_xlabel("Number of Flights", fontsize=9)
        ax.set_ylabel("", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.grid(axis='x', linestyle='--', alpha=0.3)
        st.pyplot(fig)
    else:
        st.warning("No data available for the current filter selection.")
        
    st.info("**💡 Insight:** Identifies the dominant aircraft models, helping ground operations plan gate sizing and parking effectively.")

# --- 8. قسم الرسمة الثالثة (عرض كامل الصفحة) ---
st.markdown("<div class='section-header'>⏰ 3. Comparison of Peak Hours: Arrivals vs Departures</div>", unsafe_allow_html=True)
if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(12, 3.5))
    sns.countplot(data=filtered_df, x='hour', hue='flight_type', palette='Set2', ax=ax)
    ax.set_xlabel("Hour of the Day (00:00 to 23:00)", fontsize=9)
    ax.set_ylabel("Number of Flights", fontsize=9)
    ax.tick_params(labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.legend(title='Flight Type', fontsize=8, title_fontsize=9)
    plt.grid(axis='y', linestyle='--', alpha=0.2)
    st.pyplot(fig)
else:
    st.warning("No data available for the current filter selection.")

st.info("**💡 Insight:** Maps out peak operational intervals to schedule customs, security, and baggage handling shifts during busy times.")

# --- 9. قسم الرسوم البيانية المتجاورة (4 و 5) ---
plot_col3, plot_col4 = st.columns(2)

with plot_col3:
    st.markdown("<div class='section-header'>📊 4. Histogram of Flight Scheduled Hours</div>", unsafe_allow_html=True)
    if not filtered_df.empty:
        fig, ax = plt.subplots(figsize=(6, 3.5))
        sns.histplot(filtered_df['hour'], bins=24, kde=True, color='purple', ax=ax)
        ax.set_xlabel("Hour of the Day", fontsize=9)
        ax.set_ylabel("Frequency", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        st.pyplot(fig)
    else:
        st.warning("No data available.")
        
    st.info("**💡 Insight:** Provides a continuous view of overall daily traffic flow, highlighting smooth transitions between quiet and rush hours.")

with plot_col4:
    st.markdown("<div class='section-header'>📦 5. Boxplot of Flight Hours by Terminal</div>", unsafe_allow_html=True)
    # تصفية الصالات الشهيرة من 1 إلى 5 فقط للرسمة الصندوقية
    popular_terminals = filtered_df[filtered_df['terminal'].isin(['1', '2', '3', '4', '5'])]
    
    if not popular_terminals.empty:
        fig, ax = plt.subplots(figsize=(6, 3.5))
        sns.boxplot(data=popular_terminals, x='terminal', y='hour', palette='Set3', ax=ax)
        ax.set_xlabel("Terminal", fontsize=9)
        ax.set_ylabel("Hour of the Day", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        st.pyplot(fig)
    else:
        st.warning("No data found for Terminals 1-5.")
        
    st.info("**💡 Insight:** Compares the density spread of flights per terminal; a tighter box indicates highly condensed flight arrivals or departures.")

# --- 10. قسم الشركات الأكثر إلغاءً والجدول السفلي ---
st.markdown("<div class='section-header'>🚨 6. Top 5 Airlines with Flight Cancellations</div>", unsafe_allow_html=True)
top_canceled_airlines = canceled_flights_df['airline_name'].value_counts().head(5)

if not top_canceled_airlines.empty:
    # تحويل البيانات إلى DataFrame لعرضها بشكل جدول تفاعلي منظم بدلاً من نص مطبوع
    canceled_df_display = top_canceled_airlines.reset_index()
    canceled_df_display.columns = ['Airline Name', 'Canceled Flights Count']
    st.dataframe(canceled_df_display, use_container_width=True)
else:
    st.success("Great! No canceled flights found for the current filters.")
st.info("**💡 Insight:** Acts as a KPI to monitor and evaluate airline reliability, providing data evidence to hold specific operators accountable.")

# --- 11. مستكشف ومحمل البيانات المفلترة ---
st.markdown("<div class='section-header'>📋 Filtered Data Explorer & Download</div>", unsafe_allow_html=True)
action_col1, action_col2 = st.columns([3, 1])
with action_col2:
    csv_data = filtered_df.head(100).to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV Sample",
        data=csv_data,
        file_name="filtered_flights_sample.csv",
        mime="text/csv",
        use_container_width=True
    )
st.dataframe(filtered_df.head(100), use_container_width=True)