import io
import base64
from flask import Flask, render_template
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    # Example data: bu yerda haqiqiy data oling
    segments = [
        {'customer_id': 1, 'price_type_num': 3.5, 'price': 100.0, 'discount_applied_num': 5.0, 'cluster': 'A'},
        {'customer_id': 2, 'price_type_num': 2.0, 'price': 150.0, 'discount_applied_num': 10.0, 'cluster': 'B'},
        {'customer_id': 3, 'price_type_num': 4.0, 'price': 90.0, 'discount_applied_num': 7.0, 'cluster': 'A'},
        # Qo‘shimcha elementlar qo‘shing
    ]

    # Agar segments bo'sh bo'lsa, message chiqaramiz
    if not segments:
        return render_template('segments.html', message="Ma'lumotlar mavjud emas", segments=None, graph=None)

    # Grafik chizish
    clusters = [s['cluster'] for s in segments]
    prices = [s['price'] for s in segments]

    plt.figure(figsize=(6,4))
    plt.bar(clusters, prices, color='skyblue')
    plt.title('Cluster bo‘yicha o‘rtacha narx')
    plt.xlabel('Segment (Cluster)')
    plt.ylabel('O‘rtacha Price')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return render_template('segments.html', segments=segments, graph='data:image/png;base64,' + graph_url, message=None)

if __name__ == '__main__':
    app.run(debug=True)
