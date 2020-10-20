# import the necessary packages
import io
import sys
import cv2
import uvicorn
import numpy as np
from PIL import Image

from fast_api.prediction import Prediction
from fast_api.constants import OCR_MODEL_PATH
from fast_api.utils.solve_sudoku import solve_sudoku


from tensorflow.keras.models import load_model
from fastapi import FastAPI, File, UploadFile, HTTPException

import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''


# load the model
print('[INFO] loading model...')
model = load_model(OCR_MODEL_PATH, compile=True)

# get the model input shape to transform any inputs into this shape
input_shape = model.layers[0].input_shape
_, width, height, channel = input_shape

# define the FastAPI app
app = FastAPI()


# main route
@app.get('/')
def root_route():
    return {'error': 'Use GET /prediction instead of the root route!'}


# solve sudoku route
@app.post('/api/sudoku', response_model=Prediction)
async def sudoku(file: UploadFile = File(...)):
    # check if content type is image, else raise and error
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail=f'File \'{file}\' is not an image file!')

    try:
        # read the contents (bytes) into opencv format and send for sudoku solving
        contents = await file.read()
        image = cv2.imdecode(np.frombuffer(contents, dtype=np.uint8), -1)
        results = solve_sudoku(model=model, image=image, resize_target=(width, height, channel))

        return {
            'file_name': file.filename,
            'content_type': file.content_type,
            'sudoku_board': results.board,
            'sudoku_shape': (results.width, results.height),
            'sudoku_size': results.size
        }
    except:
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
