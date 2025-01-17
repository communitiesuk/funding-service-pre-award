# 📜 Scripts


### export_assessment_data script does the following:

The process_assessment_data function performs the processing of assessment data for a given fund round. It takes the following parameters:

- round_id: The UUID of the round for the fund.
- write_csv: A boolean indicating whether to export the data to a CSV file.
- csv_location: The location to save the CSV file (optional if write_csv is False).

During processing, the function retrieves assessment score data for the specified round_id using the get_assessment_records_score_data_by_round_id function. It then proceeds to extract the requested data for the round.

To run locally

        python -m scripts.export_assessment_data --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd True --write_csv True --csv_location ./assessment_data.csv

If there is data in your docker DB, you can also execute this script locally in the container

        docker exec -ti b1afa47afbd5 scripts/export_assessment_data.py --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --write_csv True --csv_location file_location.csv

**To run on paas, execute the following steps**
*Note: Choose the app based on your specific environment. The following example pertains to the test environment.*

1. Before running the task, make sure you're recording the logs and and DO NOT change the file name `tail.txt`

        cf logs funding-service-design-assessment-store-test | tee ~/tail.txt

1. In a new terminal window, run task as usual, give it a unique --name and DO NOT change the file name `assessment_data.csv`

        cf run-task funding-service-design-assessment-store-test --command "python -m scripts.export_assessment_data --round_id c603d114-5364-4474-a0c4-c41cbf4d3bbd --write_csv True --csv_location /tmp/assessment_data.csv && cat /tmp/assessment_data.csv" --name export_assessment_data

1. Wait for the logs to finish, ends at `destroying container for instance`, and Ctrl + C command on the terminal window running the cf logs to save the file.
1. Next, execute the "sed" command to eliminate unnecessary logs.

if you are on Windows sub system for Linux or Linux run the following command:

        sed -e 's/.*] OUT//' -e '0,/Exit/I!d' -e 's/Exit.*//;/^$/d' -e '/Retrieving/,/\/tmp\/assessment_data.csv/d' ~/tail.txt > ~/final.csv

If you are on Mac, run the following command:


        sed -e 's/.*] OUT//' -e 's/Exit.*//;/^$/d' -e '/Retrieving/,/\/tmp\/assessment_data.csv/d' ~/tail.txt > ~/final.csv

*Please note this command leaves two trailing lines at the end of the file which look like this and they can be deleted manually:*

        Cell 9bc96142-b9d9-435a-8dd0-723da2db27c7 stopping instance a08d8872-3035-44cc-a109-07842236fed6
        Cell 9bc96142-b9d9-435a-8dd0-723da2db27c7 destroying container for instance a08d8872-3035-44cc-a109-07842236fed6


1. `final.csv` will be located in the /home/<name of user> directory on the local machine, otherwise known as ~/  - alternatively, you can direct `final.csv` wherever you like, as long as you know the directory structure. ~/ will be the easiest to locate for both Macs and PCs.


## Delete Data
This script is intended for using in test environments, NEVER in production. It allows deletion of a specific single assessment record, or of all assessment records in a round.

The parameter `c` determines whether or not the deletes will be committed to the database. Before updating the database the script will prompt for confirmation - you can suppress this with `q`.

To delete a single assessment record, and commit, with a prompt to confirm:
```
python -m scripts.delete_data delete-assessment-record -id <application_id_to_delete> -c
```
To delete a single assessment record, and commit, with no prompt for confirmation:
```
python -m scripts.delete_data -q delete-assessment-record -id <application_id_to_delete> -c
```

To delete all assessments in a round, but not commit:
```
python -m scripts.delete_data delete-all-assessments-in-round -r <round_id_to_delete>
```

To run on AWS, wrap the above commands in:
```
copilot svc exec --name fsd-assessment-store --app pre-award --command "launcher <command goes here>"
```

### seed_assessment_store script

The `seed_assessment_store` script is used to initialize and populate the assessment store with seed data. It ensures that the assessment store has the necessary data.

#### Functionality

- Connects to the assessment store database.
- Inserts predefined seed data into the assessment store.
- Verifies that the data has been correctly inserted.

#### Requirements

- Python 3.x
- Necessary database credentials and access permissions.

#### Usage

To run the script locally, use the following command:

```sh
python -m invoke assessment.seed-assessment-store-db
```

To run the script on AWS, wrap the above command in:

```sh
copilot svc exec --command "launcher python -m invoke assessment.seed-assessment-store-db”
```
