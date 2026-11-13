import json
import re

import streamlit as st
from groq import Groq


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Poster & Social Media Caption Maker",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: "DM Sans", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(108, 92, 231, 0.10), transparent 30%),
            radial-gradient(circle at 90% 0%, rgba(0, 180, 255, 0.08), transparent 30%),
            #f7f8fc;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* HERO */

    .hero {
        background: linear-gradient(
            135deg,
            #ffffff 0%,
            #f2efff 50%,
            #eef9ff 100%
        );

        border: 1px solid #e7e3f5;
        border-radius: 28px;
        padding: 42px;
        margin-bottom: 30px;

        box-shadow:
            0 20px 60px rgba(39, 35, 75, 0.08);
    }

    .badge {
        display: inline-block;
        background: #ebe7ff;
        color: #5b4cc4;
        padding: 8px 15px;
        border-radius: 50px;

        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0.7px;
        text-transform: uppercase;
    }

    .hero-title {
        font-family: "Manrope", sans-serif;

        font-size: clamp(36px, 6vw, 64px);
        line-height: 1.05;

        color: #171621;

        font-weight: 800;

        margin-top: 18px;
        margin-bottom: 15px;
    }

    .hero-subtitle {
        color: #5e5c69;

        font-size: 18px;
        line-height: 1.7;

        max-width: 850px;
    }

    /* SECTION */

    .section-title {
        font-family: "Manrope", sans-serif;

        font-size: 27px;
        font-weight: 800;

        color: #171621;

        margin-top: 18px;
        margin-bottom: 15px;
    }

    /* CARDS */

    .card {
        background: #ffffff;

        border: 1px solid #e8e7ef;

        border-radius: 22px;

        padding: 25px;

        margin-bottom: 20px;

        box-shadow:
            0 12px 40px rgba(30, 28, 55, 0.055);
    }

    .card-title {
        font-family: "Manrope", sans-serif;

        font-size: 19px;
        font-weight: 800;

        color: #1b1a25;

        margin-bottom: 5px;
    }

    .card-description {
        color: #777582;

        font-size: 14px;

        margin-bottom: 18px;
    }

    /* RESULT CARDS */

    .result-card {
        background: white;

        border: 1px solid #e7e6ee;

        border-radius: 20px;

        padding: 24px;

        min-height: 170px;

        box-shadow:
            0 10px 35px rgba(30, 28, 55, 0.05);
    }

    .result-title {
        font-family: "Manrope", sans-serif;

        font-size: 19px;

        font-weight: 800;

        color: #171621;

        margin-bottom: 12px;
    }

    .result-content {
        color: #35343e;

        font-size: 16px;

        line-height: 1.8;

        white-space: pre-wrap;
    }

    /* BUTTON */

    div.stButton > button {
        min-height: 48px;

        border-radius: 13px;

        font-size: 15px;

        font-weight: 800;

        border: 1px solid #dddbe8;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(
            90deg,
            #6c5ce7,
            #4b8dff
        );

        color: white;

        border: none;
    }

    /* INPUTS */

    .stTextInput input,
    .stTextArea textarea {
        border-radius: 12px !important;

        font-size: 16px !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        border-radius: 12px;
    }

    /* FOOTER */

    .footer {
        text-align: center;

        color: #8b8994;

        font-size: 13px;

        margin-top: 35px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "result" not in st.session_state:
    st.session_state.result = None


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <span class="badge">
            ✨ AI Content Studio
        </span>

        <div class="hero-title">
            AI Poster & Social Media<br>
            Caption Maker
        </div>

        <div class="hero-subtitle">
            Create professional social media content for Instagram,
            Facebook, and TikTok using AI. Upload your poster,
            describe your idea, choose a style, and generate
            ready-to-use content in seconds.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CREATE CONTENT
# =========================================================

st.markdown(
    '<div class="section-title">Create Your Content</div>',
    unsafe_allow_html=True,
)


left, right = st.columns(2, gap="large")


# =========================================================
# LEFT COLUMN
# =========================================================

with left:

    st.markdown(
        """
        <div class="card">

            <div class="card-title">
                🖼️ Upload Your Poster
            </div>

            <div class="card-description">
                Upload your poster, product image, event design,
                or social media graphic.
            </div>

        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        st.image(
            uploaded_file,
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# RIGHT COLUMN
# =========================================================

with right:

    st.markdown(
        """
        <div class="card">

            <div class="card-title">
                📝 Content Details
            </div>

            <div class="card-description">
                Tell the AI what your business, product,
                event, or content is about.
            </div>

        """,
        unsafe_allow_html=True,
    )

    topic = st.text_area(
        "Business / Product / Event / Topic",
        placeholder=(
            "Example: New luxury coffee shop opening in Islamabad "
            "with premium coffee and a modern atmosphere."
        ),
        height=140,
    )

    platform = st.selectbox(
        "Select Platform",
        [
            "Instagram",
            "Facebook",
            "TikTok",
        ],
    )

    style = st.selectbox(
        "Select Content Style",
        [
            "Professional",
            "Creative",
            "Luxury",
            "Minimal",
            "Friendly",
            "Promotional",
        ],
    )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# GENERATE BUTTON
# =========================================================

st.markdown(
    """
    <div class="card">
    """,
    unsafe_allow_html=True,
)

generate_button = st.button(
    "✨ Generate Professional Content",
    type="primary",
    use_container_width=True,
)

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# AI GENERATION FUNCTION
# =========================================================

def generate_content(topic, platform, style):

    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured in Streamlit Secrets."
        )

    client = Groq(api_key=api_key)

    system_prompt = """
You are an expert social media copywriter and digital marketing
content strategist.

Create professional, engaging and natural social media content.

Return ONLY valid JSON.

Required JSON structure:

{
    "headline": "...",
    "caption": "...",
    "hashtags": "...",
    "call_to_action": "..."
}

Rules:

1. Headline:
- Short
- Attractive
- Maximum 10 words

2. Caption:
- Professional
- Engaging
- Easy to read
- 2 to 4 short paragraphs
- Suitable for the selected platform

3. Hashtags:
- 6 to 10 relevant hashtags
- Every hashtag must start with #

4. Call to action:
- Short
- Clear
- Action-oriented

Do not invent:
- prices
- discounts
- addresses
- dates
- statistics
- product specifications
- false claims

Match the selected platform and content style.
"""

    user_prompt = f"""
Create social media content for:

Topic:
{topic}

Platform:
{platform}

Style:
{style}

Make the result professional and ready to publish.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.7,
        max_tokens=900,
    )

    content = response.choices[0].message.content

    # Remove markdown code fences if AI adds them
    content = re.sub(
        r"^```json\s*",
        "",
        content.strip(),
        flags=re.IGNORECASE,
    )

    content = re.sub(
        r"\s*```$",
        "",
        content,
    )

    return json.loads(content)


# =========================================================
# GENERATE ACTION
# =========================================================

if generate_button:

    if not topic.strip():

        st.warning(
            "Please enter your business, product, event, or topic first."
        )

    else:

        try:

            with st.spinner(
                "✨ AI is creating your professional content..."
            ):

                st.session_state.result = generate_content(
                    topic=topic.strip(),
                    platform=platform,
                    style=style,
                )

            st.success(
                "Your social media content has been generated successfully!"
            )

        except Exception as error:

            st.error(
                "Something went wrong while generating the content."
            )

            with st.expander("Technical Details"):
                st.code(str(error))


# =========================================================
# RESULTS
# =========================================================

if st.session_state.result:

    result = st.session_state.result

    st.markdown(
        '<div class="section-title">Generated Content</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------
    # HEADLINE + CTA
    # -----------------------------

    col1, col2 = st.columns(2, gap="large")

    with col1:

        st.markdown(
            f"""
            <div class="result-card">

                <div class="result-title">
                    🎯 Headline
                </div>

                <div class="result-content">
                    {result["headline"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.text_area(
            "Copy Headline",
            value=result["headline"],
            height=90,
            label_visibility="collapsed",
            key="headline_text",
        )

    with col2:

        st.markdown(
            f"""
            <div class="result-card">

                <div class="result-title">
                    📣 Call-to-Action
                </div>

                <div class="result-content">
                    {result["call_to_action"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.text_area(
            "Copy CTA",
            value=result["call_to_action"],
            height=90,
            label_visibility="collapsed",
            key="cta_text",
        )

    # -----------------------------
    # CAPTION
    # -----------------------------

    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-title">
                ✍️ Social Media Caption
            </div>

            <div class="result-content">
                {result["caption"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.text_area(
        "Copy Caption",
        value=result["caption"],
        height=230,
        label_visibility="collapsed",
        key="caption_text",
    )

    # -----------------------------
    # HASHTAGS
    # -----------------------------

    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-title">
                #️⃣ Hashtags
            </div>

            <div class="result-content">
                {result["hashtags"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.text_area(
        "Copy Hashtags",
        value=result["hashtags"],
        height=110,
        label_visibility="collapsed",
        key="hashtags_text",
    )

    # -----------------------------
    # GENERATE AGAIN
    # -----------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "🔄 Generate New Content",
        use_container_width=True,
    ):

        st.session_state.result = None
        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        AI Poster & Social Media Caption Maker
        · Built with Python + Streamlit + Groq
    </div>
    """,
    unsafe_allow_html=True,
)
