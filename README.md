# COVIDCTNET

Here is an implementation of CovidCTNet model for the prediction of COVID-19 cases based on CT images. 
For more detail about the project please use [this link](https://www.nature.com/articles/s41746-021-00399-3) to access the paper.
These codes are implemented on Google Colab and for Neural Networks models we use Keras. Any library you need for this
project is provided inside the codes.
![Pipeline](/images/image_2020-04-26_14-48-21.png)

## Weights
You can find trained weights in `Model_weight` folder.

## Dicom file

These codes prepared for dicom CT images. Please clone the repository and copy all .dcm files of a patient in a folder and copy all folders of patients
in related folder in `/Data/DCM/...` folder.



## How to train the model
Before training please provide Dicom images. If you want to use trained model, please download weights and add them to the "Model_weight" folder.
Following steps can be helpful for your training:
1.  Run all cells of `/Code/preprocessing/preprocessing-step-1.ipynb` in sequential order.
2.  Run all cells of `/Code/preprocessing/preprocessing-step-2.ipynb` insequential order.
3.  Run all cells of `/Code/training and testing/Training-CovidCTNet.ipynb`in sequential order.

* If you want to train the model from scratch, don't use any weight loading in step 3.
* To train the 3D CNN model and classify if the CT image of the new patient is COVID-19, CAP or Control; you can either initialize weights of our trained model in the third link at the table, or train from the scratch on your own.

## How to test the model
### Steps
For testing the model on your dataset, please follow this list:
1.  Run all cells of `/Code/preprocessing/preprocessing-step-1.ipynb` in sequential order.
2.  Run all cells of `/Code/preprocessing/preprocessing-step-2.ipynb` in sequential order.
3.  Run all cells of `/Code/training and testing/Testing-CovidCTNet.ipynb`in sequential order.


** Please make sure you have enough space on your drive. Step 1 and 2 of preprocessing will convert your dcm file to numpy files to use and
all subfolders in `preprocessed` folder will be occupied with referred numpy files. If you have any problem with the space in your drive you can increase spacing
form [1,1,1] in preprocessing to larger numbers.
