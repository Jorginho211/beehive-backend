from flask import json, Response
from json import dumps

def custom_response(res, status_code):
  """Custom Response Function
  Param arguments:
    res -- json response
    status_code -- code
  Return: Response
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
)

def custom_response_csv(res, status_code):
  """Custom Response Function
  Param arguments:
    res -- csv response
    status_code -- code
  Return: Response
  """

  return Response(
    mimetype="application/csv",
    response=res,
    status=status_code,
    headers={
      "Content-Disposition": "attachment;filename=data.csv"
    }
  )