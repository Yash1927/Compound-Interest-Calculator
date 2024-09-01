import io
import base64

import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])

def index():
    if request.method == 'POST':
        initial = float(request.form['initial'])
        interest = float(request.form['interest'])
        contribution = float(request.form['contribution'])
        compound_type = request.form['type']
        time = int(request.form['time'])
        
        if compound_type == 'annually':
            n =1
        elif compound_type =='monthly':
            n =12
        
        total = initial * (1+interest/n)**(n*time)
        total_contributions = contribution * (((1+ interest/n)**(n*time)-1) / (interest / n))
        final_with_interest = total + total_contributions
        total_investment = initial + contribution * time *n
        difference = final_with_interest - total_investment

        amount_with_interest = []
        amount_without_interest = []
        years = list(range(time+1))

        for year in years:
            total = initial * (1+interest/n)**(n*year)
            total_contributions = contribution * (((1+ interest/n)**(n*year)-1) / (interest / n))
            total_investment = initial + contribution * year *n
            amount_with_interest.append(total+total_contributions)
            amount_without_interest.append(total_investment)

        plt.figure(figsize=(10,5))
        plt.plot(years, amount_with_interest, marker="o", label ="With Interest")
        plt.plot(years, amount_without_interest, marker="o", label ="Without Interest")
        plt.title('With Interest Compound VS Without Interest')
        plt.xlabel('Years')
        plt.ylabel('Amount')
        plt.grid(True) 
        plt.legend()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template('result.html', final = final_with_interest, difference= difference, plot_url=plot_url)

    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)