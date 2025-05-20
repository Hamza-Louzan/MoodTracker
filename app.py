import streamlit as st
import pandas as pd
from datetime import datetime, date
import matplotlib.pyplot as plt
import gsheet_script

def main():
    st.set_page_config(page_title="Mood of the Queue", layout="wide")
    st.title("📊 Mood of the Queue Logger")
    st.markdown(f"Logging to: **{gsheet_script.GOOGLE_SHEET_NAME}** (Tab: **{gsheet_script.SHEET_TAB_NAME}**)")

    gspread_client = gsheet_script.authenticate_gsheet()

    # Step 1: Log a New Mood
    st.header("📝 Log a New Mood")

    col1, col2 = st.columns([1, 2])

    with col1:
        selected_mood_display = st.selectbox(
            "Select Mood:",
            options=list(gsheet_script.MOOD_OPTIONS.keys()),
            key="mood_select"
        )
        actual_mood_value = gsheet_script.MOOD_OPTIONS[selected_mood_display]

    with col2:
        note = st.text_input("Optional Note:", key="note_input")

    if st.button("Submit Mood", key="submit_button"):
        if selected_mood_display:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = [timestamp, actual_mood_value, note]
            
            if gsheet_script.append_to_sheet(gspread_client, log_entry):
                st.success(f"Mood '{actual_mood_value}' logged!")
                st.balloons()
        else:
            st.warning("Please select a mood.")

    st.markdown("---")

    #Step 2: Visualize the Mood 
    st.header("📈 Today's Mood Overview")

    df = gsheet_script.load_data_from_sheet(gspread_client)

    if not df.empty:
        today_str = date.today().strftime("%Y-%m-%d")
        
        # Verify that 'Timestamp' is datetime
        if 'Timestamp' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['Timestamp']):
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        
        df_today = df.dropna(subset=['Timestamp']).copy()
        df_today = df_today[df_today['Timestamp'].dt.strftime("%Y-%m-%d") == today_str]

        if not df_today.empty:
            mood_counts = df_today['Mood'].value_counts()
            if not mood_counts.empty:
                fig, ax = plt.subplots()
                mood_counts.plot(kind='bar', ax=ax)
                ax.set_title(f"Mood Counts for Today ({today_str})")
                ax.set_xlabel("Mood")
                ax.set_ylabel("Count")
                ax.tick_params(axis='x', rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.info("No moods logged yet for today with valid timestamps.")
        else:
            st.info("No moods logged yet for today.")
    else:
        st.info("No mood data found in the sheet.")

if __name__ == "__main__":
    main()