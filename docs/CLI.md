# Command Line Interface

To allow EI-PaaS user push your analytic app from the local machine, **EI-PaaS AFS SDK** provides a **Command Line Interface(CLI)** for users.
The CLI only provides one function, to **push** analytic app into your service instance of EI-PaaS AFS.

## Steps

1. Login to AFS with your EI-PaaS SSO user and the target AFS endpoint. For example:
    ```
    eipaas-afs login portal-afs.iii-cflab.com $USERNAME $PASSWORD
    ```

2. List all service instances for your EI-PaaS SSO user.
    ```
    eipaas-afs service_instances
    ```

3. Select one of service instance you want to push this analytic app to.
    ```
    eipaas-afs target -s $SERVIE_INSTANCE_ID

4. Change your current directory to your analytic app and run the command:
    ```
    eipaas-afs push
    ```
    This will read the **manifest.yml** and push this analytic app into your workspace.
    This operation may take a while, just patient.

5. Use AFS portal to check the result.
