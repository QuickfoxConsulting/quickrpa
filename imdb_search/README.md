# README for the IMDb Movie's Rating, Storyline, Tagline, and Genres

IMDb robot fetches the rating, storyline, tagline and genres from the [IMDB](https://imdb.com) website. The list of the movies are given in excel file which is included in `excel_file` directory named `imdb.xlsx`. After retreiving rating, storyline, taglines and genres, the robot will append the information in the same excel file and finally copy it into output folder.

It uses [rpaframework] (http://rpaframework.org) Selenium library to automate the process.

After the robot completes the task, the output file can be found in `output` folder.


#### Requirements

- python=3.7.5
- rpaframework==12.8.1
- openpyxl==3.0.9

### Snapshots of input and output of excel file

1. Input Excel file having movies' name

![input excel](/assets/images/input.png)

2. Outpu Excel file after required infos are appended

![output](/assets/images/output.png)

### Snapshots of how movies are filtered and selected to get rating, storyline, tagline, & genres

1. Robot opening browser and searching movie.

![Robot Opening Browser and and searching movie](/assets/images/1.png)

2. Filter movie based on `Movie` only

![Select Movie Only](/assets/images/2.png)

3. Filter again based on exact title match provided on search

![Search Exact title match](/assets/images/3.png)

4. Select the latest movies if movies have more than one list after filter

![Selected Movie](/assets/images/4.png)

5. When no search result are found, or exact title match option not found
![No search result](/assets/images/5.png)


## Development guide

Run the robot locally:

```
rcc run
```

Provide access credentials for Control Room connectivity:

```
rcc configure credentials <your_credentials>
```

Upload to Control Room:

```
rcc cloud push --workspace <workspace_id> --robot <robot_id>
```

### Suggested directory structure

The directory structure given by the template:

```
├── devdata
├── keywords
│   └── keywords.robot
├── libraries
│   └── MyLibrary.py
├── variables
│   └── variables.py
├── conda.yaml
├── robot.yaml
└── tasks.robot
```

where

- `devdata`: A place for all data/material related to development, e.g., test data. Do not put any sensitive data here!
- `keywords`: Robot Framework keyword files.
- `libraries`: Python library code.
- `variables`: Define your robot variables in a centralized place. Do not put any sensitive data here!
- `conda.yaml`: Environment configuration file.
- `robot.yaml`: Robot configuration file.
- `tasks.robot`: Robot Framework task suite - high-level process definition.

In addition to these, you can create your own directories (e.g. `bin`, `tmp`). Add these directories to the `PATH` or `PYTHONPATH` section of `robot.yaml` if necessary.

Logs and artifacts are stored in `output` by default - see `robot.yaml` for configuring this.

Learn how to [handle variables and secrets](https://robocorp.com/docs/development-guide/variables-and-secrets/secret-management).

### Configuration

Give the task name and startup commands in `robot.yaml` with some additional configuration. See [Docs](https://robocorp.com/docs/setup/robot-structure#robot-configuration-file-robot-yaml)for more.

Put all the robot dependencies in `conda.yaml`. These are used for managing the execution environment.

### Additional documentation

See [Robocorp Docs](https://robocorp.com/docs/) for more documentation.
