import streamlit as st
from typing import Dict, Tuple


def calculate_exam_readiness(
    exam_type: str,
    subjects_count: int,
    daily_hours: int,
    days_left: int,
    understanding_level: int,
) -> Tuple[int, str]:
    """
    Simple rule-based calculation for an exam readiness score (0–100).

    This is NOT a statistical or ML model – just transparent, explainable rules.
    """
    # Normalize core factors to 0–1 ranges
    max_days = 180
    max_daily_hours = 12
    max_understanding = 10

    # Weighting: understanding and consistency matter more than raw time
    time_factor = min(daily_hours / max_daily_hours, 1.0)
    time_horizon_factor = min(days_left / max_days, 1.0)
    understanding_factor = min(understanding_level / max_understanding, 1.0)

    # Penalty for many subjects with limited time
    subjects_penalty = min(subjects_count / 8, 1.0)

    # Base score from understanding and preparation horizon
    base_score = 40 * understanding_factor + 25 * time_horizon_factor

    # Add contribution from available daily time
    time_score = 25 * time_factor

    # Reduce score if many subjects relative to preparation time
    load_penalty = 15 * subjects_penalty * (1 - time_horizon_factor)

    raw_score = base_score + time_score - load_penalty

    # Adjust slightly by exam type (competitive exams are typically harder)
    if exam_type == "Competitive Exam":
        raw_score -= 7
    elif exam_type == "College Exam":
        raw_score -= 3

    # Clamp to 0–100
    score = max(0, min(int(raw_score), 100))

    # Risk level decisions are transparent thresholds
    if score >= 70:
        risk = "Low"
    elif score >= 40:
        risk = "Medium"
    else:
        risk = "High"

    return score, risk


def generate_subject_priorities(
    subjects_count: int,
    understanding_level: int,
    days_left: int,
    daily_hours: int,
) -> Dict[str, Dict[str, float]]:
    """
    Rule-based "agent" for subject priorities and time allocation.

    - Early days or low understanding → more time on fundamentals.
    - Close to the exam → more revision and mock tests.
    """
    # Guard against edge cases to keep logic robust
    subjects_count = max(1, min(subjects_count, 8))
    daily_hours = max(0, daily_hours)
    days_left = max(1, days_left)

    # Hypothetical relative difficulty profile across subjects
    difficulty_profile = [0.8, 1.0, 1.2, 1.1, 0.9, 1.3, 1.0, 0.7][:subjects_count]

    # Lower understanding → more weight on harder subjects
    difficulty_amplifier = 1.0 + (10 - understanding_level) * 0.06
    weights = [d * difficulty_amplifier for d in difficulty_profile]

    total_weight = sum(weights) or 1.0
    subject_hours = []
    for i, w in enumerate(weights):
        # Allocate proportionally to weight
        hours = (w / total_weight) * daily_hours

        # If exam is very close, shift some hours from content learning to revision
        if days_left <= 7:
            focus_learning = 0.4
            focus_revision = 0.6
        elif days_left <= 30:
            focus_learning = 0.55
            focus_revision = 0.45
        else:
            focus_learning = 0.7
            focus_revision = 0.3

        subject_hours.append(
            {
                "name": f"Subject {i+1}",
                "total_hours": round(hours, 2),
                "concept_learning_hours": round(hours * focus_learning, 2),
                "revision_hours": round(hours * focus_revision, 2),
            }
        )

    # Convert to named dictionary for easy display
    return {sh["name"]: sh for sh in subject_hours}


def generate_recommendations(
    exam_type: str,
    score: int,
    risk_level: str,
    daily_hours: int,
    days_left: int,
    understanding_level: int,
) -> Tuple[str, str]:
    """
    Produce:
    - strategy_recommendations: practical, study-related tips
    - motivational_message: supportive, learner-centered feedback
    """
    # Strategy recommendations
    lines = []
    if risk_level == "High":
        lines.append(
            "- Focus first on **core concepts** and past questions instead of trying to cover everything."
        )
        lines.append(
            "- Use **short, focused sessions** of 25–30 minutes with 5-minute breaks (Pomodoro)."
        )
    elif risk_level == "Medium":
        lines.append(
            "- Consolidate what you already know and **close the biggest gaps** in 1–2 key subjects."
        )
        lines.append(
            "- Add **regular mini-revisions** at the end of each day (10–15 minutes)."
        )
    else:  # Low risk
        lines.append(
            "- Maintain your current pace but add **weekly mock tests** to simulate real exam conditions."
        )
        lines.append(
            "- Start building a **formula / key-concept sheet** for quick revision."
        )

    # Exam-type specific suggestions
    if exam_type == "School Exam":
        lines.append(
            "- Align your preparation with the **official syllabus and textbook exercises**."
        )
    elif exam_type == "College Exam":
        lines.append(
            "- Review **lecture notes, assignments, and previous semester papers**."
        )
    else:  # Competitive
        lines.append(
            "- Prioritize **mock tests and previous years' question papers** to understand patterns."
        )

    # Time horizon and understanding-based tweaks
    if days_left <= 7:
        lines.append(
            "- With limited days left, **avoid learning brand new topics** unless they are very high-yield."
        )
    if daily_hours < 2:
        lines.append(
            "- Try to carve out at least **1–2 distraction-free hours** daily, even if split into small blocks."
        )
    if understanding_level <= 4:
        lines.append(
            "- Use **beginner-friendly resources** (YouTube explainers, basic notes) before jumping into tough problems."
        )

    strategy_recommendations = "\n".join(lines)

    # Motivational message – supportive, non-judgmental
    if score >= 70:
        motivation = (
            "You’re on a **strong path** – keep your momentum, but remember to rest and protect your mental health. "
            "Small, consistent effort now can make a big difference on exam day."
        )
    elif score >= 40:
        motivation = (
            "You have a **real opportunity to improve** from here. Focus on one improvement at a time and track your progress. "
            "Progress, not perfection, is the goal."
        )
    else:
        motivation = (
            "It’s okay if you’re starting from behind – what matters is the **next step**, not the past. "
            "Begin with short, realistic goals, and celebrate every small win. You are capable of learning and growing."
        )

    return strategy_recommendations, motivation


def main() -> None:
    """
    Streamlit UI for the AI StudyMentor application.

    This app aims to support SDG 4 (Quality Education) by giving accessible,
    transparent, rule-based study guidance for learners.
    """
    st.set_page_config(
        page_title="AI StudyMentor",
        page_icon="📚",
        layout="centered",
    )

    # --- Header / Introduction ---
    st.title("AI StudyMentor 📚")
    st.markdown(
        """
**AI-powered study guidance aligned with SDG 4 – Quality Education.**

This tool provides **simple, rule-based study strategies** to help you plan for upcoming exams.
It is designed to be transparent and understandable, not a black-box AI model.
"""
    )

    st.info(
        "This app is an educational support tool and **does not guarantee exam results**. "
        "Always combine AI-generated suggestions with your own judgment and, where appropriate, guidance from qualified teachers or mentors."
    )

    st.markdown("---")

    # --- Input Sidebar ---
    with st.sidebar:
        st.header("Your Exam Profile")

        exam_type = st.selectbox(
            "Exam type",
            options=["School Exam", "College Exam", "Competitive Exam"],
            index=0,
            help="Different exam types can have different difficulty and expectations.",
        )

        subjects_count = st.slider(
            "Number of subjects",
            min_value=1,
            max_value=8,
            value=4,
        )

        daily_hours = st.slider(
            "Daily study hours (realistic)",
            min_value=0,
            max_value=12,
            value=3,
        )

        days_left = st.slider(
            "Days left until the exam",
            min_value=1,
            max_value=180,
            value=60,
        )

        understanding_level = st.slider(
            "Self-rated understanding level (overall)",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = very low confidence, 10 = very strong understanding.",
        )

        generate_btn = st.button("Generate Study Strategy ✨", use_container_width=True)

    # --- Main Output Area ---
    if generate_btn:
        score, risk_level = calculate_exam_readiness(
            exam_type=exam_type,
            subjects_count=subjects_count,
            daily_hours=daily_hours,
            days_left=days_left,
            understanding_level=understanding_level,
        )

        subject_plan = generate_subject_priorities(
            subjects_count=subjects_count,
            understanding_level=understanding_level,
            days_left=days_left,
            daily_hours=daily_hours,
        )

        recommendations, motivation = generate_recommendations(
            exam_type=exam_type,
            score=score,
            risk_level=risk_level,
            daily_hours=daily_hours,
            days_left=days_left,
            understanding_level=understanding_level,
        )

        # --- Exam Readiness Summary ---
        st.subheader("📊 Exam Readiness Overview")
        col1, col2 = st.columns(2)

        with col1:
            st.metric(label="Exam Readiness Score", value=f"{score} / 100")
        with col2:
            if risk_level == "Low":
                st.success(f"Risk Level: {risk_level}")
            elif risk_level == "Medium":
                st.warning(f"Risk Level: {risk_level}")
            else:
                st.error(f"Risk Level: {risk_level}")

        st.caption(
            "This score is based on your available time, days remaining, number of subjects, "
            "and self-rated understanding. It is **only an estimate** to help structure your plan."
        )

        # --- Personalized Study Plan ---
        st.markdown("---")
        st.subheader("📝 Personalized Daily Study Plan")

        if daily_hours == 0:
            st.warning(
                "You set daily study hours to 0. To make progress, try to allocate at least **30–60 minutes** per day, "
                "even if in short bursts."
            )
        else:
            st.write(
                f"Based on **{daily_hours} hours/day** and **{subjects_count} subjects**, "
                "here is a suggested **daily time distribution**:"
            )

        for subject_name, info in subject_plan.items():
            with st.expander(subject_name, expanded=True):
                st.write(
                    f"- **Total per day**: {info['total_hours']} hours\n"
                    f"- **Concept learning / practice**: {info['concept_learning_hours']} hours\n"
                    f"- **Revision / recap**: {info['revision_hours']} hours"
                )

        # --- AI-generated Recommendations ---
        st.markdown("---")
        st.subheader("🎯 Strategy Recommendations")
        st.markdown(recommendations)

        # --- Motivational Feedback ---
        st.markdown("---")
        st.subheader("💬 Motivational Feedback")
        st.markdown(motivation)

    else:
        st.info(
            "Set your exam details in the sidebar and click **“Generate Study Strategy ✨”** "
            "to receive a personalized plan."
        )


    st.markdown("---")
    st.caption(
        "Ethical disclaimer: This application provides **general educational guidance only**. "
        "It does not replace professional academic counseling, does not predict actual exam scores, "
        "and may not fully account for your personal circumstances, learning needs, or well-being. "
        "Please use this as one input among many, and seek support from teachers, guardians, or qualified professionals when needed."
    )


if __name__ == "__main__":
    main()

