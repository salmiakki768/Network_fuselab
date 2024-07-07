import streamlit as st


def main():
    # タイトル表示
    st.title('タイトル表示')
    # ヘッダー表示
    st.header('ヘッダー表示')
    # テキスト表示
    st.text('テキスト表示')
    # サブレベルヘッダー表示
    st.subheader('ブレベルヘッダー表示')
    # マークダウンテキスト表示
    st.markdown('**マークダウンテキスト表示 **')
    # LaTeX テキスト表示
    st.latex(r'\bar{X} = \frac{1}{N} \sum_{n=10}^{N} x_i')
    # コードスニペット表示
    st.code('print(\'code snippets ! \')')
    # エラーメッセージ表示
    st.error('エラーメッセージ表示')
    # 警告メッセージ表示
    st.warning('警告メッセージ表示')
    # インフォメッセージ表示
    st.info('インフォメッセージ表示')
    # 成功メッセージ表示
    st.success('成功メッセージ表示')
    # 例外表示
    st.exception(Exception('例外表示'))
    # 辞書の出力
    data = {'アプリ名': 'streamlitサンプル',
            'ユーザー': ['otupy', 'okkun', ], }
    st.json(data)


if __name__ == '__main__':
    main()