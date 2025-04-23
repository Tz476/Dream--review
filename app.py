import threading
import time
import streamlit as st
import uuid
import os
import logging
import chat_ai
import text2img

# Suppress warnings of streamlit.watcher.local_sources_watcher
from streamlit.logger import get_logger
_LOGGER = get_logger('streamlit.watcher.local_sources_watcher')
_LOGGER.setLevel(logging.ERROR)

IMAGE_DIR = 'images'


def init_models():
    """
    Initialize the models
    """
    if 'results' not in st.session_state:
        results = {'errors': [], 'data': {}}
        result1 = text2img.initialize()
        if isinstance(result1, str):
            results['errors'].append(result1)
        else:
            results['data']['text2img'] = result1
        result2 = chat_ai.initialize()
        if result2:
            results['errors'].append(result2)
        if results['errors']:
            results['errors'].append('Please refresh the webpage after fixing the above errors.')
        st.session_state['results'] = results
    return st.session_state['results']


def rewrite_dream(container, dream):
    """
    Rewrite the dream using AI
    """
    task_completed = False

    def task():
        nonlocal dream, task_completed
        dream = chat_ai.rewrite(dream).strip()
        task_completed = True

    # Start a thread to rewrite the dream
    thread = threading.Thread(target=task)
    thread.start()

    # Update timer
    start_time = time.time()
    container.text('0s')
    while not task_completed:
        time.sleep(0.1)
        used_time = time.time() - start_time
        container.text('%.1fs' % used_time)
    thread.join()
    return dream


def create_image(data, container, dream, image_index, config):
    """
    Create one image
    """
    task_completed = False

    image_path = os.path.join(IMAGE_DIR, '%s.png' % str(uuid.uuid4()))

    def task():
        nonlocal dream, task_completed
        model_data = data['text2img']
        text2img.generate_image(model_data, dream, image_path, config)
        task_completed = True

    # Start a thread to rewrite the dream
    thread = threading.Thread(target=task)
    thread.start()

    # Update timer
    start_time = time.time()
    container.text('0s')
    while not task_completed:
        time.sleep(0.1)
        used_time = time.time() - start_time
        container.text('%.1fs' % used_time)
    thread.join()

    caption = '%s image' % (['First', 'Second', 'Third'])[image_index - 1]
    container.image(image_path, caption=caption)
    return dream


def create_side_bar():
    """
    Create a sidebar
    """
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                min-width: 480px;
                max-width: 480px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.sidebar:
        with st.form(key='left_form'):
            st.info("🧸Create Pictures from Textual Dream Descriptions🧸")

            # Adjust setting
            with st.expander(":blue[**Adjust settings**]"):
                num_images = st.slider(
                    "Number of images", value=1, min_value=1, max_value=3)
                guidance_scale = st.slider(
                    "The intensity of guidance", value=7.5, min_value=7.0, max_value=8.0, step=0.1)

            dream = st.text_area(":orange[**✍️ Describe your dream**]").strip()
            negative_prompt = st.text_area(":orange[**⚠️ Hope these contents are not included in the images ️**]",
                                           value="distorted features, disfigured",
                                           help="This is a negative prompt, basically type what you don't want in images")

            rewrite = st.checkbox("Rewrite the dream using AI")

            submitted = st.form_submit_button(
                'Replay a Dream', type="primary", use_container_width=True)
            container = st.empty()
            if submitted and not dream:
                container.error('Please describe you dream first')
                submitted = False

            # Write the data to session_state
            st.session_state['num_images'] = num_images
            st.session_state['guidance_scale'] = guidance_scale
            st.session_state['dream'] = dream
            st.session_state['negative_prompt'] = negative_prompt
            st.session_state['rewrite'] = rewrite
            st.session_state['submitted'] = submitted


def create_main_Page(data):
    """
    Create a main page
    """
    # Read data from session_state
    num_images = st.session_state['num_images']
    guidance_scale = st.session_state['guidance_scale']
    dream = st.session_state['dream']
    negative_prompt = st.session_state['negative_prompt']
    rewrite = st.session_state['rewrite']
    submitted = st.session_state['submitted']

    st.title('✨️ Dream Replay ')
    st.subheader('☁️ Your dream description')
    container1 = st.empty()
    st.subheader('🖼️ Generated images')
    containers = [st.empty() for _ in range(num_images)]
    if submitted:
        if rewrite:
            # Rewrite the dream
            dream = rewrite_dream(container1, dream)
        container1.info(dream)
        # Generate images
        for i in range(num_images):
            container = containers[i]
            create_image(data, container, dream, i + 1, config={
                'guidance_scale': guidance_scale, 'negative_prompt': negative_prompt
            })
    else:
        container1.info('Please describe you dream first')
        containers[0].info('No images')


def main():
    os.makedirs(IMAGE_DIR, exist_ok=True)
    # Set page
    st.set_page_config(page_title='Dream Replay', page_icon='✨️')
    # Initialize models
    results = init_models()
    if results['errors']:
        st.subheader('❌ Failed to initialize AI models')
        for i, result in enumerate(results['errors']):
            st.write('%d: %s' % (i + 1, result))
    else:
        # Create a sidebar
        create_side_bar()
        # Main page
        create_main_Page(results['data'])


if __name__ == '__main__':
    main()
