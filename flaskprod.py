import json
from fabric_func import os
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import fabric_func


app = Flask(__name__)
api = Api(app)

if 'retailers' not in [f for f in os.listdir(os.path.dirname(os.path.abspath(__file__))) if os.path.isdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), f))]:
    os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'retailers'))
retailer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'retailers')
print(retailer_path)



def fun():
    info = {
        '': {
            'GET': {
                'description': 'Get all main sub directories and available requests',
            },
        },
        'retailers':
            {'methods':
                {
                    'GET': {
                        'description': 'Get all retailers and their json instructions',
                    },
                    '/retailers/<name>': {
                        'GET without parameters': {
                            'description': 'Get retailer and Json instructions',
                        },
                        'GET with parameters': {
                            'description': 'Get fabric composition of product from retailer',
                            'parameters': {
                                'url': 'string',
                            },
                        },
                        'POST': {
                            'description': 'Add new retailer and Json instructions',
                            'parameters': {
                                'json_instructions': 'json',
                            },
                        },
                        'DELETE': {
                            'description': 'Delete existing retailer and Json instructions',
                        },
                    },
                },
                'retailers':
                    {i:
                        json.load(
                            open(os.path.join(retailer_path, i, 'scrape.json'))) for
                        i in
                        os.listdir(retailer_path)}
             },
    }
    return jsonify(info)


@app.route('/')
def getmain():
    return jsonify(fun().get_json())


@app.route('/<name>')
def getsub(name=''):
    print(name)
    print(fun(), type(fun()))
    info = fun().get_json()
    print(info, type(info), info.keys(), name)
    if name in list(info.keys()):
        return jsonify(info[name])
    return '', 400


@app.route('/retailers/<retailer>', methods=['GET'])
def retailersget(retailer=''):
    print(retailer)
    parameters = request.get_json()
    rpath = os.path.join(retailer_path, retailer)
    if os.path.isdir(rpath):
        if parameters == None:
            return jsonify(
                {'retailer': retailer, 'json_instructions': json.load(open(os.path.join(rpath, 'scrape.json')))})
        return fabric_func.scrap(retailer, parameters['url'])
    return 'Retailer does not exist', 400


# for i in list(info.keys()):
#     @app.route(i)
#     def temp():
#         return jsonify(info[i])
#     # eval(f'def {i[1:]}a():return jsonify(info["{i}"])')
@app.route('/retailers/<retailer>', methods=['POST'])
def retailerspost(retailer=''):
    parameters = request.get_json()
    rpath = os.path.join(retailer_path, retailer)
    if os.path.isdir(os.path.join(rpath)):
        return 'Retailer already exists', 400
    os.mkdir(rpath)
    with open(os.path.join(rpath, 'scrape.json'), 'w', encoding='utf-8') as f:
        json.dump(parameters, f, ensure_ascii=False)
    return 'Success', 204


@app.route('/retailers/<retailer>', methods=['DELETE'])
def retailersdelete(retailer=''):
    rpath = os.path.join(retailer_path, retailer)
    if os.path.isdir(os.path.join(rpath)):
        os.remove(os.path.join(rpath, 'scrape.json'))
        os.rmdir(rpath)
        return '', 204
    return 'Retailer does not exist', 400


# @app.route('/retailers/<retailer>/<url>', methods=['GET'])
# def retailersurlget(retailer='', url=''):
#     parameters = request.get_json()
#     rpath = os.path.join(retailer_path, retailer)
#     if os.path.isdir(os.path.join(rpath)):
#         return fabric_func.scrap(retailer, url)
#     return 'Retailer does not exist', 400


# @app.route('/fabric', methods=['GET'])
# def exceute_command():
#     print(request.get_json())
#     x = request.get_json()
#     fabric_parameters = info['/fabric']['GET']['parameters']
#     if x.keys() == fabric_parameters.keys():
#         return fabric_func.scrap(x[list(fabric_parameters.keys())[0]], x[list(fabric_parameters.keys())[1]]), 200
#     return 'bad request', 400
# case 'addretailer':
#     params = x[1]
#     newdir = os.path.join(retailer_path, params[0])
#     if os.path.isdir(newdir):
#         return 'Retailer exists, try updating with PUT request', 204
#     os.mkdir(newdir)
#     with open(f'{newdir}\\scrape.json', 'w', encoding='utf-8') as f:
#         json.dump(params[1], f, ensure_ascii=False)
#     print(params[1])
#     return '', 204
# case default:
#     return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0')  # run our Flask app
# curl -X POST -H "Content-Type: application/json" -d '["getfabric","https://www.terminalx.com/catalog/product/view/id/810153/s/x976060017/","terminalx"]' http://localhost:5000/fabric
