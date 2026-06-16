import streamlit as st
from questions import questions
from traits import traits
from career_profiles import career_profiles

st.set_page_config(
    page_title="Career Recommendation System",
    page_icon="🎓"
)

# -----------------------------
# Session State Initialization
# -----------------------------

if "started" not in st.session_state:
    st.session_state.started = False

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "responses" not in st.session_state:
    st.session_state.responses = {}

if "show_profile" not in st.session_state:
    st.session_state.show_profile = False

# -----------------------------
# Flatten Questions
# -----------------------------

all_questions = []

for section in questions:
    for q_no in questions[section]:

        all_questions.append(
            {
                "q_no": q_no,
                "section": section,
                "question":
                questions[section][q_no]["question"]
            }
        )

total_questions = len(all_questions)


####   WELCOME SCREEN   ####
if not st.session_state.started:

    st.title("🎓 Career Recommendation System")

    st.markdown(
        """
        Welcome!

        This assessment contains **25 questions**
        designed to evaluate your:

        - Interests
        - Skills
        - Personality Traits
        - Career Goals

        There are no right or wrong answers.

        Answer honestly.

        The results may help you identify
        career paths that align with your profile.
        """
    )

    if st.button("Start Assessment"):

        st.session_state.started = True
        st.rerun()


####   QUESTIONNAIRE   ####
else:

        current_index = st.session_state.question_index

        if current_index < total_questions:

            current_question = (
                all_questions[current_index]
            )

            st.progress(
                (current_index + 1)
                / total_questions
            )

            st.subheader(
                f"Question "
                f"{current_index + 1}"
                f" of {total_questions}"
            )

            st.caption(
                current_question["section"]
            )

            response = st.radio(
                current_question["question"],
                [1, 2, 3, 4, 5],
                horizontal=True,
                key=f"q_{current_index}"
            )

            if st.button("Next"):

                st.session_state.responses[
                    current_question["q_no"]
                ] = response

                st.session_state.question_index += 1

                st.rerun()

        else:

            st.success(
                "🎉 Assessment Completed Successfully!"
            )

            st.write(
                "All 25 questions have been answered."
            )

            if st.button(
                "Generate My Profile"
            ):

                st.session_state.show_profile = True

                st.rerun()


####    Profile + Recommendations  ####

if st.session_state.show_profile:

    st.title("📊 Your Profile")

    # -----------------------------
    # Initialize Scores
    # -----------------------------

    profile_scores = {}

    for category in traits:
        for trait in traits[category]:
            profile_scores[trait] = 0

    # -----------------------------
    # Calculate Scores
    # -----------------------------

    for section in questions:

        for q_no in questions[section]:

            if q_no in st.session_state.responses:

                score = (
                    st.session_state.responses[q_no]
                )

                for trait in (
                    questions[section][q_no]["traits"]
                ):
                    profile_scores[
                        trait
                    ] += score

    # -----------------------------
    # Question Counts
    # -----------------------------

    question_counts = {}

    for category in traits:
        for trait in traits[category]:
            question_counts[trait] = 0

    for section in questions:
        for q_no in questions[section]:
            for trait in (
                questions[section][q_no]["traits"]
            ):
                question_counts[trait] += 1

    # -----------------------------
    # Percentages
    # -----------------------------

    profile_percentages = {}

    for trait in profile_scores:

        max_score = (
            question_counts[trait] * 5
        )

        profile_percentages[trait] = (
            profile_scores[trait]
            / max_score
        ) * 100

    # -----------------------------
    # Levels
    # -----------------------------

    profile_levels = {}

    for trait in profile_percentages:

        if profile_percentages[trait] < 40:

            profile_levels[trait] = "Low"

        elif profile_percentages[trait] < 70:

            profile_levels[trait] = "Medium"

        else:

            profile_levels[trait] = "High"

    st.session_state.profile_levels = (
        profile_levels
    )

    # -----------------------------
    # Display Profile
    # -----------------------------

    for category in traits:

        st.subheader(category)

        for trait in traits[category]:

            st.write(
                f"**{trait}:** "
                 f"{profile_levels[trait]}"
                    )

    st.markdown("---")

    st.subheader(
        "🎯 Career Path Selection"
    )

    career_choice = st.radio(
    "What are you primarily considering?",
    [
        "Jobs",
        "Higher Studies",
        "Work-Integrated Learning Programme (WILP)"
    ],
    key="career_choice"
)

    if st.button(
                "Generate Recommendations"
            ):

                career_weights = {
                    "Major Essential": 4,
                    "Essential": 3,
                    "Helpful": 2,
                    "Neutral": 1
                }

                level_weights = {
                    "High": 3,
                    "Medium": 2,
                    "Low": 1
                }

                job_profiles = [
                    "Corporate & Private Sector Jobs",
                    "Startup",
                    "Public Sector / Government Jobs",
                    "Defence Services",
                    "Technical Government Cadres",
                    "Civil Services (UPSC / State PSC)"
                ]

                higher_study_profiles = [
                    "M.Tech",
                    "MS",
                    "PhD",
                    "MBA / PGDM",
                    "Specialized Techno-Management",
                    "M.Des",
                    "LLB / LLM",
                    "Data Science & AI Advanced Diploma"
                ]

                def calculate_scores(profile_list):

                  recommendation_scores = {}

                  for career in profile_list:

                      total_score = 0

                      for trait in profile_levels:

                          user_weight = level_weights[
                              profile_levels[trait]
                          ]

                          for category in career_profiles[career]:

                              if trait in career_profiles[career][category]:

                                 career_weight = career_weights[
                                     category
                                 ]

                                 total_score += (
                                     user_weight * career_weight
                                 )

                      recommendation_scores[career] = total_score

                  return sorted(
                      recommendation_scores.items(),
                      key=lambda x: x[1],
                      reverse=True
            )

        # JOBS

                if career_choice == "Jobs":

                    results = calculate_scores(
                        job_profiles
                   )

                    st.subheader(
                        "💼 Top Job Recommendations"
                    )

                    for rank, (career, score) in enumerate(
                        results[:3],
                        start=1
                    ):

                        st.write(
                            f"{rank}. {career}"
                        )

        # HIGHER STUDIES

                elif career_choice == "Higher Studies":

                    results = calculate_scores(  
                        higher_study_profiles
                    )

                    st.subheader(
                        "🎓 Top Higher Study Recommendations"
                    )

                    for rank, (career, score) in enumerate(
                        results[:3],
                        start=1
                   ):

                        st.write(
                            f"{rank}. {career}"
                )

        # WILP

                else:

                    jobs = calculate_scores(
                        job_profiles
            )

                    studies = calculate_scores(
                        higher_study_profiles
                    )

                    st.subheader(
                        "💼 Top Job Recommendations"
            )

                    for rank, (career, score) in enumerate(
                        jobs[:3],
                        start=1
            ):

                        st.write(
                            f"{rank}. {career}"
                )

                    st.subheader(
                        "🎓 Top Higher Study Recommendations"
            )

                    for rank, (career, score) in enumerate(
                        studies[:3],
                        start=1
            ):

                        st.write(
                            f"{rank}. {career}"
                )

                    st.info(
                         "A Work-Integrated Learning Programme can be a suitable option if you wish to gain professional experience while continuing your education. Based on your profile, the job and study paths listed above may be worth exploring together."
            )

                st.markdown("---")

                st.caption(
                     "Disclaimer: This recommendation system is intended to provide guidance based on your responses and profile traits. No automated system can fully determine your interests, abilities, goals, or future career satisfaction. Use these recommendations as a starting point for exploration. The final decision should always be based on your own interests, research, and judgment."
        )