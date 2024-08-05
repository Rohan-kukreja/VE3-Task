import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend for non-GUI environments
import matplotlib.pyplot as plt
import seaborn as sns
import io
import urllib, base64
import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            df = pd.read_csv(csv_file)
            
            # Data analysis
            data_head = df.head().to_html()
            summary_stats = df.describe().to_html()
            
            # Data visualization
            fig, ax = plt.subplots()
            sns.histplot(df.select_dtypes(include=['number']), kde=True, ax=ax)
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            
            context = {
                'data_head': data_head,
                'summary_stats': summary_stats,
                'plot': uri
            }
            return render(request, 'csvapp/results.html', context)
    else:
        form = UploadFileForm()
    return render(request, 'csvapp/upload.html', {'form': form})
