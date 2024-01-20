import os
import sys
from zipfile import ZipFile
import shutil
from src.exception import CustomException

"""
This script sync our data to AWS S3. There are some cleaning process done as well like remove categorical images that we dont need
"""
# https://www.kaggle.com/datasets/imbikramsaha/caltech-101 [ Get data from kaggle and put it into data folder ]

class DataStore:
    def __init__(self):
        """
        Here we are just creating path to our data which we just downloaded
        """
        self.root = os.path.join(os.getcwd(), "data") #Data folder
        self.zip = os.path.join(self.root, "archive.zip")
        self.images = os.path.join(self.root, "caltech-101") #So if we unzip the archive.zip we will have another folder called caltech-101
                                                             #where our images we be
        self.list_unwanted = ["BACKGROUND_Google"] #So inside the caltech-101 folder. There is a folder (called BACKGROUND_Google) that has 
                                                   #pictures we dont want on our training

    def prepare_data(self):
        """
        Here we are just unzipping the archive.zip file
        """
        try:
            print(" Extracting Data ")
            with ZipFile(self.zip, 'r') as files:
                files.extractall(path=self.root) #Unzip archive.zip on self.root = Search_Engine/search-engine-data-collection/data

            files.close()
            print(" Process Completed ")
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}

    def remove_unwanted_classes(self):
        """
        Here we are just performing some cleaning. We don't want BACKGROUND_Google folder so we are gonna remove it with the help of this
        function in our class
        """
        try:
            print(" Removing unwanted classes ")
            for label in self.list_unwanted:
                path = os.path.join(self.images,label)
                shutil.rmtree(path, ignore_errors=True) #Remove the whole folder including the images inside of that BACKGROUND_Google folder
            print(" Process Completed ")
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}

    def sync_data(self):
        """
        After cleaning is done above. We can now make a connection to our S3 Bucket and that what this function does
        """
        try:
            print("\n====================== Starting Data sync ==============================\n")
            #You can get this URL from AWS by copying S3 URI: s3://data-collection-s3bucket/images/
            #Here os.system just mean, look inside our environmental variable for the secret keys to make the connect to AWS S3
            os.system(f"aws s3 sync { self.images } s3://data-collection-s3bucket/images/ ") #Sync caltech-101 = self.images to S3
            print("\n====================== Data sync Completed ==========================\n")

        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}

    def run_step(self):
        try:
            self.prepare_data()
            self.remove_unwanted_classes()
            self.sync_data()
            return True
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}


if __name__ == "__main__":
    store = DataStore()
    store.run_step()
