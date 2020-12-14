# Implementing Canary Releases of TensorFlow Model Deployments with Kubernetes and Istio


## GSP778


![[/fragments/labmanuallogo]]


## Overview




AutoML Vision helps developers with limited ML expertise train high quality image recognition models. Once you upload images to the AutoML UI, you can train a model that will be immediately available on Google Cloud for generating predictions via an easy to use REST API.

In this lab you will upload images to Cloud Storage and use them to train a custom model to recognize different types of clouds (cumulus, cumulonimbus, etc.).

#### __What you'll learn__

* Uploading a labeled dataset to Cloud Storage and connecting it to AutoML Vision with a CSV label file.
* Training a model with AutoML Vision and evaluating its accuracy.
* Generating predictions on your trained model.


## Setup and requirements




### __Qwiklabs setup__

![[/fragments/startqwiklab]]

![[/fragments/gcpconsole]]



## Set up AutoML Vision


AutoML Vision provides an interface for all the steps in training an image classification model and generating predictions on it. Start by enabling the Cloud AutoML API.

From the __Navigation menu__, select __APIs & Services__ > __Library__.

In the search bar type in "Cloud AutoML". Click on the __Cloud AutoML API__ result and then click __Enable__.


This will take a minute to set up.

Now open this [AutoML UI](https://console.cloud.google.com/vision/datasets) link in a new browser.



Click __Check my progress__ to verify the objective.

<ql-activity-tracking step=1>
    Enable the AutoML API
</ql-activity-tracking>




![[/fragments/cloudshell]]

In Cloud Shell use the following commands to create environment variables for you Project ID and Username, replacing `<USERNAME>` with the User Name you logged into the lab with:

```
export PROJECT_ID=$DEVSHELL_PROJECT_ID
```
```
export QWIKLABS_USERNAME=<USERNAME>
```

Run the following command to give AutoML permissions:

```
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="user:$QWIKLABS_USERNAME" \
    --role="roles/automl.admin"
```

Now create a storage bucket by running the following:

```
gsutil mb -p $PROJECT_ID \
    -c standard    \
    -l us-central1 \
    gs://$PROJECT_ID-vcm/
```

In the Google Cloud console, open the __Navigation menu__ and click on __Storage__ to see it.

![b91e6a77309137cf.png](img/b91e6a77309137cf.png)


Click __Check my progress__ to verify the objective.

<ql-activity-tracking step=2>
    Create a Cloud Storage Bucket
</ql-activity-tracking>

## Upload training images to Cloud Storage




In order to train a model to classify images of clouds, you need to provide labeled training data so the model can develop an understanding of the image features associated with different types of clouds. In this example your model will learn to classify three different types of clouds: cirrus, cumulus, and cumulonimbus. To use AutoML Vision you need to put your training images in Cloud Storage.

Before adding the cloud images, create an environment variable with the name of your bucket.

Run the following command in Cloud Shell:
```
export BUCKET=$PROJECT_ID-vcm
```

The training images are publicly available in a Cloud Storage bucket.

Use the `gsutil` command line utility for Cloud Storage to copy the training images into your bucket:

```
gsutil -m cp -r gs://automl-codelab-clouds/* gs://${BUCKET}
```

When the images finish copying, click the __Refresh__ button at the top of the Storage browser, then click on your bucket name. You should see 3 folders of photos for each of the 3 different cloud types to be classified:

![autoML_bucket_folders.png](img/autoML_bucket_folders.png)

If you click on the individual image files in each folder you can see the photos you'll be using to train your model for each type of cloud.



## Create a dataset

Now that your training data is in Cloud Storage, you need a way for AutoML Vision to access it. You'll create a CSV file where each row contains a URL to a training image and the associated label for that image. This CSV file has been created for you; you just need to update it with your bucket name.

Run the following command to copy the file to your Cloud Shell instance:

```
gsutil cp gs://automl-codelab-metadata/data.csv .
```

Then update the CSV with the files in your project:

```
sed -i -e "s/placeholder/${BUCKET}/g" ./data.csv
```

Now upload this file to your Cloud Storage bucket:

```
gsutil cp ./data.csv gs://${BUCKET}
```

Once that command completes, click the __Refresh__ button at the top of the Storage browser, then Click on your bucket name. Confirm that you see the `data.csv` file in your bucket.

Navigate back to the [AutoML Vision](https://console.cloud.google.com/vision/datasets) tab. Your page should now resemble the following:

![MLVision_nobeta.png](img/MLVision_nobeta.png)

At the top of the console, click __+ NEW DATASET__.

Type "clouds" for the Dataset name.

Select "Single-Label Classification".


![mlvision-new-dataset.png](img/mlvision-new-dataset.png)

<aside>
In your own projects, you may want to use  [multi-class classification](https://cloud.google.com/vision/automl/docs/datasets).
</aside>

Click __Create Dataset__.

Choose __Select a CSV file on Cloud Storage__ and add the file name to the URL for the file you just uploaded - `gs://your-bucket-name/data.csv`

An easy way to get this link is to go back to the Cloud Console, click on the `data.csv` file. Click on the __copy__ icon in the URI field.

![mlvision-select-file.png](img/mlvision-select-file.png)

Click __Continue__.


It will take 2 - 5 minutes for your images to import. Once the import has completed, you'll be brought to a page with all the images in your dataset.


Click __Check my progress__ to verify the objective.

<ql-activity-tracking step=3>
    Create a Dataset
</ql-activity-tracking>

## Inspect images


After the import completes, click on the __Images__ tab to see the images you uploaded.

![VisionAutoML_images.png](img/VisionAutoML_images.png)

Try filtering by different labels in the left menu (i.e. click cumulus) to review the training images:

<aside class="special"><p><strong>Note: </strong>If you were building a production model, you&#39;d want <em>at least</em> 100 images per label to ensure high accuracy. This is just a demo so only 20 images were used so the model could train quickly.</p>
</aside>

If any images are labeled incorrectly you can click on the image to switch the label:

![mlvision-image-detail.png](img/mlvision-image-detail.png)

To see a summary of how many images you have for each label, click on __LABEL STATS__ at the top of the page. You should see the following show up on the right side of your browser.

![mlvision-label-stats.png](img/mlvision-label-stats.png)

<aside class="special"><p><strong>Note: </strong>If you are working with a dataset that isn&#39;t already labeled, AutoML Vision provides an in-house <a href="https://cloud.google.com/vision/automl/docs/human-labeling"> human labeling service </a>.</p>
</aside>


## Train your model




You're ready to start training your model! AutoML Vision handles this for you automatically, without requiring you to write any of the model code.

To train your clouds model, go to the __Train__ tab and click __Start Training__.

Enter a name for your model, or use the default auto-generated name.

Leave __Cloud-hosted__ selected, then click __Continue__.

Set the node hours set to __8__.

![VisionAutoML_8nodehrs.png](img/VisionAutoML_8nodehrs.png)

Click __Start Training__.


Since this is a small dataset, it will only take around __25-30 minutes__ to complete.

While you're waiting, you can watch this YouTube video on [preparing an image data in AutoML](https://youtu.be/_2eG8xpRYZ4) - the images should look familiar!


## Evaluate your model

In the __Evaluate__ tab, you'll see information about Precision and Recall of the model.

![AutoML_precision_graph.png](img/AutoML_precision_graph.png)

You can also play around with __Score threshold__.

Finally, scroll down to take a look at the __Confusion matrix__.

![AutoML_confusion.png](img/AutoML_confusion.png)

All of this provides some common machine learning metrics to evaluate your model accuracy and see where you can improve your training data. Since the focus for this lab was not on accuracy, move on to the next section about predictions section. Feel free to browse the accuracy metrics on your own.


## Generate predictions


Now it's time for the most important part: generating predictions on your trained model using data it hasn't seen before.

Navigate to the __Test & Use__ tab in the AutoML UI:

![mlvision-test-n-use.png](img/mlvision-test-n-use.png)

__Deploy model__ then __Deploy__.

This will take around __20 minutes__ to deploy.

## Generate predictions

There are a few ways to generate predictions. In this lab you'll use the UI to upload images. You'll see how your model does classifying these two images (the first is a cirrus cloud, the second is a cumulonimbus).

Download these images to your local machine by right-clicking on each of them:

![a4e6d50183e83703.png](img/a4e6d50183e83703.png)

![1d4aaa17ec62e9ba.png](img/1d4aaa17ec62e9ba.png)

Return to the AutoML Vision UI, click __Upload Images__ and upload the clouds to the online prediction UI. When the prediction request completes you should see something like the following:

![AutoML_cumulo.png](img/AutoML_cumulo.png)

Click __Check my progress__ to verify the objective.

<ql-activity-tracking step=4>
    Run the pedictions
</ql-activity-tracking>



Pretty cool - the model classified each type of cloud correctly!



## Congratulations!

You've learned how to train your own custom machine learning model and generate predictions on it through the web UI. Now you've got what it takes to train a model on your own image dataset.

#### __What was covered__

* Uploading training images to Cloud Storage and creating a CSV for AutoML Vision to find these images.
* Reviewing labels and training a model in the AutoML Vision UI.
* Generating predictions on new cloud images.

### Finish your Quest

![ml_quest_icon.png](img/ml_quest_icon.png)
![ML-Image-Processing-badge.png](img/ML-Image-Processing-badge.png)

This self-paced lab is part of the Qwiklabs  [Machine Learning APIs](https://google.qwiklabs.com/quests/32) and [Intro to ML: Image Processing](https://google.qwiklabs.com/quests/85) Quests. A Quest is a series of related labs that form a learning path. Completing a Quest earns you a badge to recognize your achievement. You can make your badge (or badges) public and link to them in your online resume or social media account. Enroll in these Quests and get immediate completion credit if you've taken this lab.  [See other available Qwiklabs Quests](https://google.qwiklabs.com/catalog).

### Take your next lab

Continue your Quest with  [Detect Labels, Faces, and Landmarks in Images with the Cloud Vision API](https://google.qwiklabs.com/catalog_lab/1112), or check out these suggestions:

* [Awwwvision: Cloud Vision API from a Kubernetes Cluster](https://google.qwiklabs.com/catalog_lab/1041)
* [Entity and Sentiment Analysis with the Natural Language API](https://google.qwiklabs.com/catalog_lab/1113)

### Next steps / learn more

* Watch the  [intro video](https://www.youtube.com/watch?v=GbLQE2C181U)
* Learn more about how AutoML Vision works by listening to the  [Google Cloud Podcast episode](https://www.gcppodcast.com/post/episode-109-cloud-automl-vision-with-amy-unruh-and-sara-robinson/)
* Read the announcement  [blog post](https://www.blog.google/topics/google-cloud/cloud-automl-making-ai-accessible-every-business/)
* Learn how to  [perform each step with the API](https://cloud.google.com/vision/automl/docs/beginners-guide)

![[/fragments/TrainingCertificationOverview]]

##### Manual Last Updated September 07, 2020

##### Lab Last Tested September 07, 2020

![[/fragments/copyright]]
