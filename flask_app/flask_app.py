from flask import Flask, render_template_string
from view_data import ViewData

app = Flask(__name__)

@app.route("/")
def show_table():
    view_data = ViewData()
    rows = view_data.fetch_table()
    view_data.close()

    if not rows:
        return "No any result"

    html = '''
    <h1>TITANIC Column (Limit 20 )</h1>
    <table border="1">
        <tr>
            {% for key in rows[0].keys() %}
            <th>{{ key }}</th>
            {% endfor %}
        </tr>
        {% for row in rows %}
        <tr>
            {% for item in row.values() %}
            <td>{{ item }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
    '''
    return render_template_string(html, rows=rows)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
