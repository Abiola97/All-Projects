
# 🤖 From Friction to Flows: NLP-Based Feedback Review System for Optimizing Product Performance at Any.do

A Natural Language Processing (NLP) project applying **collective intelligence principles** to analyze 16,092 Google Play reviews of the productivity app **Any.do**. The goal was to uncover hidden friction points, prioritize fixes, and provide actionable insights for product improvement.

---

## 📊 Project Workflow

1. **Data Acquisition** – Imported 16,092 reviews (ID, content, score, timestamp) from Kaggle.  
2. **Text Cleaning** – Removed duplicates, normalized text (lowercasing, lemmatization, regex cleaning).  
3. **Exploratory Data Analysis (EDA)** –  
   - Score distribution (positive, neutral, negative)  
   - Temporal trends (2014–2020 growth surge)  
   - Word clouds for positive vs. negative reviews  
4. **Sentiment Classification** – Applied Hugging Face `pysentimiento` (RoBERTa-based) for text-driven sentiment detection.  
5. **Pain Point Detection** – Used TF-IDF + Latent Dirichlet Allocation (LDA) to identify recurring complaint themes.  
6. **Insights & Reporting** – Aggregated findings into strategic recommendations for Any.do’s product roadmap.  

---

## ⚙️ Tools & Libraries

- **Python, Pandas, NumPy** – Data processing  
- **Regex, NLTK, WordNetLemmatizer** – Text normalization  
- **Matplotlib, Seaborn, WordCloud** – Visualization  
- **Scikit-learn, Gensim** – Topic modeling (TF-IDF, LDA)  
- **Hugging Face `pysentimiento`** – Transformer-based sentiment classification  
- **Google Colab** – Computational environment  

---

## 📈 Key Insights

- **Neutral “Swing” Segment** – 3,136 reviews scored 3 stars, representing a critical retention opportunity.  
- **Text vs. Ratings Disconnect** – 58% of reviews expressed Neutral/Negative sentiment despite high star ratings.  
- **Positive Themes** – Users praised core features: *tasks, calendar, lists*.  
- **Negative Themes** –  
  - Monetization friction: premium prompts, ads, poor “Pro” experience  
  - Workflow failures: unreliable reminders, notifications, sync issues  
  - Update regressions: widgets breaking after updates  
- **Strategic Priority** – Stabilize sync engine + refine premium experience to convert neutral users into advocates.  

---

## 📷 Sample Visualizations

**Sentiment Distribution Pie Chart**  
<img width="638" height="658" alt="image" src="https://github.com/user-attachments/assets/eb286764-de0a-475f-80c3-d110569e2905" />


**Positive Word Cloud**  
<img width="790" height="427" alt="image" src="https://github.com/user-attachments/assets/a681e09c-6575-48f9-ae12-5b273eb49fd7" />


**Negative Word Cloud**  
<img width="790" height="427" alt="image" src="https://github.com/user-attachments/assets/aad1d067-540b-4486-b815-974cb5ea271e" />


---

## 🚀 Outcomes

- Demonstrated limitations of rating-based sentiment analysis.  
- Built a reusable NLP pipeline for feedback-driven product optimization.  
- Delivered actionable roadmap: improve sync stability, premium reliability, and workflow integrity.  
- Showcased how **collective intelligence + NLP** can transform raw feedback into strategic insights.  

---

## 👤 Author

Developed by **Ajao Abiola Olanrewaju**  
🎓 School of Collective Intelligence, UM6P  
💼 Co-Founder & CEO @ BizIntel Enterprise  
🔗 [LinkedIn](https://www.linkedin.com/in/abiola-ajao/) | 📧 ajaoabiola0812@gmail.com  

 

Would you like me to also prepare a **shorter “featured project” snippet** (like a one-liner with emoji + link + description) so you can pin it at the top of your GitHub profile alongside your other projects?
