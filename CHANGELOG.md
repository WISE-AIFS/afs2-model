3.8.2 (2022-03-30)
------------------

- Fix Bug - Fix upload models to different model repository

3.8.1 ()
------------------

- Add Requirement - [SDK] Add tag for task and job

3.8.0 (2021-12-26)
------------------

- Add Requirement #23140 - [SDK] Download model from blob define

3.6.2 (2021-11-26)
------------------

- Fix boto3 version

3.6.0 (2021-07-15)
------------------

- Add blob info retries

3.4.0 (2021-05-17)
------------------

- Add Requirement #16536 - [SDK] encrypt / decrypt model with RSA public/private key


3.3.1 (2020/11/11)
------------------

- Add Requirement #16655 - [SDK] Fix decode data_dir message for apm source

- Add Requirement - [SDK] Can use blob credential in env without api version


3.3.0 (unreleased)
------------------

- Add Requirement #15395 - [SDK] Download model through boto3


3.2.0 (2020-07-13)
------------------

- Add Requirement - Support AFS 3.2 upload model to different blob.

- Remove model metadata API.

- Remove part of test case.

- Add Requirement - Update to get blob key credential.


3.0.2 (2020-05-14)
------------------

- Add Requirement #13878 - Support Coefficient parameter

- Fix Bug #13864 - Fix botocore upload incomplete model, and use boto3 instead.


3.0.1 (2020-04-27)
------------------

- Add Requirement #13390 - [SDK] Store dataset_id and target when upload model.


3.0.0 (2020-04-06)
------------------

- Add Requirement - [SDK] Update upload model default using blob mode.

- Add Requirement #12871 - [SDK] Add feature importance field.

- Remove EnSaaS 3.0 function and doc.


2.1.28.2 (2020-03-09)
---------------------

- Fix Bug #12428 -Fix get_model_info and download_model get error model by model_name


2.1.28 (2019-12-27)
-------------------

- Fix accuracy cannot send when value is 0


2.1.27.1 (2019-10-04)
-------------------

- Compatible to py35


2.1.27 (2019-09-19)
-------------------

- Set env blobstore to blob credential


2.1.26 (2019-08-13)
-------------------

- Fix Bug #8788 - Fix download_model doc and token prefix bearer


2.1.25 (2019-08-06)
-------------------

- Add Requirements #8629 - Support model metafile operation(upload, delete, list)


2.1.23 (2019-07-23)
-------------------

- Add Requirements #8366 - Support API by token


2.1.19 (2019-06-26)
-------------------

- Add Requirements #7777 - Upload big model to blob and sync metadata

- Add Bug #7912 - Check the PAI_DATA_DIR value format


2.1.18 (2019-06-17)
-------------------

- Fix Bug #7564 - Fix accuracy cannot be 1.0 error

- Fix Bug #7570 - Fix upload model filepath cannot be path way error

- Add Requirements #7538 - Auto add APM node if setting APM firehose

- Refactor unit tests


2.1.13 (2019-04-29)
-------------------

- Rename afs to afs2-model

- Remove v1 API and v1 unit tests


2.1.8 (2019-03-12)
------------------

- Update env version to AFS_API_VERSION


2.1.2 (2019-02-14)
------------------

- Add v2 models API

- Update v2 models API unit tests


2.0.2 (2019-01-10)
------------------

- Remove duplicate get portal info

- Update version API info.


2.0.0 (2018-12-24)
------------------

- Nothing changed.


1.3.1 (2018-12-07)
------------------

- implement v2 models upload_model

- Update parsers requirements afs-sdk specific version


1.3.0 (2018-11-16)
------------------

- add parsers module to parse ipynb manifest.

- add parsers module unit test

- Add parsers in cli.

- Update config_handler set env from headers changed yet.



1.2.28 (2018-11-08)
-------------------

- Update config_hanelder init

- Update documents



1.2.27 (2018-10-30)
-------------------

- Nothing changed yet.


1.2.26 (2018-10-26)
-------------------

- Fix bug - update services module method

- Add Feature - Integrate AFS hidden space


1.2.25 (2018-10-19)
-------------------

- Nothing changed yet.


1.2.24 (2018-10-16)
-------------------

- Nothing changed yet.


1.2.23 (2018-10-15)
-------------------

- Nothing changed yet.


1.2.22 (2018-10-02)
-------------------


- For AFS 1.2.22

1.2.21 (2018-09-27)
-------------------


- Fix bug - Check value of environment variable is exist in function which use these variable.

- Fix bug - Check status code of request afs api to get env variable.

- Fix bug - Check key of url is exist in next node when request next node.

- Add Feature #757 - Warning message when SDK does not meet AFS version.



1.2.20 (2018-09-19)
-------------------


- For AFS 1.2.20

1.2.19 (2018-09-13)

-------------------





- Add Feature #536 - Limit accuracy between 0-1


- Fix bug #703 - Update the SDK part of ReadtheDocs


- Fix bug #714 - Disable InsecureRequestWarning


- Add Feature #722 - Get the metadata info of the latest model


​





1.2.18 (2018-09-07)


-------------------





- Add Feature - add models module get the latest model info


- Add Feature - add services modules get the credential by key











1.2.17 (2018-08-29)








-------------------





- Add Feature #584: upload model upper limit 2G





- Add Feature #650: SDK get influxdb credential 





- Add Feature #632: AFS upload model naming rule and unit test








1.2.16 (2018-08-22)





-------------------








- Add Feature #599: AFS SDK get numerical, target, select_feature





- Add Feature #574: Add SDK can set and get parameter by list type.





- Add Feature #595: Integrate SDK environment variable and flow handling





- Add Feature: Add SDK services modules, get credential from the subscribed databases or services.





1.2.15 (unreleased)





-------------------





1.2.14 (2018-08-10)





-------------------





- Add Feature #542 - add get_join_table documents
