import streamlit as st
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.cluster import KMeans
import random
import pickle

# ----------------------------
# STEP 1: Load and preprocess data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(r"D:\Guvi project 3\cleaned_data.csv")

    # OneHotEncode categorical columns
    encoder = OneHotEncoder(sparse_output=False)
    cat_features = encoder.fit_transform(df[['cuisine', 'city']])
    cat_df = pd.DataFrame(cat_features, columns=encoder.get_feature_names_out(['cuisine', 'city']))

    # Combine numerical + categorical
    num_df = df[['rating', 'rating_count', 'cost']].reset_index(drop=True)
    final_df = pd.concat([num_df, cat_df], axis=1)

    # Standardize numerical features
    scaler = StandardScaler()
    final_df.loc[:, ['rating', 'rating_count', 'cost']] = scaler.fit_transform(final_df[['rating', 'rating_count', 'cost']])

    return df, final_df

df, final_df = load_data()

# ✅ Export dataset as pickle file
pickle_path = r"D:\Guvi project 3\final_encoded.pkl"
with open(pickle_path, 'wb') as file:
    pickle.dump(final_df, file)

# ----------------------------
# STEP 2: Train KMeans
# ----------------------------
@st.cache_resource
def train_kmeans(data, n_clusters=4):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(data.copy())
    return kmeans, df

kmeans, df = train_kmeans(final_df, n_clusters=4)

# ----------------------------
# STEP 3: Recommendation function
# ----------------------------
def recommend_restaurants(df, city, min_rating, price_min, price_max,sel_cuisine, n_recommendations=5):
    # Filter based on user preferences
    filtered = df[
        (df['city'].str.lower() == city.lower()) &
        (df['rating'] >= min_rating) &
        (df['cost'].between(price_min, price_max)) &
        (df['cuisine'].str.lower()==sel_cuisine.lower())
    ]

    if filtered.empty:
        return None

    # Select a random restaurant from filtered list to find similar ones
    selected_restaurant = filtered.sample(1, random_state=42).iloc[0]
    cluster_label = selected_restaurant['cluster']

    # Find similar restaurants in the same cluster
    cluster_members = df[(df['cluster'] == cluster_label) & (df['name'] != selected_restaurant['name'])]
    if cluster_members.empty:
        return None

    recommendations = cluster_members.sample(
        n=min(n_recommendations, len(cluster_members)), random_state=42
    )
    
    return selected_restaurant['name'], recommendations[['name', 'cuisine', 'city', 'rating', 'cost']]

# ----------------------------
# STEP 4: Streamlit UI
# ----------------------------
st.title("🍽️ Swiggy Restaurant Recommendation System")
st.write("Get personalized restaurant recommendations based on your preferences and similar clusters!")

# Sidebar filters
st.sidebar.header("🔍 Filter your preferences")

selected_city = st.sidebar.selectbox("Select City:", sorted(df['city'].unique()))
price_range = st.sidebar.slider("Select Price Range (₹):", 0, int(df['cost'].max()), (200, 800))
min_rating = st.sidebar.slider("Minimum Rating:", 0.0, 5.0, 3.5, 0.1)
selected_cuisine=st.sidebar.selectbox("Select Cuisine:", sorted(df['cuisine'].unique()))

# Main recommendation button
if st.sidebar.button("Find Restaurants"):
    result = recommend_restaurants(df, selected_city, min_rating, price_range[0], price_range[1],selected_cuisine)

    if result is None:
        st.warning("No restaurants found matching your preferences.")
    else:
        selected_restaurant, recs = result
        st.success(f"✨ Based on your preferences, here are restaurants similar to **{selected_restaurant}**:")
        st.dataframe(recs)

# ----------------------------
# STEP 5: Optional Cluster Summary
# ----------------------------
# with st.expander("📊 View Cluster Summary"):
#     cluster_summary = df.groupby('cluster')[['rating', 'cost']].mean().reset_index()
#     st.dataframe(cluster_summary)
