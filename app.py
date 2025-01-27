#from cgitb import text
from flask import Flask,render_template,request
import model as model 
app = Flask('__name__')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend',methods=['POST'])
def recommend_top5():
    print(request.method)
    user_name = request.form['User Name']
    print('User name=',user_name)
    
    if  request.method == 'POST':
        get_top5 = model.recommend_top5_products(user_name)
        print(get_top5.head())
        return render_template('index.html',column_names=get_top5.columns.values, row_data=list(get_top5.values.tolist()), zip=zip,text='Recommended products')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.debug=False

    app.run()