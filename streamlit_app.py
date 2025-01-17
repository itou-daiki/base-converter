import streamlit as st
import math
import traceback

st.set_page_config(page_title="進数変換学習アプリ")

st.title("進数変換学習アプリ")
st.caption("Created by Dit-Lab.(Daiki Ito)")

# Introduction
st.markdown("""
## **概要**
このウェブアプリケーションは、10進数からn進数の変換の学習を補助します。  
表の描画、エラー処理、コピー機能を追加したサンプル実装です。
""")

decimal_input = st.number_input("10進数の数値を入力してください", min_value=0, value=62, step=1)
base_options = ["2進数", "8進数", "16進数", "n進数"]
selected_base = st.selectbox("変換する進数を選択してください", base_options)

if selected_base == "n進数":
    n_base = st.number_input("nの値を入力してください", min_value=2, max_value=36, value=3, step=1)
else:
    n_base = {"2進数": 2, "8進数": 8, "16進数": 16}[selected_base]

def decimal_to_binary(decimal_num):
    return bin(decimal_num)[2:]

def binary_to_octal(binary):
    return oct(int(binary, 2))[2:]

def binary_to_hexadecimal(binary):
    return hex(int(binary, 2))[2:].upper()

def group_binary(binary_str, group_size):
    """binary_strをgroup_size桁ごとに空白区切り文字列に変換"""
    return ' '.join([binary_str[max(i - group_size, 0):i]
                     for i in range(len(binary_str), 0, -group_size)][::-1])

def binary_group_to_decimal(binary_group):
    """2進数の塊(binary_group)を10進数に変換して文字列で返す"""
    return str(int(binary_group, 2))

try:
    # 変換処理
    if decimal_input == 0:
        # 0の場合は変換結果も「0」になる
        st.write(f"{decimal_input}を{n_base}進数に変換すると: 0")
        result = "0"
    else:
        # まず2進数に変換
        binary = decimal_to_binary(decimal_input)

        if selected_base in ["8進数", "16進数"]:
            st.subheader("変換過程")
            st.write(f"1. 10進数を2進数に変換: {decimal_input} → {binary}")

            # 8進数(3bit区切り) or 16進数(4bit区切り)
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
            # 2進数 or n進数(2~36)
            digits = []
            temp = decimal_input
            while temp > 0:
                digits.append(temp % n_base)
                temp //= n_base
            digits.reverse()  # 上位桁が先頭になるように反転

            max_power = len(digits) - 1

            st.subheader("位取り記数法の表")
            # ここでインデントを減らしてMarkdown表が正しく描画されるようにする
            # 行頭に余計なスペースを入れずに記述
            markdown_table = f"""|      | {' | '.join([f"$${n_base}^{{{i}}}$$" for i in range(max_power, -1, -1)])} |
|------|{'|---' * (max_power + 1)}|
| 値   | {' | '.join(str(n_base ** i) for i in range(max_power, -1, -1))} |
| 桁   | {' | '.join(str(d) for d in digits)} |
"""
            st.markdown(markdown_table)

            st.subheader("計算式")
            # 桁が0でないところだけを項にする
            terms = [f"{n_base}^{{{max_power - i}}} \\times {digits[i]}" 
                     for i in range(len(digits)) if digits[i] != 0]
            equation = f"$${decimal_input} = {' + '.join(terms)}$$"
            st.markdown(equation)

            # nが10を超える場合(11～36進)はアルファベットを使う
            if n_base <= 10:
                result = "".join(map(str, digits))
            else:
                def to_base_n(num):
                    return str(num) if num < 10 else chr(ord('A') + num - 10)
                result = "".join(to_base_n(d) for d in digits)

    # 結果表示
    st.subheader("結果")
    centered_result = f"""
<div style="display: flex; justify-content: center; align-items: center; height: 50px;">
    <p style="font-size: 18px; font-weight: bold;">
        {decimal_input}を{selected_base}に変換すると: {result}
    </p>
</div>
"""
    st.markdown(centered_result, unsafe_allow_html=True)

    # コピー用ボタンを追加
    if st.button("結果をコピー"):
        # Streamlitには直接クリップボード機能はないので、ユーザがコピーしやすいようにテキスト表示
        st.write("以下を手動でコピーしてください:")
        st.code(result)

except Exception as e:
    st.warning("基数変換に失敗しました。入力値やnの値を確認してください。")
    # デバッグ用に詳細を表示したい場合は以下のコメントアウトを外してください
    # st.error(traceback.format_exc())

st.markdown("""
---
## 使い方
1. 10進数の数値を入力します。  
2. 変換したい進数を選択します。  
3. 「n進数」を選んだ場合は、nの値を入力します。  
4. 結果、位取り記数法の表、計算式、コピー用ボタンが自動的に表示されます。

## 進数について
- 2進数: コンピューターの基本的な数体系
- 8進数: UNIXのファイル権限などで使用
- 16進数: カラーコード、メモリアドレスなどで使用
- n進数: 任意の基数での表現が可能
---
""")

# Copyright
st.subheader('© 2022-2024 Dit-Lab.(Daiki Ito). All Rights Reserved.')
