import streamlit as st
import requests


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Image & Text Generator",
    page_icon="🤖",
    layout="wide"
)


# =====================================================
# FASTAPI BACKEND
# =====================================================

API_URL = "http://127.0.0.1:8000"


# =====================================================
# HEADER
# =====================================================

st.title("🤖 AI Image & Text Generator")

st.markdown(
    "Generate images from text and generate text "
    "from images using local AI models."
)

st.divider()


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("⚙️ AI Models")

st.sidebar.info(
    """
    **Text → Image**

    `segmind/tiny-sd`

    **Image → Text**

    `Salesforce/blip-image-captioning-base`
    """
)

st.sidebar.divider()

st.sidebar.write("Backend")

st.sidebar.code(
    "FastAPI : 8000"
)


# =====================================================
# SELECT MODE
# =====================================================

mode = st.radio(
    "Choose an operation",
    [
        "🎨 Text → Image",
        "🖼️ Image → Text"
    ],
    horizontal=True
)


# =====================================================
# TEXT → IMAGE
# =====================================================

if mode == "🎨 Text → Image":

    st.header("🎨 Text → Image")

    st.write(
        "Enter a prompt and Tiny-SD will generate an image."
    )

    prompt = st.text_area(
        "Enter your prompt",
        placeholder=(
            "Example: A beautiful white cat "
            "sitting in a garden, realistic photography"
        ),
        height=140
    )

    # Example prompts

    st.write("💡 Example:")

    example = st.selectbox(
        "Choose an example prompt",
        [
            "Select an example",

            "A cute white cat sitting in a beautiful garden",

            "A futuristic city at night with neon lights",

            "A beautiful mountain landscape at sunset",

            "A sports car parked on a wet street",

            "A small wooden house in a snowy forest"
        ]
    )

    if example != "Select an example":

        prompt = example

    # Generate button

    if st.button(
        "🎨 Generate Image",
        type="primary",
        use_container_width=True
    ):

        if not prompt.strip():

            st.warning(
                "⚠️ Please enter a prompt first."
            )

        else:

            with st.spinner(
                "Generating image... Please wait ⏳"
            ):

                try:

                    response = requests.post(
                        f"{API_URL}/generate",
                        data={
                            "prompt": prompt
                        },
                        timeout=600
                    )

                    if response.status_code == 200:

                        content_type = response.headers.get(
                            "content-type",
                            ""
                        )

                        if "image" in content_type:

                            st.success(
                                "✅ Image generated successfully!"
                            )

                            st.image(
                                response.content,
                                caption="Generated Image",
                                use_container_width=True
                            )

                            st.download_button(
                                label="⬇️ Download Image",
                                data=response.content,
                                file_name="generated_image.png",
                                mime="image/png",
                                use_container_width=True
                            )

                        else:

                            try:

                                result = response.json()

                                st.error(
                                    result.get(
                                        "error",
                                        "Image generation failed."
                                    )
                                )

                            except Exception:

                                st.error(
                                    response.text
                                )

                    else:

                        st.error(
                            f"FastAPI Error: "
                            f"{response.status_code}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ FastAPI backend is not running."
                    )

                    st.code(
                        "python -m uvicorn app:app --reload"
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "⏳ Request timed out. "
                        "Tiny-SD may be slow on CPU."
                    )

                except Exception as e:

                    st.error(
                        f"❌ Error: {str(e)}"
                    )


# =====================================================
# IMAGE → TEXT
# =====================================================

else:

    st.header("🖼️ Image → Text")

    st.write(
        "Upload an image and BLIP will generate a description."
    )

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp"
        ]
    )

    if uploaded_file:

        st.image(
            uploaded_file,
            caption="Uploaded Image",
            use_container_width=True
        )

        st.divider()

        if st.button(
            "📝 Generate Text",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "Analyzing image... Please wait ⏳"
            ):

                try:

                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type
                        )
                    }

                    response = requests.post(
                        f"{API_URL}/image-to-text",
                        files=files,
                        timeout=300
                    )

                    if response.status_code == 200:

                        result = response.json()

                        if result.get("success"):

                            st.success(
                                "✅ Text generated successfully!"
                            )

                            st.subheader(
                                "📝 Generated Text"
                            )

                            generated_text = result.get(
                                "generated_text",
                                ""
                            )

                            st.text_area(
                                "Result",
                                value=generated_text,
                                height=150
                            )

                        else:

                            st.error(
                                result.get(
                                    "error",
                                    "Text generation failed."
                                )
                            )

                    else:

                        st.error(
                            f"FastAPI Error: "
                            f"{response.status_code}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ FastAPI backend is not running."
                    )

                    st.code(
                        "python -m uvicorn app:app --reload"
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "⏳ Request timed out."
                    )

                except Exception as e:

                    st.error(
                        f"❌ Error: {str(e)}"
                    )

    else:

        st.info(
            "👆 Upload an image to get started."
        )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "🤖 Powered by Segmind Tiny-SD + BLIP | FastAPI + Streamlit"
)