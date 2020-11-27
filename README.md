# COVIDCTNET

Here is an implementation of CovidCTNet model for the prediction of COVID-19 cases based on CT images. 
For more detail about the project please use [this link](https://arxiv.org/abs/2009.05096) to access the paper.
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

### Test data
If you want to test our model, visulize the images and etc, please download the dataset from the following links and put them in `/preprocessed/ct-normal-slices-test` folder. Using them you can skip preprocessing steps (1&2).

| Description | Link to .npy array |
| ------ | ------ |
| COVID-19 case No.1| [Download](https://drive.google.com/file/d/1-AP07TKRAqQbd9EnYJgU3FZykjgztNeW/view?usp=sharing) |
| COVID-19 case No.2| [Download](https://drive.google.com/file/d/1-HLUScpgGFi5lL-NJ4JI_OKgqwa8UsCl/view?usp=sharing) |
| COVID-19 case No.3| [Download](https://drive.google.com/file/d/1-KyXYh8Y-r6__fNECOTZV9drhTJuOwT-/view?usp=sharing) |
| Control case No.1| [Download](https://drive.google.com/file/d/10YTyUdOmIuIPq1W0OI1qB9cBr_uHJVMZ/view?usp=sharing) |
| Control case No.2| [Download](https://drive.google.com/file/d/10Zj_6F6tY86mtivNCGbUHQUP07x5-_EH/view?usp=sharing) |
| Control case No.3| [Download](https://drive.google.com/file/d/10ct3YQAyNWr0fLdFZp6QElaOFR4z1XgR/view?usp=sharing) |
| CAP case No.1| [Download](https://drive.google.com/file/d/11QBndF4aHwrJRZeC8HxmRk1hzODvBiOz/view?usp=sharing) |
| CAP case No.2| [Download](https://drive.google.com/file/d/11Twu7LyWmPbELhHRptm50Eq7lHbKEYKA/view?usp=sharing) |
| CAP case No.3| [Download](https://drive.google.com/file/d/11WYfgEFuWaIrWpjpEbzFvRntmmJ8zId5/view?usp=sharing) |


** Please make sure you have enough space on your drive. Step 1 and 2 of preprocessing will convert your dcm file to numpy files to use and
all subfolders in `preprocessed` folder will be occupied with referred numpy files. If you have any problem with the space in your drive you can increase spacing
form [1,1,1] in preprocessing to larger numbers.
