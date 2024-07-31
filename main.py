from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from census import refresh_census_datasets, get_census_datasets
import json

genai.configure(api_key='AIzaSyAKeDkzd7IKby2GnOWNdeAGz4QUNxbBSIY')

model = genai.GenerativeModel('gemini-1.5-flash')


app = Flask(__name__)

# api_key = 'XXXXXXXXXX'
# client = openai.OpenAI(
#     api_key=api_key
# )
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    hypothesis = data.get('hypothesis', '')
    dataset_links = get_relevant_datasets(hypothesis)
    analysis = analyze_datasets(dataset_links, hypothesis)
    return jsonify({'result': analysis, 'datasets': dataset_links})

def get_relevant_datasets(hypothesis):
    datasets=get_census_datasets()
    system_message = "You are a data scientist identifying relevant census datasets for a hypothesis. Respond in json with a list of relevant dataset gor given hypothesis."
    prompt=system_message+f"\n\n\nWhich of these census datasets would be relevant to test this hypothesis: {hypothesis}\n\nAvailable datasets:\n {json.dumps(datasets)}"
    response = model.generate_content(prompt)
    # print(response)
    json_response = response.text.split('```json\n')[1].split('\n```')[0]
    response = json.loads(json_response)
    return response


    # base_url = "https://api.census.gov/data"
    
    # datasets = {
    #     "Population Estimates": f"{base_url}/2019/pep/population",
    #     "American Community Survey": f"{base_url}/2019/acs/acs5",
    #     "Economic Census": f"{base_url}/2017/ecnbasic",
    #     "County Business Patterns": f"{base_url}/2019/cbp",
    #     "Survey of Business Owners": f"{base_url}/2012/sbo",
    #     "Annual Survey of Manufactures": f"{base_url}/2019/asm"
    # }
    
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a data scientist identifying relevant census datasets for a hypothesis. Respond with a list of relevant dataset names, separated by commas."},
    #         {"role": "user", "content": f"Which of these census datasets would be relevant to test this hypothesis: {hypothesis}\n\nAvailable datasets: {', '.join(datasets.keys())}"}
    #     ]
    # )
    
    # relevant_datasets = [dataset.strip() for dataset in response.choices[0].message.content.split(',')]
    # return [{"name": dataset, "url": datasets[dataset]} for dataset in relevant_datasets if dataset in datasets]

def analyze_datasets(dataset_links, hypothesis):
    # dataset_info = "\n".join([f"{dataset['name']}: {dataset['url']}" for dataset in dataset_links])
    system_message = "You are a data analyst explaining how to use Census datasets to explore a hypothesis."
    prompt=system_message+f"Explain how these Census datasets could be used to explore the following hypothesis. Provide a step-by-step approach and mention specific variables or data points that would be useful.\n\nHypothesis: {hypothesis}\n\nAvailable datasets:\n{json.dumps(dataset_links, indent=2)} "

    response = model.generate_content(prompt)
    # print(response)
    return response.text
    
    
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a data analyst explaining how to use Census datasets to explore a hypothesis."},
    #         {"role": "user", "content": f"Explain how these Census datasets could be used to explore the following hypothesis. Provide a step-by-step approach and mention specific variables or data points that would be useful.\n\nHypothesis: {hypothesis}\n\nAvailable datasets:\n{dataset_info}"}
    #     ]
    # )
    # return response.choices[0].message.content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
