#!/usr/bin/env python3


from flask import Flask, request
import pandas as pd
from utils.balance_data import balance_data
from utils.common import read_json_time_series, response_message, convert_date_to_shamsi, convert_json_to_df, \
    get_requests_and_convert_to_json
from utils.interpolation_methods import linear_interpolation
from utils.detect_outlier import detect_outlier
from utils.manage_data import clean_data
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


@app.route("/", methods=["GET", "POST"])
def check_service():
    """this is a test for checking if project is up or not
    This is using docstrings for specifications.
    ---
    parameters:
        - name: status_checker
          required: false

    responses:
        200:
          description: server is working

    """
    return "service is working , hello there XD, thank you for all the things you did for us <3, it was wonderful."


@app.route("/service1", methods=["GET", "POST"])
def service1():
    """ this is first service for linear interpolation
      interpolate data in Daily/Monthly and return in miladi.
      ---
      tags:
      - service1
      summary: interpolate data
      produces:
      - "application/json"

      parameters:
      - in: "body"
        name: "body"
        description: "data given for interpolate in daily or monthly, input and output sample will be given in input folder for each service."
        required: true
        schema:
          $ref: "#/definitions/model1"
      definitions:
        model1:
          type: object
          properties:
            data:
              type: object
              items: timeseries
            config:
              type: object

        daily/monthly:
          type:string

        interpolation:
          type:string

        output_1:
          type: object
          properties:
            data:
              type: object
              items: timeseries

      responses:
        "200":
          description: "successful operation"
          schema:
            $ref: "#/definitions/output_1"
        "400":
          description: "Invalid model"

      """
    data, req = get_requests_and_convert_to_json()
    config = req["config"]

    if config["type"] == "miladi":
        result = linear_interpolation(data, config)
        result = result.to_json()
        return response_message(dict({"data": result}))


@app.route("/service2", methods=["GET", "POST"])
def service2():
    """ this is second service for linear interpolation
          interpolate data in Daily/Monthly and return results in shamsi.
          ---
          tags:
          - service2
          summary: interpolate data return shamsi
          produces:
          - "application/json"

          parameters:
          - in: "body"
            name: "body"
            description: "data given for interpolate in daily or monthly , skip holiday feature is not implemented, input and output sample will be given in input folder for each service."
            required: true
            schema:
              $ref: "#/definitions/model1"
          definitions:
            model1:
              type: object
              properties:
                data:
                  type: object
                  items: timeseries
                config:
                  type: object

            daily/monthly:
              type:string

            interpolation:
              type:string

            output_1:
              type: object
              properties:
                data:
                  type: object
                  items: timeseries

          responses:
            "200":
              description: "successful operation"
              schema:
                $ref: "#/definitions/output_1"
            "400":
              description: "Invalid model"

          """

    data, req = get_requests_and_convert_to_json()

    config = req["config"]

    if config["interpolation"] == "linear":
        result = linear_interpolation(data, config)
        result_shamsi = convert_date_to_shamsi(result)
        result_shamsi = result_shamsi.to_json(default_handler=str)
        return response_message(dict({"data": result_shamsi}))


@app.route("/service3", methods=["GET", "POST"])
def service3():
    """ this is third service for outlier detection
              detect outlier with 3 methods, mean, IQR, zstat.
              ---
              tags:
              - service3
              summary: outlier detection
              produces:
              - "application/json"

              parameters:
              - in: "body"
                name: "body"
                description: "data given for outlier detection, service can get panda df with any number of features, input and output sample will be given in input folder for each service."
                required: true
                schema:
                  $ref: "#/definitions/model3"
              definitions:
                model3:
                  type: object
                  properties:
                    data:
                      type: object
                      items: feature/vol
                    config:
                      type: Boolean
                feature/vol:
                  type:int

                daily/monthly:
                  type:string

                interpolation:
                  type:string

                output_3:
                  type: object
                  properties:
                    data:
                      type: object
                      items: method_n

                method_n:
                  type: Boolean


              responses:
                "200":
                  description: "successful operation, data will be return as a df for all methods "
                  schema:
                    $ref: "#/definitions/output_3"
                "400":
                  description: "Invalid model"

              """

    req = request.get_json()
    data = req["data"]

    config = req["config"]
    if config["time_series"]:
        data = read_json_time_series(req["data"])
        result = detect_outlier(data, True)
    else:
        data = convert_json_to_df(data)
        result = detect_outlier(data, False)
    result = result.to_json(default_handler=str)
    return response_message(dict({"data": result}))


@app.route("/service4", methods=["GET", "POST"])
def service4():

    """ this is forth service for manage imbalance data
                  manage imbalance data with 3method oversampling , undersampling , SMOTE( require min 6 sample for each class).
                  ---
                  tags:
                  - service4
                  summary: imbalance data
                  produces:
                  - "application/json"

                  parameters:
                  - in: "body"
                    name: "body"
                    description: "manage imbalance data with 3method , SMOTE (each class must have at least 6 sample), input and output sample will be given in input folder for each service."
                    required: true
                    schema:
                      $ref: "#/definitions/model4"
                  definitions:
                    model4:
                      type: object
                      properties:
                        data:
                          type: object
                          items: timeseries
                        config:
                          type: object

                    daily/monthly:
                      type:string

                    interpolation:
                      type:string

                    output_4:
                      type: object
                      properties:
                        data:
                          type: object
                          items: int

                  responses:
                    "200":
                      description: "successful operation"
                      schema:
                        $ref: "#/definitions/output_4"
                    "400":
                      description: "Invalid model"

                  """

    req = request.get_json()
    data = req["data"]
    data = convert_json_to_df(data)
    data, classes, col = clean_data(data)
    config = req["config"]
    x, y = balance_data(data, config, classes)
    if type(y) == str:
        return response_message(x)
    df = pd.DataFrame(x, columns=col)
    y = pd.Series(y)
    df['class'] = y
    result = df.to_json(default_handler=str)
    return response_message(dict({"data": result}))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
