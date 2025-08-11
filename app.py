import streamlit as st
import random
import unicodedata

# Hàm bỏ dấu và chuẩn hóa chữ
def normalize_text(text):
    text = text.strip().lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')  # bỏ dấu
    return text

st.title("📚 Luyện từ vựng tiếng Anh - Điền từ từ nghĩa")

# Trạng thái ban đầu
if "stage" not in st.session_state:
    st.session_state.stage = "input"
if "vocab_list" not in st.session_state:
    st.session_state.vocab_list = []
if "unused_words" not in st.session_state:
    st.session_state.unused_words = []
if "current_word" not in st.session_state:
    st.session_state.current_word = None
if "score" not in st.session_state:
    st.session_state.score = 0

# Giao diện nhập từ vựng
if st.session_state.stage == "input":
    st.subheader("Nhập danh sách từ vựng")
    vocab_input = st.text_area(
        "Nhập từ vựng (mỗi dòng: tiếng_Anh - nghĩa_Tiếng_Việt)",
        placeholder="Ví dụ:\nflexible - linh hoạt\norganised - ngăn nắp"
    )

    if st.button("Bắt đầu học"):
        lines = vocab_input.strip().split("\n")
        vocab_list = []
        for line in lines:
            if "-" in line:
                eng, viet = line.split("-", 1)
                vocab_list.append({"word": eng.strip(), "meaning": viet.strip()})
        if vocab_list:
            st.session_state.vocab_list = vocab_list
            st.session_state.unused_words = vocab_list.copy()
            st.session_state.score = 0
            st.session_state.stage = "learn"
            st.session_state.current_word = random.choice(st.session_state.unused_words)
            st.session_state.unused_words.remove(st.session_state.current_word)
            st.rerun()

# Giao diện học
elif st.session_state.stage == "learn":
    st.write(f"Nghĩa tiếng Việt: **{st.session_state.current_word['meaning']}**")
    user_word = st.text_input("Nhập từ tiếng Anh:")

    if st.button("Kiểm tra"):
        correct_word = st.session_state.current_word["word"]

        if normalize_text(user_word) == normalize_text(correct_word):
            st.success("✅ Chính xác!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Sai! Đúng là: **{correct_word}**")

    if st.button("Từ tiếp theo"):
        if st.session_state.unused_words:
            # Lấy từ mới từ danh sách chưa dùng
            st.session_state.current_word = random.choice(st.session_state.unused_words)
            st.session_state.unused_words.remove(st.session_state.current_word)
        else:
            # Nếu hết từ -> reset vòng mới
            st.session_state.unused_words = st.session_state.vocab_list.copy()
            st.session_state.current_word = random.choice(st.session_state.unused_words)
            st.session_state.unused_words.remove(st.session_state.current_word)
            st.info("🔄 Hoàn thành một vòng! Bắt đầu vòng mới.")
        st.rerun()

    if st.button("Quay lại nhập từ mới"):
        st.session_state.stage = "input"
        st.rerun()

    st.write(f"Điểm: **{st.session_state.score}**")
