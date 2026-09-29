import streamlit as st
import pandas as pd

# Import processed dataframe and cosine similarity values
from project_prep import df, similarity_matrix


# Page settings
st.set_page_config(
    page_title="Profile Recommendation System",
    page_icon="🤝",
    layout="wide"
)


# Recommendation function
def recommend_profiles(profile_name, top_n=5):

    # Find selected person's index
    profile_index = df[df["Name"] == profile_name].index[0]

    # Get cosine similarity scores
    scores = list(enumerate(similarity_matrix[profile_index]))

    # Sort from highest score to lowest score
    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Skip the selected person's own profile
    scores = scores[1:top_n + 1]

    recommendations = []

    for index, score in scores:

        profile = df.iloc[index].copy()

        # Convert decimal score into percentage
        profile["Compatibility Score"] = round(score * 100, 2)

        recommendations.append(profile)

    return pd.DataFrame(recommendations)


# Application title
st.title("🤝 NLP Profile Recommendation System")

st.write(
    """
    Select a profile to find the most compatible people based on
    their skills, education, experience and interests.
    """
)

st.divider()


# Profile selection
selected_profile = st.selectbox(
    "Select a profile:",
    df["Name"].unique()
)


# Number of recommendations
top_n = st.slider(
    "How many recommendations do you want?",
    min_value=1,
    max_value=10,
    value=5
)


# Display selected profile
st.subheader("Selected Profile")

selected_data = df[df["Name"] == selected_profile]

st.dataframe(
    selected_data,
    use_container_width=True,
    hide_index=True
)


# Recommendation button
if st.button("Recommend Profiles", type="primary"):

    result = recommend_profiles(
        selected_profile,
        top_n
    )

    st.success(
        f"Top {top_n} compatible profiles for {selected_profile}"
    )

    st.subheader("Recommended Profiles")

    # Hide combined text if it exists
    display_columns = [
        column for column in result.columns
        if column != "combined_text"
    ]

    st.dataframe(
        result[display_columns],
        use_container_width=True,
        hide_index=True
    )