import csv
import json
import io
import aiohttp
import requests
from fastapi import FastAPI, File, UploadFile
from openpyxl import Workbook
from defusedxml.ElementTree import parse as xml_parse


app = FastAPI()


@app.post("/csv-to-json")
async def csv_to_json(file: UploadFile = File(...)):
    contents = await file.read()
    rows = csv.DictReader(io.StringIO(contents.decode("utf-8")))
    result = json.dumps(list(rows))
    headers = {
    'accept': 'application/json',
}
    requests.post('http://localhost:8000/upload_file/', headers=headers, files={'file': (file.filename + ".json",result)})
    #requests.post('',)
    # async with aiohttp.ClientSession() as session:
    #     async with session.post('localhost:8000/upload_file/', data=outfile) as resp:
    #         pass
    return {"result": file.filename + ".json"}


@app.post("/csv-to-xlsx")
async def csv_to_xlsx(file: UploadFile = File(...)):
    contents = await file.read()
    rows = csv.reader(io.StringIO(contents.decode("utf-16")))
    
    wb = Workbook()
    ws = wb.active
    for row in rows:
        ws.append(row)
    output = io.BytesIO()
    
    # Save the Excel file to the buffer
    wb.save(output)
    byte_stream = output.getvalue()
    
    headers = {
    'accept': 'application/json',
}
    requests.post('http://localhost:8000/upload_file/', headers=headers, files={'file': (file.filename + ".xlsx",byte_stream)})
    return {"result": byte_stream}


@app.post("/csv-to-xml")
async def csv_to_xml(file: UploadFile = File(...)):
    contents = await file.read()
    rows = csv.DictReader(io.StringIO(contents.decode("utf-8")))
    root = xml_parse("<root></root>").getroot()
    for row in rows:
        item = xml_parse("<item></item>").getroot()
        for key, value in row.items():
            child = xml_parse("<{}></{}>".format(key, key)).getroot()
            child.text = value
            item.append(child)
        root.append(item)
    buffer = io.BytesIO()
    root.write(buffer, encoding="utf-8", xml_declaration=True)
    buffer.seek(0)
    return {"result": buffer}
