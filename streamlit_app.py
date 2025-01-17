import streamlit as st
import math
import traceback
import pandas as pd

st.set_page_config(page_title="進数変換学習アプリ")

st.title("進数変換学習アプリ")
st.caption("Created by Dit-Lab.(Daiki Ito)")

st.markdown("""
## **概要**
このウェブアプリケーションは、10進数からn進数の変換の学習を補助します。
""")

decimal_input = st.number_input("10進数の数値を入力してください", min_value=0, value=62, step=1)
base_options = ["2進数", "8進数", "16進数", "n進数"]
selected_base = st.selectbox("変換する進数を選択してください", base_options)

# ---------------------------
# n進数用の入力
# ---------------------------
if selected_base == "n進数":
    n_base = st.number_input("nの値を入力してください", min_value=2, max_value=36, value=3, step=1)
    base_label = f"{n_base}進数"  # 「4進数」「7進数」のように表示される
else:
    n_base = {"2進数": 2, "8進数": 8, "16進数": 16}[selected_base]
    base_label = selected_base  # 「2進数」「8進数」など元のまま

def decimal_to_binary(decimal_num):
    return bin(decimal_num)[2:]

def binary_to_octal(binary):
    return oct(int(binary, 2))[2:]

def binary_to_hexadecimal(binary):
    return hex(int(binary, 2))[2:].upper()

def group_binary(binary_str, group_size):
    return ' '.join([
        binary_str[max(i - group_size, 0):i]
        for i in range(len(binary_str), 0, -group_size)
    ][::-1])

def binary_group_to_decimal(binary_group):
    return str(int(binary_group, 2))

try:
    if decimal_input == 0:
        st.write(f"{decimal_input}を{base_label}に変換すると: 0")
        result = "0"
    else:
        # まず 10進数→2進数
        binary = decimal_to_binary(decimal_input)

        if selected_base in ["8進数", "16進数"]:
            st.subheader("変換過程")
            st.write(f"1. 10進数を2進数に変換: {decimal_input} → {binary}")

            group_size = 3 if selected_base == "8進数" else 4
            grouped_binary = group_binary(binary, group_size)
            st.write(f"2. 2進数を{group_size}桁ずつグループ化: {grouped_binary}")

            decimal_groups = [binary_group_to_decimal(g) for g in grouped_binary.split()]
            st.write(f"3. 各グループを10進数に変換: {' '.join(decimal_groups)}")

            # 8進数 or 16進数に変換
            if selected_base == "8進数":
                result = binary_to_octal(binary)
                st.write(f"4. 10進数を8進数に変換: {' '.join(result)}")
            else:
                result = binary_to_hexadecimal(binary)
                st.write(f"4. 10進数を16進数に変換: {' '.join(result)}")

                # 16進数変換表
                st.text("参考：16進数変換表")
                hex_table = """
| 10進数 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|--------|---|---|---|---|---|---|---|---|---|---|----|----|----|----|----|----|
| 16進数 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A  | B  | C  | D  | E  | F  |
"""
                st.markdown(hex_table)

        else:
            # n進数 (2進数含む) の処理
            digits = []
            temp = decimal_input
            while temp > 0:
                digits.append(temp % n_base)
                temp //= n_base
            digits.reverse()

            max_power = len(digits) - 1

            st.subheader("位取り記数法の表")
            columns = [f"{n_base}^{i}" for i in range(max_power, -1, -1)]
            values_str = [str(n_base**i) for i in range(max_power, -1, -1)]
            digits_str = [str(d) for d in digits]

            df = pd.DataFrame(
                [values_str, digits_str],
                index=["値", "桁"],
                columns=columns
            )
            st.table(df)

            # 計算式
            st.subheader("計算式")
            terms = [
                f"{n_base}^{{{max_power - i}}} \\times {digits[i]}"
                for i in range(len(digits)) if digits[i] != 0
            ]
            equation = f"$${decimal_input} = {' + '.join(terms)}$$"
            st.markdown(equation)

            if n_base <= 10:
                result = "".join(map(str, digits))
            else:
                def to_base_n(num):
                    return str(num) if num < 10 else chr(ord('A') + num - 10)
                result = "".join(to_base_n(d) for d in digits)

    st.subheader("結果")
    centered_result = f"""
<div style="display: flex; justify-content: center; align-items: center; height: 50px;">
    <p style="font-size: 18px; font-weight: bold;">
        {decimal_input}を{base_label}に変換すると: {result}
    </p>
</div>
"""
    st.markdown(centered_result, unsafe_allow_html=True)

except Exception as e:
    st.warning("基数変換に失敗しました。入力値やnの値を確認してください。")
    # st.error(traceback.format_exc())  # デバッグ用

st.markdown("""
## 使い方
1. 10進数の数値を入力します。  
2. 変換したい進数を選択します。  
3. 「n進数」を選んだ場合は、nの値を入力します。  
4. 結果、位取り記数法の表と計算式が自動表示されます。

## 進数について
- 2進数: コンピューターの基本的な数体系
- 8進数: UNIXのファイル権限などで使用
- 16進数: カラーコード、メモリアドレスなどで使用
- n進数: 任意の基数での表現が可能
""")

st.subheader('© 2022-2024 Dit-Lab.(Daiki Ito). All Rights Reserved.')
