import streamlit as st
import math

st.set_page_config(page_title="進数変換アプリ", layout="wide")

st.title("進数変換アプリ")

col1, col2 = st.columns(2)

with col1:
    decimal_input = st.number_input("10進数の数値を入力してください", min_value=0, value=10, step=1)
    base_options = ["2進数", "8進数", "16進数", "n進数"]
    selected_base = st.selectbox("変換する進数を選択してください", base_options)

    if selected_base == "n進数":
        n_base = st.number_input("nの値を入力してください", min_value=2, max_value=36, value=3, step=1)
    else:
        n_base = {"2進数": 2, "8進数": 8, "16進数": 16}[selected_base]

with col2:
    if st.button("変換"):
        if decimal_input == 0:
            st.write(f"{decimal_input}を{n_base}進数に変換すると: 0")
        else:
            digits = []
            temp = decimal_input
            while temp > 0:
                digits.append(temp % n_base)
                temp //= n_base

            digits.reverse()

            max_power = len(digits) - 1
            
            st.subheader("位取り記数法の表")
            
            headers = [f"{n_base}^{i}" for i in range(max_power, -1, -1)]
            values = [n_base ** i for i in range(max_power, -1, -1)]
            digits_row = digits

            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("指数")
                st.write("\n".join(map(str, headers)))
            with col2:
                st.write("値")
                st.write("\n".join(map(str, values)))
            with col3:
                st.write("桁")
                st.write("\n".join(map(str, digits_row)))

            st.subheader("計算式")
            terms = [f"{n_base}^{max_power-i}" for i, digit in enumerate(digits) if digit != 0]
            equation = f"{decimal_input} = {' + '.join(terms)}"
            st.write(equation)

            st.subheader("結果")
            if n_base <= 10:
                result = "".join(map(str, digits))
            else:
                def to_base_n(num):
                    if num < 10:
                        return str(num)
                    return chr(ord('A') + num - 10)
                result = "".join(to_base_n(d) for d in digits)
            
            st.write(f"{decimal_input}を{n_base}進数に変換すると: {result}")

    st.info("このアプリは、10進数を2進数、8進数、16進数、またはn進数に変換し、位取り記数法の表と計算式を表示します。")

st.sidebar.header("使い方")
st.sidebar.markdown("""
1. 10進数の数値を入力します。
2. 変換したい進数を選択します。
3. 「n進数」を選んだ場合は、nの値を入力します。
4. 「変換」ボタンをクリックします。
5. 結果、位取り記数法の表、計算式が表示されます。
""")

st.sidebar.header("進数について")
st.sidebar.markdown("""
- 2進数: コンピューターの基本的な数体系
- 8進数: UNIXのファイル権限などで使用
- 16進数: カラーコード、メモリアドレスなどで使用
- n進数: 任意の基数での表現が可能
""")