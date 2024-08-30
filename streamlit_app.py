import streamlit as st
import math

st.set_page_config(page_title="進数変換アプリ", layout="wide")

st.title("進数変換アプリ")

decimal_input = st.number_input("10進数の数値を入力してください", min_value=0, value=44, step=1)
base_options = ["2進数", "8進数", "16進数", "n進数"]
selected_base = st.selectbox("変換する進数を選択してください", base_options)

if selected_base == "n進数":
    n_base = st.number_input("nの値を入力してください", min_value=2, max_value=36, value=3, step=1)
else:
    n_base = {"2進数": 2, "8進数": 8, "16進数": 16}[selected_base]

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
    
    # Markdownテーブルを作成
    markdown_table = f"""
| | {" | ".join([f"$${n_base}^{{{i}}}$$" for i in range(max_power, -1, -1)])} |
|---|{"|---" * (max_power + 1)}|
| 値 | {" | ".join([str(n_base ** i) for i in range(max_power, -1, -1)])} |
| 桁 | {" | ".join(map(str, digits))} |
"""
    st.markdown(markdown_table)

    st.subheader("計算式")
    terms = [f"{n_base}^{{{max_power-i}}} \\times {digits[i]}" for i in range(len(digits)) if digits[i] != 0]
    equation = f"$${decimal_input} = {' + '.join(terms)}$$"
    st.markdown(equation)

    st.subheader("結果")
    if n_base <= 10:
        result = "".join(map(str, digits))
    else:
        def to_base_n(num):
            if num < 10:
                return str(num)
            return chr(ord('A') + num - 10)
        result = "".join(to_base_n(d) for d in digits)
    
    # 結果をセンタリングして表示
    centered_result = f"""
<div style="display: flex; justify-content: center; align-items: center; height: 50px;">
    <p style="font-size: 18px; font-weight: bold;">
        {decimal_input}を{n_base}進数に変換すると: {result}
    </p>
</div>
"""
    st.markdown(centered_result, unsafe_allow_html=True)

st.markdown("""
## 使い方
1. 10進数の数値を入力します。
2. 変換したい進数を選択します。
3. 「n進数」を選んだ場合は、nの値を入力します。
4. 結果、位取り記数法の表、計算式が自動的に表示されます。

## 進数について
- 2進数: コンピューターの基本的な数体系
- 8進数: UNIXのファイル権限などで使用
- 16進数: カラーコード、メモリアドレスなどで使用
- n進数: 任意の基数での表現が可能
""")