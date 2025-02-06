import streamlit as st
import requests
import json  # ✅ Ensure JSON formatting

def show_dashboard(api_predict_url):
    # Check if the user is logged in
    if 'username' not in st.session_state:
        st.error("You need to login first.")
        st.stop()

    st.title("🎓 Student Dashboard")
    st.success(f"Welcome {st.session_state['username']}! Let's predict your performance.")

    # 📌 Prediction Form
    st.header("📊 Predict Your Next GPA")

    # ✅ Lifestyle Factors
    study_hours = st.slider("📚 Study Hours Per Day", 1, 10, 3)
    extracurricular_hours = st.slider("🎭 Extracurricular Hours Per Day", 0, 10, 1)
    sleep_hours = st.slider("😴 Sleep Hours Per Day", 0, 12, 8)
    social_hours = st.slider("🗣️ Social Hours Per Day", 0, 10, 2)
    physical_activity_hours = st.slider("🏃 Physical Activity Hours Per Day", 0, 10, 1)

    # ✅ Stress level selection
    stress_level_category = st.selectbox("🧠 Stress Level", ["Low", "Moderate", "High"], index=1)
    stress_level_mapping = {"Low": 0, "Moderate": 1, "High": 2}
    stress_level = stress_level_mapping[stress_level_category]

    # ✅ Additional Performance Data
    study_hours_per_week = st.slider("📖 Study Hours Per Week", 0, 50, 30)
    attendance_rate = st.slider("📅 Attendance Rate (%)", 0, 100, 80)

    # ✅ Categorical Inputs
    gender = st.selectbox("👤 Gender", ["Male", "Female"])
    major = st.selectbox("📚 Major", ["Engineering", "Science", "Arts", "Business", "Education", "General"])
    part_time_job = st.selectbox("💼 Part-Time Job", ["Yes", "No"])
    extracurricular_activity = st.selectbox("🎾 Extracurricular Activities", ["Yes", "No"])

    if st.button("🎯 Predict GPA"):
        # ✅ Prepare the data to send to the API
        data = {
            "username": st.session_state['username'],
            "Study_Hours_Per_Day": study_hours,
            "Extracurricular_Hours_Per_Day": extracurricular_hours,
            "Sleep_Hours_Per_Day": sleep_hours,
            "Social_Hours_Per_Day": social_hours,
            "Physical_Activity_Hours_Per_Day": physical_activity_hours,
            "Stress_Level": stress_level,
            "StudyHoursPerWeek": study_hours_per_week,
            "AttendanceRate": attendance_rate,
            "Gender": gender,
            "Major": major,
            "PartTimeJob": part_time_job,
            "ExtraCurricularActivities": extracurricular_activity
        }

        try:
            # ✅ Convert to JSON format
            json_data = json.dumps(data)  # Convert dict to JSON string

            # ✅ Make the API request
            response = requests.post(api_predict_url, data=json_data, headers={'Content-Type': 'application/json'})
            response_data = response.json()

            # ✅ Handle response
            if response.status_code == 200:
                predicted_gpa = response_data.get("GPA")
                if predicted_gpa is not None:
                    st.success(f"🎉 Your Predicted GPA: **{round(predicted_gpa, 2)}**")
                else:
                    st.error("⚠️ Prediction failed. No GPA returned from API.")
            else:
                st.error(f"❌ Failed to get prediction: {response.status_code} - {response_data.get('error', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 API request failed: {e}")
        except json.JSONDecodeError as e:
            st.error(f"🚨 JSON Parse Error: {e}")
