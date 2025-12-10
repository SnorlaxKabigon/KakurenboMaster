import streamlit as st
import cv2
import numpy as np
import easyocr
from PIL import Image

st.title("かくれんぼマスター")
st.write("画像をアップロードして、探したい数字を入力してください。")

# Initialize EasyOCR reader (cache it to avoid reloading)
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en']) # Numbers are usually recognized with English model

reader = load_reader()

uploaded_files = st.file_uploader("画像を選択してください", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
target_number = st.text_input("探したい数字を入力してください (3桁)", max_chars=3)

if uploaded_files:
    if target_number:
        if len(target_number) != 3 or not target_number.isdigit():
            st.warning("3桁の数字を入力してください。")
        else:
            if st.button("探す！"):
                with st.spinner('数字を探しています...'):
                    for uploaded_file in uploaded_files:
                        # Convert the file to an opencv image.
                        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                        image = cv2.imdecode(file_bytes, 1)
                        
                        # Detect text
                        results = reader.readtext(image)
                        
                        found = False
                        output_image = image.copy()
                        
                        for (bbox, text, prob) in results:
                            # Clean text and check if it matches target
                            # Remove spaces and non-numeric chars just in case
                            clean_text = ''.join(filter(str.isdigit, text))
                            
                            if clean_text == target_number:
                                found = True
                                # bbox is [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
                                
                                # Get coordinates
                                (tl, tr, br, bl) = bbox
                                tl = (int(tl[0]), int(tl[1]))
                                br = (int(br[0]), int(br[1]))
                                
                                # Calculate center and radius for circle
                                center_x = int((tl[0] + br[0]) / 2)
                                center_y = int((tl[1] + br[1]) / 2)
                                
                                # Radius can be half the diagonal or max of width/height
                                width = br[0] - tl[0]
                                height = br[1] - tl[1]
                                radius = int(max(width, height) / 2 * 1.2) # slightly larger
                                
                                # Draw red circle
                                cv2.circle(output_image, (center_x, center_y), radius, (0, 0, 255), 5)
                        
                        st.divider()
                        st.write(f"**ファイル名: {uploaded_file.name}**")
                        
                        if found:
                            st.success(f"数字 '{target_number}' が見つかりました！")
                            output_image_rgb = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
                            st.image(output_image_rgb, caption='結果', use_container_width=True)
                        else:
                            st.warning(f"数字 '{target_number}' は見つかりませんでした。")
                            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                            st.image(image_rgb, caption='元の画像', use_container_width=True)
