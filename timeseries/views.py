import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse

def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        try:
            # CSVファイルを読み込む
            df = pd.read_csv(csv_file, encoding='shift-jis')  # または適切なエンコーディング
            
            # 日付列を日時型に変換
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            if df['Date'].isnull().all():
                return HttpResponse("日付データが正しくありません。")
            
        except pd.errors.EmptyDataError:
            return HttpResponse("CSVファイルにデータが含まれていません。")
        except UnicodeDecodeError:
            return HttpResponse("エンコーディングエラーが発生しました。別のエンコーディングでファイルをアップロードしてください。")
        
        # データが空でないか確認
        if df.empty:
            return HttpResponse("アップロードされたファイルは空です。別のファイルをアップロードしてください。")
        
        df = df.dropna(subset=['Date'])  # 日付がNaTの行を削除
        df = df.sort_values('Date')

        # グラフ作成
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['Ra'], marker='o', label='Ra')

        # カテゴリデータの表示（log列がNaNでない場合のみ表示）
        for index, row in df.iterrows():
            if pd.notna(row['log']):
                plt.text(row['Date'], row['Ra'], row['log'], fontsize=9, ha='right')

        plt.xlabel('Date')
        plt.ylabel('Ra')
        plt.title('Ra Time Series')
        plt.legend()
        plt.grid(True)

        # グラフをバイナリストリームに保存
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        return HttpResponse(buffer, content_type='image/png')

    return render(request, 'upload.html')
