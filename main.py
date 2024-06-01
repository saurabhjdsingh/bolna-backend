import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Header
from fastapi.responses import JSONResponse
import aiohttp

app = FastAPI()
load_dotenv()
host = os.getenv("host")


@app.get("/")
def read_root():
    return {"host": host}


@app.post("/create")
async def create_batch(api_key: str = Form(...), agent_id: str = Form(...), file: UploadFile = File(...)):
    url = host + '/batches'
    headers = {'Authorization': f'Bearer {api_key}'}
    form_data = aiohttp.FormData()
    form_data.add_field('agent_id', agent_id)
    form_data.add_field('file', file.file, filename=file.filename, content_type='application/octet-stream')

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=form_data) as response:
                response_data = await response.json()
                return JSONResponse(content=response_data, status_code=response.status)
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/schedule")
async def schedule_batch(api_key: str = Form(...), agent_id: str = Form(...), batch_id: str = Form(...), scheduled_at: str = Form(...)):
    url = host + '/batches/schedule'
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {
        'agent_id': agent_id,
        'batch_id': batch_id,
        'scheduled_at': scheduled_at
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                response_data = await response.json()
                if response.status == 200:
                    return JSONResponse(content=response_data)
                else:
                    raise HTTPException(status_code=response.status, detail=response_data)
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/batches/{agent_id}/{batch_id}")
async def get_batch_status(agent_id: str, batch_id: str, api_key: str = Header(...)):
    url = host + f'/batches/{agent_id}/{batch_id}'
    headers = {'Authorization': f'Bearer {api_key}'}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response_data = await response.json()
                if response.status == 200:
                    return JSONResponse(content=response_data)
                else:
                    raise HTTPException(status_code=response.status, detail=response_data)
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/executions/{agent_id}/{batch_id}")
async def get_batch_executions(agent_id: str, batch_id: str, api_key: str = Header(...)):
    url = host + f'/batches/{agent_id}/{batch_id}/executions'
    headers = {'Authorization': f'Bearer {api_key}'}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response_data = await response.json()
                if response.status == 200:
                    return JSONResponse(content=response_data)
                else:
                    raise HTTPException(status_code=response.status, detail=response_data)
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
