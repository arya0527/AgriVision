import uuid
import streamlit as st

from agent import get_final_response, get_follow_ups


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="🌿 AgriVision",
    page_icon="🌿",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

# Agno session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Store CNN + agent analysis
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# Store messages for displaying chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# HEADER
# ============================================================

st.title("🌿 AgriVision")

st.subheader(
    "AI-Powered Potato Disease Detection & Agricultural Assistant"
)

st.markdown("---")


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Settings")

language = st.sidebar.selectbox(
    "🌍 Select Language",
    ["English", "Hindi"]
)


# ============================================================
# IMAGE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📤 Upload a Potato Leaf Image",
    type=["jpg", "jpeg", "png"]
)


# ============================================================
# IMAGE PREVIEW
# ============================================================

if uploaded_file is not None:

    st.success("✅ Image uploaded successfully!")

    st.image(
        uploaded_file,
        caption="Uploaded Potato Leaf",
        use_container_width=True
    )

    # ========================================================
    # DETECT DISEASE
    # ========================================================

    if st.button(
        "🔍 Detect Disease",
        use_container_width=True
    ):

        with st.spinner(
            "🔬 Analyzing leaf and generating AI guidance..."
        ):

            try:

                # ------------------------------------------------
                # NEW ANALYSIS = NEW SESSION
                # ------------------------------------------------

                st.session_state.session_id = str(uuid.uuid4())

                # Clear old chat
                st.session_state.chat_history = []

                # ------------------------------------------------
                # CNN → POTATO AGENT → LANGUAGE TEAM
                # ------------------------------------------------

                result = get_final_response(
                    uploaded_file,
                    language=language
                )

                # Save result
                st.session_state.analysis_result = result

                # ------------------------------------------------
                # CNN RESULT
                # ------------------------------------------------

                cnn_result = result["cnn_result"]

                st.success("✅ Analysis Complete!")

                st.markdown("---")

                # =================================================
                # CNN ANALYSIS
                # =================================================

                st.header("🔬 CNN Analysis")

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Disease",
                        cnn_result["disease_name"]
                    )

                with col2:

                    st.metric(
                        "Confidence",
                        f'{cnn_result["confidence"]:.2f}%'
                    )

                with col3:

                    st.metric(
                        "Severity",
                        cnn_result["severity_level"]
                    )

                st.info(
                    f'Severity Estimation: '
                    f'**{cnn_result["severity"]:.2f}%**'
                )

                # =================================================
                # AI AGRICULTURAL GUIDANCE
                # =================================================

                st.markdown("---")

                st.header(
                    "🤖 AI Agricultural Guidance"
                )

                st.markdown(
                    result["response"]
                )

                # =================================================
                # MODEL VISUALIZATION
                # =================================================

                st.markdown("---")

                st.header(
                    "🧠 Model Visualization"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.subheader(
                        "Original Image"
                    )

                    st.image(
                        uploaded_file,
                        use_container_width=True
                    )

                with col2:

                    st.subheader(
                        "🔥 Grad-CAM Heatmap"
                    )

                    st.image(
                        cnn_result["heatmap"],
                        clamp=True,
                        use_container_width=True
                    )

                with col3:

                    st.subheader(
                        "🌿 Grad-CAM Overlay"
                    )

                    st.image(
                        cnn_result["overlay"],
                        use_container_width=True
                    )

            except Exception as e:

                st.error(
                    "❌ Error while running AgriVision."
                )

                st.exception(e)


# ============================================================
# FOLLOW-UP CHAT
# ============================================================

if st.session_state.analysis_result is not None:

    st.markdown("---")

    st.header("💬 Ask AgriVision")

    st.caption(
        "Ask follow-up questions about the analyzed potato plant."
    )

    # --------------------------------------------------------
    # DISPLAY CHAT HISTORY
    # --------------------------------------------------------

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )

    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    question = st.chat_input(
        "Ask a follow-up question..."
    )

    if question:

        # ====================================================
        # DISPLAY USER MESSAGE
        # ====================================================

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        # ====================================================
        # FOLLOW-UP AGENT
        # ====================================================

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    analysis = (
                        st.session_state.analysis_result
                    )

                    cnn_result = analysis["cnn_result"]

                    potato_solution = (
                        analysis["potato_solution"]
                    )

                    # ------------------------------------------------
                    # FOLLOW-UP PROMPT
                    # ------------------------------------------------

                    prompt = f"""
Continue the existing AgriVision conversation.

The CNN has already analyzed this potato leaf.

==============================
CNN RESULT
==============================

Disease:
{cnn_result["disease_name"]}

Confidence:
{cnn_result["confidence"]:.2f}%

Severity:
{cnn_result["severity_level"]}

Severity Percentage:
{cnn_result["severity"]:.2f}%

==============================
PREVIOUS AGRICULTURAL GUIDANCE
==============================

{potato_solution}

==============================
FARMER'S NEW QUESTION
==============================

{question}

==============================

Answer the farmer's question using the
current conversation history.

IMPORTANT:

- Remember information the farmer has already told you.
- Do NOT perform another CNN diagnosis.
- Do NOT change the CNN disease.
- Do NOT change the CNN confidence.
- Do NOT change the CNN severity.
- Answer the actual question directly.
- Use simple and practical language.
"""

                    # ------------------------------------------------
                    # AGNO SESSION MEMORY
                    # ------------------------------------------------

                    response = get_follow_ups.run(
                        prompt,
                        session_id=st.session_state.session_id
                    )

                    answer = response.content

                    # Display response
                    st.markdown(answer)

                    # Save response for Streamlit UI
                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                except Exception as e:

                    st.error(
                        "❌ Error while answering your question."
                    )

                    st.exception(e)


# ============================================================
# INITIAL MESSAGE
# ============================================================

else:

    if uploaded_file is None:

        st.info(
            "👆 Upload a potato leaf image to begin."
        )