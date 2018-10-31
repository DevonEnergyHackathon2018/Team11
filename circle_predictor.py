import requests
import os
import time

def upload_circle(api_url, api_key, path):
    """uploads the circle imager to the vision API"""
    headers = {"Prediction-Key": api_key, "Content-Type": "multipart/form-data"}
    img_data = open(path,'rb')
    print(api_url)
    resp = requests.post(url=api_url, headers=headers, data=img_data)
    print(resp)

    if resp.status_code == 200:
        return resp.json()
    else:
        return {}

def predict_circles(api_url, api_key,circles_folder):
    """gets predictions based on the folder of circles"""
    results = {}
    for filename in os.listdir(circles_folder):
        if filename.startswith('circle'):
            full_path_to_file = "%s/%s" % (circles_folder, filename)
            results[filename] = upload_circle(api_url, api_key,full_path_to_file)
            time.sleep(0.7)
    return results

def interpret_results(filename, probs):
    results = {}
    for circle in probs:
        prob = 0
        if 'predictions' in probs[circle]:
            for cpred in probs[circle]['predictions']:
                if not cpred['tagName'] == "NOT":
                    if cpred['probability'] > prob:
                        results[circle] = int(cpred['tagName'])
                        prob = cpred['probability']  
    rsum = 0
    count=0
    rmax = 0
    for res in results.values():
        rsum +=res
        count+=1
        if res > rmax:
            rmax = res
    mean = rsum/count
    print(filename, mean, count, rmax)
    message = ""
    if count > 15:
        message = {"message":"%s is suffering from data quality issues - can't have a total of (%d)" % (filename, count),"colour":"800080"}
    else:
        if mean < 3:
            message = {"message":"%s is within nominal values (%d)" % (filename, round(mean)),"colour":"009933"}
        elif mean < 5:
            message = {"message":"%s is getting worn down (%d)" % (filename, round(mean)),"colour":"ffcc00"}
        else:
             message = {"message":"%s needs replacing (%d)" % (filename, round(mean)),"colour":"b30000"}
    return message