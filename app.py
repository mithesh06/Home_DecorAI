from flask import Flask, request, render_template, redirect, url_for, jsonify
from main import process_data


app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.js')

@app.route('/getSuggestions',methods=['POST'])
def getSuggestions():
    if request.method=='POST':
        # image_data= request.get_json('imageURL')
        # style_data= request.get_json('style')
        img_sty_Data = request.get_json()
        print(img_sty_Data)
        new_img,changes= process_data(img_sty_Data['imageURL'],img_sty_Data['style'])
        print(new_img,changes)
        data={
                "new_img":new_img,
                "changes":changes
        }
        return jsonify(data)
        

if __name__=='__main__':
    app.run(debug=True)

