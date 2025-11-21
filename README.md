# 🍽️ Swiggy Restaurant Recommendation System  
A Machine Learning–powered restaurant recommendation system built using **Python**, **Scikit-learn**, and **Streamlit**.  
This project analyzes restaurant data, processes categorical & numerical features, applies clustering (KMeans), and recommends similar restaurants based on user preferences.

---

## 🚀 Features
- 🔍 **Personalized restaurant recommendations**
- 🍛 Filter by **City**, **Cuisine**, **Rating**, & **Price Range**
- 🤖 **KMeans Clustering** to find similar restaurants
- 🧹 Full pipeline: Cleaning → Encoding → Scaling → Clustering
- 🌐 Interactive **Streamlit** frontend
- 💾 Automatic Pickle export for encoded dataset

---

## 📁 Project Structure


---

## 🧠 Workflow Overview

### **1️⃣ Data Cleaning**
- Removed duplicates  
- Handled missing values  
- Standardized text fields  

### **2️⃣ Preprocessing**
- One-Hot Encoding:  
  - `cuisine`  
  - `city`  
- Numerical features:  
  - `rating`, `rating_count`, `cost`  
- StandardScaler used for normalization  

### **3️⃣ Clustering (KMeans)**
- Model: `KMeans(n_clusters=4, random_state=42, n_init=10)`  
- Each restaurant assigned to a cluster  
- This cluster is used to recommend similar restaurants  

### **4️⃣ Recommendation Logic**
Based on user inputs:
- City  
- Cuisine  
- Minimum Rating  
- Price Range  

The algorithm:
1. Filters restaurants  
2. Picks a random restaurant from the filtered list  
3. Finds similar restaurants from the **same cluster**  
4. Displays the top recommendations  

---

## 🖥️ How to Run Locally

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/swiggy-recommendation.git
cd swiggy-recommendation

2️⃣ Install Requirements

streamlit
pandas
scikit-learn
numpy
THen install
pip install -r requirements.txt
3️⃣ Run the App
streamlit run app.py

📊 Dataset Columns

id

name

city

rating

rating_count

cost

cuisine

address, menu, link

Cleaned dataset → cleaned_data.csv

🔧 Technologies Used
Category	Tools
Frontend	Streamlit
ML	Scikit-learn (KMeans, OneHotEncoder, StandardScaler)
Data Processing	Pandas
Language	Python

Future Improvements

Add Cosine-Similarity based recommendations

Show restaurant locations on an interactive map

Use embedding models (Word2Vec/BERT) for cuisine/menu similarity

Deploy on Streamlit Cloud / AWS / Render

👨‍💻 Author
Jayaganesh Sekar

## 📄 License
MIT License

git clone https://github.com/your-username/swiggy-recommendation.git
cd swiggy-recommendation
