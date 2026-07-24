import streamlit as st
from utils import predict_leaf

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
st.subheader("AI-Powered Potato Disease Detection")

st.markdown("---")

# ----------------------------------
# Sidebar
# ----------------------------------
st.sidebar.header("Settings")

language = st.sidebar.selectbox(
    "🌍 Select Language",
    ["English", "Hindi"]
)

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

    if st.button("🔍 Detect Disease", use_container_width=True):

        with st.spinner("Analyzing leaf... Please wait..."):

            try:

                result = predict_leaf(
                    uploaded_file,
                    language=language
                )

                st.success("✅ Detection Complete!")

                st.markdown("---")

                # -------------------------
                # Metrics
                # -------------------------

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Disease",
                        result["disease_name"]
                    )

                with col2:
                    st.metric(
                        "Confidence",
                        f"{result['confidence']:.2f}%"
                    )

                with col3:
                    st.metric(
                        "Severity",
                        f"{result['severity']:.2f}%"
                    )

                st.info(
                    f"Severity Level: **{result['severity_level']}**"
                )

                st.markdown("---")

                # -------------------------
                # Treatment
                # -------------------------

                st.subheader("💊 Recommended Treatment")

                st.write(
                    f"**Medicine:** {result['medicine']}"
                )

                st.write(
                    f"**Dosage:** {result['dosage']}"
                )

                st.write("### Steps")

                for step in result["steps"]:
                    st.write(f"✅ {step}")

                st.markdown("---")
                st.subheader("🖼️ Visualization")

                # -------------------------
                # Images
                # -------------------------

                col1, col2 ,col3= st.columns(3)

                with col1:
                    st.subheader("Original Image")
                    st.image(
                        uploaded_file,
                        use_container_width=True
                    )

                with col2:
                    st.subheader("🔥 Grad-CAM Heatmap")
                    st.image(
                        result["heatmap"],
                        clamp=True,
                        use_container_width=True
                    )

                with col3:
                    st.subheader("🌿 Grad-CAM Overlay")
                    st.image(
                        result["overlay"],
                        use_container_width=True
                    )

            except Exception as e:
                st.error("❌ Error while running prediction.")
                st.exception(e)

else:
    st.info("👆 Upload a potato leaf image to begin.")