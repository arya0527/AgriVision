import streamlit as st

from agent import get_final_response


# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(
    page_title="🌿 AgriVision",
    page_icon="🌿",
    layout="wide"
)


# ----------------------------------
# Header
# ----------------------------------

st.title("🌿 AgriVision")
st.subheader(
    "AI-Powered Potato Disease Detection & Agricultural Assistant"
)

st.markdown("---")


# ----------------------------------
# Sidebar
# ----------------------------------

st.sidebar.header("⚙️ Settings")

language = st.sidebar.selectbox(
    "🌍 Select Language",
    ["English", "Hindi"]
)


# ----------------------------------
# Upload Image
# ----------------------------------

uploaded_file = st.file_uploader(
    "📤 Upload a Potato Leaf Image",
    type=["jpg", "jpeg", "png"]
)


# ----------------------------------
# Image Preview
# ----------------------------------

if uploaded_file is not None:

    st.success("✅ Image uploaded successfully!")

    st.image(
        uploaded_file,
        caption="Uploaded Potato Leaf",
        use_container_width=True
    )


    # ----------------------------------
    # Detect Disease
    # ----------------------------------

    if st.button(
        "🔍 Detect Disease",
        use_container_width=True
    ):

        with st.spinner(
            "🔬 Analyzing leaf and generating AI guidance..."
        ):

            try:

                # ==========================================
                # CNN → POTATO AGENT → LANGUAGE TEAM
                # ==========================================

                result = get_final_response(
                    uploaded_file,
                    language=language
                )


                # ==========================================
                # CNN RESULT
                # ==========================================

                cnn_result = result["cnn_result"]


                st.success(
                    "✅ Analysis Complete!"
                )

                st.markdown("---")


                # ==========================================
                # CNN METRICS
                # ==========================================

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


                # ==========================================
                # AI AGRICULTURAL GUIDANCE
                # ==========================================

                st.markdown("---")

                st.header(
                    "🤖 AI Agricultural Guidance"
                )


                st.markdown(
                    result["response"]
                )


                # ==========================================
                # MODEL VISUALIZATION
                # ==========================================

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


else:

    st.info(
        "👆 Upload a potato leaf image to begin."
    )