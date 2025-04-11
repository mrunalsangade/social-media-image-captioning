from flask import Flask, render_template, request
import Caption_it

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        f = request.files['userfile']
        path = f"./static/{f.filename}"
        f.save(path)

        caption = Caption_it.caption_this_image(path)
        result_dic = {
            'image': path,
            'caption': caption        
        }
        return render_template("index.html", your_result=result_dic)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
