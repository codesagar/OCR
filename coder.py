# Thanks to HP for providing IDOL OnDemand APIs
# HP IDOL OnDemand APIs used: OCR Document, Store Object(not shown here)
# Created in Angelhack Delhi 2015. 20-21 June 2015 

from flask import Flask, request, Response, render_template, jsonify
import requests, json


app = Flask(__name__)

@app.route('/ocr')
def ocr():
	"""
		Raw file(.jpg or .pdf) processed via Store Object API, reference of which is read by a synchronous GET request to example.example/ocr?ref=&apikey=
		Returns json of the read and edited text containing two arrays (key and value).
	"""
    ref = request.args.get('ref')
    apikey = request.args.get('apikey')

    # return redirect('https://api.idolondemand.com/1/api/sync/ocrdocument/v1?reference='+ref+'&apikey='+apikey)
    payload = {'apikey': apikey, 'reference': ref}
    r = requests.get('http://api.idolondemand.com/1/api/sync/ocrdocument/v1', params=payload)
    text=str(r.text)
    
	# Filtering the OCRed text to something readable.
	# Store the text after encountering the word 'range' which becomes key. # Store the text after encountering '\' (in '\n') which becomes value.
	count=0
    cnt=0
    ct=15
    v1=0
    v2=0
    for i in range(0, len(text)-4):
        if text[i]=="R" or text[i]=="r":
            if text[i+1]=="A" or text[i+1]=="a":
                if text[i+2]=="N" or text[i+2]=="n":
                    if text[i+3]=="G" or text[i+3]=="g":
                        if text[i+4]=="E" or text[i+4]=="e":
                            count=i
                            cnt=i
                            break
    start=0
    end=0
    keyarray=[]
    valarray=[]
    # for j in range(count, len(text)):
    #     print(text[j],end="")
    while ct>0:
        key = []
        value = []
        while ord(str(text[cnt])) != 92:
            cnt += 1
        start=cnt+2
        while ord(str(text[cnt])) > 58 or ord(str(text[cnt])) < 47:
            cnt += 1
        end=cnt
        for t in range(start, end):
            key.append(text[t])
        v1=cnt
        while ord(str(text[cnt])) != 32:
            cnt +=1
        v2=cnt+1
        for t in range(v1, v2):
            value.append(text[t])
        ct -=1
        keyarray.append("".join(map(str, key)))
        valarray.append("".join(map(str, value)))
    # print(keyarray)
    # print(valarray)
    js = [{'keyarray': keyarray,
           'valarray': valarray}]
    return Response(json.dumps(js),  mimetype='application/json')

if __name__ == '__main__':
	"""
	local server used here.
	"""
    app.run(host="127.0.0.1", debug=True)
