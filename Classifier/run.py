import json
import os
import logging
from flask import Flask, request
from watson_developer_cloud import VisualRecognitionV3
from watson_developer_cloud import watson_service

app = Flask(__name__, static_url_path='')
app.config['PROPAGATE_EXCEPTIONS'] = True
logging.basicConfig(level=logging.FATAL)
port = os.getenv('VCAP_APP_PORT', '5000')

# Global variables for credentials
apikey = "tO9kPWGER7OiqHqx0cXayG2jKVmh4Cf30hA-wFspbKTW"
classifier_id = 'waste_331686010'


@app.route('/api/sort', methods=['POST'])
def sort():
        images_file = request.files.get('images_file')
        visual_recognition = VisualRecognitionV3('2018-03-19',
                                                 iam_apikey=apikey)
        url_result = visual_recognition.classify(images_file=images_file,
                                                classifier_ids=["waste_331686010"]).get_result()
        if len(url_result["images"][0]["classifiers"]) < 1:
            return json.dumps(
                    {"status code": 500, "result": "Image is either not "
                        "a waste or it's too blurry, please try it again.",
                        "confident score": 0})
        list_of_result = url_result["images"][0]["classifiers"][0]["classes"]
        result_class = ''
        result_score = 0
        for result in list_of_result:
            if result["score"] >= result_score:
                result_score = result["score"]
                result_class = result["class"]
        ether = 0
        if(result_class == "Compost"):
            ether  += 2
        elif result_class == "Recycle":
            ether += 3
        else:
            ether += 1
        data = request.form.to_dict(flat=False)
        return json.dumps(
            {"status code": 200, "result": result_class,
                "confident score": result_score,"ether":ether,"i":data.get('i')})
    

# Default frontend page.
@app.route('/')
def default():
    return ''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
