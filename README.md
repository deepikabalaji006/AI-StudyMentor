## AI StudyMentor 📚

AI-powered, rule-based study guidance aligned with **SDG 4 – Quality Education**.

This Streamlit web app helps learners plan their exam preparation by:
- Estimating an **Exam Readiness Score (0–100)**
- Identifying **risk level** (Low / Medium / High)
- Generating a **personalized daily study plan**
- Providing **AI-style recommendations** and **motivational feedback**

All logic is simple and transparent – there is **no model training** or external API required.

### Running the app locally

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

### Deploying to Streamlit Community Cloud

1. Push this project to a public Git repository (e.g. GitHub).
2. Go to Streamlit Community Cloud and create a new app.
3. Point it to your repo and select:
   - **Main file**: `app.py`
4. Deploy – Streamlit will automatically install from `requirements.txt`.

### Ethical disclaimer

This application provides **general educational guidance only**. It does not replace
professional academic counseling, does not predict actual exam scores, and may not
fully account for individual circumstances, learning needs, or well-being. Always
use this tool as one input among many and seek support from teachers, guardians,
or qualified professionals where needed.

