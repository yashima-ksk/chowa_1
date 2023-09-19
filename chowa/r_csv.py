import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")

@st.cache_data
def load_csv(file_path):
    return pd.read_csv(file_path, encoding='shift_jis')

csv_dir = r'D:\CMS#002'
csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

# ページの選択
page = st.sidebar.radio("ページの選択", ["CSVファイルの選択", "データの分析", "Ambient"])

if page == "CSVファイルの選択":
    st.header("ファイルの選択")
    st.write("表の列をクリックすると昇降します")
    st.write("表示したいファイルを選択して一番下の解析ボタンを押し、データ分析タブに移動してください")
    # 各CSVファイルの名前と更新日時を取得して、表として表示
    file_info = [{"name": f, "last_modified": os.path.getmtime(os.path.join(csv_dir, f))} for f in csv_files]
    file_df = pd.DataFrame(file_info)
    file_df['last_modified'] = pd.to_datetime(file_df['last_modified'], unit='s')  # UNIX時間を日時に変換
    st.write(file_df.sort_values(by="last_modified", ascending=False))  # 日時でソートして表示

    # ここをselectboxから表のname列で選択するように修正
    selected_file = st.radio("CSVファイルを選択", file_df['name'].tolist())
    if st.button("選択したファイルで分析"):
        st.session_state.selected_file = selected_file
        page = "データの分析"

if page == "データの分析":
    if 'selected_file' in st.session_state:
        st.write("表示させたいグラフを選んでください、複数選択可能です")
        st.write("先ほど選んだグラフの横軸の選択")
        file_path = os.path.join(csv_dir, st.session_state.selected_file)
        df = load_csv(file_path)
        st.write(df)

        columns = st.multiselect("表示するカラムを選択", df.select_dtypes(include=['number']).columns)
        index_col = st.selectbox("インデックスとして使用するカラムを選択", df.columns)
        for col in columns:
            if col != index_col:
                st.subheader(f"グラフ: {col} vs {index_col}")
                y_min = st.number_input(f"{col} の y軸の最小値", float(df[col].min()), float(df[col].max()))
                y_max = st.number_input(f"{col} の y軸の最大値", float(df[col].min()), float(df[col].max()))
                fig = px.line(df, x=index_col, y=col)
                fig.update_layout(yaxis_range=[y_min, y_max])
                st.plotly_chart(fig)
