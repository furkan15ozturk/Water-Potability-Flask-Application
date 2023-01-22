from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf

app = Flask(__name__)

formData = {}


def prediction(ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity):
    model = tf.keras.models.load_model("potability.model")
    pred = model.predict([[ph, hardness, solids, chloramines,
                           sulfate, conductivity, organic_carbon,
                           trihalomethanes, turbidity]])

    return check_potability(pred)


def check_potability(pred):
    if pred > 0.5:
        return "drinkable."
    else:
        return "not drinkable."


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        ph = request.form['ph']
        hardness = request.form['hardness']
        solids = request.form['solids']
        chloramines = request.form['chloramines']
        sulfate = request.form['sulfate']
        conductivity = request.form['conductivity']
        organic_carbon = request.form['organic-carbon']
        trihalomethanes = request.form['trihalomethanes']
        turbidity = request.form['turbidity']
        formData['ph'] = ph
        formData['hardness'] = hardness
        formData['solids'] = solids
        formData['chloramines'] = chloramines
        formData['sulfate'] = sulfate
        formData['conductivity'] = conductivity
        formData['organic-carbon'] = organic_carbon
        formData['trihalomethanes'] = trihalomethanes
        formData['turbidity'] = turbidity
        return redirect(url_for('output'))
    else:
        return render_template("index.html", title="Potability Check")


@app.route("/output")
def output():
    predict = prediction(formData['ph'], formData['hardness'], formData['solids'],
                         formData['chloramines'], formData['sulfate'], formData['conductivity'],
                         formData['organic-carbon'], formData['trihalomethanes'], formData['turbidity'])
    return render_template('output.html', title='Potability', pot=formData['turbidity'])


if __name__ == '__main__':
    app.run()
