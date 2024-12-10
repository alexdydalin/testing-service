import os
import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

# Load the pre-trained model
model = load_model('gherkin_to_cucumber_model.h5')

# Initialize tokenizers (you should load these based on your training setup)
gherkin_tokenizer = Tokenizer(num_words=1000)
cucumber_tokenizer = Tokenizer()  # Load this with your actual vocabulary

# Function to prepare input for prediction
def prepare_input(gherkin_text):
    sequence = gherkin_tokenizer.texts_to_sequences([gherkin_text])
    padded_sequence = pad_sequences(sequence, maxlen=20)  # Use your max_sequence_length
    return padded_sequence

# Route to serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint to upload Gherkin file and generate Cucumber Java code
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        gherkin_text = file.read().decode('utf-8')
        input_data = prepare_input(gherkin_text)
        prediction = model.predict(input_data)
        predicted_sequence = np.argmax(prediction, axis=-1)
        cucumber_code = decode_output(predicted_sequence)
        print('Это код: ', cucumber_code)
        return jsonify({'cucumber_java': cucumber_code})

def decode_output(predicted_sequence):
    return ' '.join([cucumber_tokenizer.index_word.get(idx, '') for idx in predicted_sequence[0]])

@app.route('/upload-file', methods=["GET", "POST"])
def uploadFile():
  if request.method == "POST":
    file = request.files['file']
    expansion = 'None'
    match expansion:
      case ".feature":  # расширение файла Ghiirkin
        pass
      case ".txt":
        pass
    if 'file' not in request.files:
      return { "success": False, "message": "Не удалось счиатать файл" }, 400
    file_content = file.read('./test1.txt').decode('utf-8')
    processed_file = file_content.split('###')
    if "Функция" in file_content:
      pass
    if "Предыстория" in file_content:
      pass
    if "Сценарий" in file_content:
      pass
  return 1
@app.route("/predict")
def predict():
  model = None # load_model('имя_модели.h5')
  data = request.get_json(force=True)
  prediction = None #model.predict(X)
  response = { "prediction": prediction.tolist() }
  return jsonify(response)
@app.route('/process')
def process():
  data = request.get_json()
  try:
    return { "success": True, "message": "Файл успешно загружен" }, 200
  except:
    return { "success": False, "message": "Не удалось загрузить файл" }, 400
@app.route('/process')
def process():
  data = request.get_json()
  response = {
    "status": "success",
    "message": "Data received successfully!"
  }
  return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)