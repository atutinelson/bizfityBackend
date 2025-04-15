import firebase_admin
import os
from django.conf import settings
from firebase_admin import credentials ,messaging


def initializationOfFirebaseClient():
    if not  firebase_admin._apps:
        path = os.path.join(settings.BASE_DIR,"bizfity-31dd6-firebase-adminsdk-fbsvc-c86b604119.json")
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)


def sendPushNotification(device_token,title, body):
    initializationOfFirebaseClient()
    
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=device_token,
    )

    response = messaging.send(message)
    print("Successfully sent message:", response)
    