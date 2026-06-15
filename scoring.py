# Import questionnaire data and trait categories from separate files
from questions import questions
from traits import traits
from career_profiles import career_profiles

# Dictionary to store the user's score for each profile trait
profile_scores = {}

# Initialize all profile scores to 0
for category in traits:
    for trait in traits[category]:
        profile_scores[trait] = 0

# Loop through each section of the questionnaire
for section in questions:

    # Display the section name
    print(f"\n--- {section} ---\n")

    # Loop through each question in the current section
    for q_no in questions[section]:

        # Display question number and question text
        print(f"Question {q_no}")
        print(questions[section][q_no]["question"])

        # Take user response on a scale of 1 to 5
        score = int(input(
            "Enter your response from 1 to 5 "
            "(1=Strongly Disagree, 2=Disagree, "
            "3=Neutral, 4=Agree, 5=Strongly Agree): "
        ))

        # Add the selected score to all traits mapped to the question
        for trait in questions[section][q_no]["traits"]:
            profile_scores[trait] += score


# Count how many questions contribute to each trait
question_counts = {}


# Initialize counts to 0
for category in traits:
    for trait in traits[category]:
        question_counts[trait] = 0

# Count occurrences
for section in questions:
    for q_no in questions[section]:
        for trait in questions[section][q_no]["traits"]:
            question_counts[trait] += 1


# Calculate maximum possible scores
max_scores = {}

for trait in question_counts:
    max_scores[trait] = question_counts[trait] * 5


# Calculate percentage scores for each trait
profile_percentages = {}

for trait in max_scores:
    profile_percentages[trait] = (
        profile_scores[trait] / max_scores[trait]
    ) * 100

#Classify the level of each trait based on the percentage score
profile_levels = {}
for trait in profile_percentages:
    if profile_percentages[trait] < 40:
     profile_levels[trait] = "Low"    
    elif profile_percentages[trait] < 70:
     profile_levels[trait] = "Medium"  
    else:
     profile_levels[trait] = "High"
    
# Display profile levels
print("\n========== YOUR PROFILE ==========\n")

for category in traits:

    print(f"{category}:")

    for trait in traits[category]:
        print(
            f"  {trait}: "
            f"{profile_levels[trait]}"
        )

    print()


# Ask user what they are primarily considering

print("\nWhat are you primarily considering?\n")

print("1. Jobs")
print("2. Higher Studies")
print("3. Work-Integrated Learning Programme (WILP)")

choice = input("\nEnter your choice (1/2/3): ")

# Create profile groups

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

# Career recommendation scoring based on user profile levels

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

# --------------------------------------------------
# JOBS
# --------------------------------------------------

if choice == "1":

    recommendation_scores = {}

    for career in job_profiles:

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

    sorted_recommendations = sorted(
        recommendation_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    print("\n========== TOP JOB RECOMMENDATIONS ==========\n")

    for rank, (career, score) in enumerate(
        sorted_recommendations[:3],
        start=1
    ):
        print(f"{rank}. {career}")

# --------------------------------------------------
# HIGHER STUDIES
# --------------------------------------------------

elif choice == "2":

    recommendation_scores = {}

    for career in higher_study_profiles:

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

    sorted_recommendations = sorted(
        recommendation_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    print("\n========== TOP HIGHER STUDY RECOMMENDATIONS ==========\n")

    for rank, (career, score) in enumerate(
        sorted_recommendations[:3],
        start=1
    ):
        print(f"{rank}. {career}")

# --------------------------------------------------
# WILP
# --------------------------------------------------

elif choice == "3":

    job_scores = {}

    for career in job_profiles:

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

        job_scores[career] = total_score

    study_scores = {}

    for career in higher_study_profiles:

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

        study_scores[career] = total_score

    sorted_jobs = sorted(
        job_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    sorted_studies = sorted(
        study_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    print("\n========== TOP JOB RECOMMENDATIONS ==========\n")

    for rank, (career, score) in enumerate(
        sorted_jobs[:3],
        start=1
    ):
        print(f"{rank}. {career}")

    print("\n========== TOP HIGHER STUDY RECOMMENDATIONS ==========\n")

    for rank, (career, score) in enumerate(
        sorted_studies[:3],
        start=1
    ):
        print(f"{rank}. {career}")

    print(
        "\nWILP Guidance:\n"
        "A Work-Integrated Learning Programme can be a suitable option if you wish to gain professional experience while continuing your education. Based on your profile, the job and study paths listed above may be worth exploring together."
    )

else:

    print("Invalid Choice")

#Disclaimer
print(
    "\nDisclaimer:\n"
    "This recommendation system is intended to provide guidance based on your responses and profile traits. No automated system can fully determine your interests, abilities, goals, or future career satisfaction. Use these recommendations as a starting point for exploration. The final decision should always be based on your own interests, research, and judgment."
)