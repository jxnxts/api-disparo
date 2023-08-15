from compreface import CompreFace
from compreface.service import RecognitionService
from compreface.collections import FaceCollection
from compreface.collections.face_collections import Subjects
from dotenv import load_dotenv
import os

load_dotenv()

DOMAIN = os.getenv('DOMAIN')
PORT= os.getenv('PORT')
API_KEY= os.getenv('API_KEY')

compre_face: CompreFace = CompreFace(DOMAIN, PORT)

recognition: RecognitionService = compre_face.init_face_recognition(API_KEY)

face_collection: FaceCollection = recognition.get_face_collection()

subjects: Subjects = recognition.get_subjects()



def _recognitionImage(image):
    data = recognition.recognize(image_path=image)
    return data

