import os
import sys
from src.utils.database_handler import MongodbClient
from src.exception import CustomException

"""
This script does the samething as s3_setup. It sync the images from our data folder to MongoDB so we can keep count of our labels.
Please see AWS-MongoDB-Setup for more detail reason why we are doing this. I hope you know before you even go to that docx file. If not,
then refresh your memory
"""
class MetaDataStore:
    def __init__(self):
        self.root = os.path.join(os.getcwd(), "data")
        self.images = os.path.join(self.root, "caltech-101")
        self.labels = os.listdir(self.images)
        self.mongo = MongodbClient()

    def register_labels(self):
        """
        This is where the magic is done which I talked about in AWS-MongoDB-Setup
        """
        try:
            records = {}
            for num, label in enumerate(self.labels): #Get all the labels in ranks so like 0:"accordion",1:"airplanes" etc etc which will end 
                                                      #up giving us the total count
                records[f"{num}"] = label

            self.mongo.database['labels'].insert_one(records) #Now insert those rank records in MongoDB. So we will have all the labels with
                                                             #it corresponding rank

        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}

    def run_step(self):
        try:
            self.register_labels()
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}


if __name__ == "__main__":
    meta = MetaDataStore()
    meta.run_step()
